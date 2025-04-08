from .Model import *

# 验证 cover_set 是否能覆盖所有冲突对
def verify_cover(cover_set: set[str], disc_matrix: DiscernibilityMatrix) -> bool:
    for (x,y) in disc_matrix.all_conflict_pairs():
        diff_attrs = disc_matrix.get_discern_set(x,y)
        if len(cover_set.intersection(diff_attrs)) == 0:
            return False
    return True

# 绝对能覆盖搜有冲突对的某个条件属性
def get_core(disc_matrix: DiscernibilityMatrix) -> set[str]:
    cover_set = disc_matrix.decision_table.attributes
    core = set()

    for a in cover_set:
        candidate = set(cover_set) - {a}
        if verify_cover(candidate, disc_matrix):
            continue
        else:
            core.add(a)
    
    return core

def get_core2(disc_matrix: DiscernibilityMatrix, core=None) -> set[str]:
    cover_set = disc_matrix.decision_table.attributes
    if core:
        cover_set = set(cover_set) - core
    
    temp = set()
    for a in cover_set:
        candidate = set(cover_set) - {a}
        if verify_cover(candidate, disc_matrix):
            continue
        else:
            pass
        temp.add(a)
    
    if not core:
        return temp
    return temp | core

# 在给定的可辨识矩阵上用贪心算法找最小覆盖
def get_greedy_cover(disc_matrix: DiscernibilityMatrix, verbose: bool=True) -> set[str]:
    """
    1. 将所有冲突对视为未覆盖
    2. 不断选能覆盖最多未覆盖对的属性
    3. 更新已覆盖对
    4. 重复直到无未覆盖对或无法进一步覆盖
    """
    conflict_pairs = disc_matrix.all_conflict_pairs() # 冲突对
    matrix = disc_matrix.matrix # 可辨识矩阵
    core = get_core(disc_matrix)
    attributes = set(disc_matrix.decision_table.attributes) - core

    uncovered = set(conflict_pairs)
    cover_set = set()
    step = 0

    while uncovered:
        step += 1
        best_attr = None
        best_cover_count = 0

        for a in attributes:
            coverset = {(x,y) for (x,y) in uncovered if a in matrix[(x,y)]}
            count = len(coverset)
            if count > best_cover_count:
                best_cover_count = count
                best_attr = a

        if best_attr is None:
            if verbose:
                print(f"[GreedyCover] Step {step}: 无法继续覆盖, 剩余对{len(uncovered)}.")
            break

        cover_set.add(best_attr)
        newly_covered = {(x,y) for (x,y) in uncovered if best_attr in matrix[(x,y)]}
        uncovered -= newly_covered

        if verbose:
            print(f"[GreedyCover] Step {step}: 选属性 {best_attr}, 覆盖 {best_cover_count} 对, 剩余 {len(uncovered)} 对。")

    return cover_set | core

# 冗余删除: 尝试去掉多余的属性, 使得依然覆盖全部冲突对
def refine_cover(cover_set: set[str], disc_matrix: DiscernibilityMatrix, verbose:bool=True) -> set[str]:
    refined = set(cover_set)
    changed = True
    round_idx = 0

    while changed:
        changed = False
        round_idx += 1
        for a in list(refined):
            candidate = refined - {a}
            if verify_cover(candidate, disc_matrix):
                refined = candidate
                changed = True
                if verbose:
                    print(f"[Refine] Round {round_idx}: 删除冗余属性 {a}")
                break
    
    return refined
