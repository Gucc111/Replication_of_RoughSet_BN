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

    # uncovered = set(conflict_pairs)
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

from typing import List, Dict, Set, Tuple

class DecisionTable:
    """
    决策表类：存储对象、属性及其决策值。
    提供冲突对象对(list_conflict_pairs)等接口。
    """
    def __init__(self,
                 objects: List[str],
                 attributes: List[str],
                 decision: str,
                 data: Dict[str, Dict[str, int or str]]):
        self.objects = objects
        self.attributes = attributes
        self.decision = decision
        # data: { "x1": {"a1":..., "a2":..., ..., "d":"故障?..."} }
        self.data = data

    def get_decision(self, obj: str):
        return self.data[obj][self.decision]

    def get_value(self, obj: str, attr: str):
        return self.data[obj][attr]

    def list_conflict_pairs(self) -> List[Tuple[str,str]]:
        """
        列出所有决策不同的对象对(x,y)，x<y。
        """
        conflict_pairs = []
        n = len(self.objects)
        for i in range(n):
            for j in range(i+1, n):
                x, y = self.objects[i], self.objects[j]
                if self.get_decision(x) != self.get_decision(y):
                    conflict_pairs.append((x,y))
        return conflict_pairs


class DiscernibilityMatrix:
    """
    可辨识矩阵：存储(对象对) -> (可辨识属性集)的映射。
    """
    def __init__(self, decision_table: DecisionTable):
        self.decision_table = decision_table
        self.conflict_pairs = decision_table.list_conflict_pairs()
        self.matrix: Dict[Tuple[str,str], Set[str]] = {}

        for (x,y) in self.conflict_pairs:
            diff_attrs = set()
            for a in decision_table.attributes:
                if decision_table.get_value(x,a) != decision_table.get_value(y,a):
                    diff_attrs.add(a)
            self.matrix[(x,y)] = diff_attrs

    def all_conflict_pairs(self) -> List[Tuple[str,str]]:
        return self.conflict_pairs

    def get_discern_set(self, x: str, y: str) -> Set[str]:
        if (x,y) in self.matrix:
            return self.matrix[(x,y)]
        elif (y,x) in self.matrix:
            return self.matrix[(y,x)]
        else:
            return set()


def find_all_min_covers(disc_matrix: DiscernibilityMatrix, verbose: bool = True):
    """
    使用回溯搜索，找出所有最小属性覆盖解。
    返回 (best_size, solutions):
      best_size: int -> 最小覆盖的属性数
      solutions: list[set[str]] -> 所有同大小的覆盖解
    """
    conflict_pairs = disc_matrix.all_conflict_pairs()        # [(x,y), ...]
    matrix = disc_matrix.matrix                              # (x,y)->可辨识属性集
    attributes = disc_matrix.decision_table.attributes       # 全部属性
    
    # 全局保存
    best_size = [float('inf')]
    best_solutions = []

    def backtrack(cover_so_far: Set[str],
                  uncovered: Set[Tuple[str,str]],
                  start_index: int):
        # 剪枝1：若当前选择的属性数 >= 已知最优 => 直接停止
        if len(cover_so_far) >= best_size[0]:
            return
        
        # 若 uncovered 为空 => 找到一个可行解
        if not uncovered:
            size_now = len(cover_so_far)
            if size_now < best_size[0]:
                best_size[0] = size_now
                best_solutions.clear()
                best_solutions.append(set(cover_so_far))
            elif size_now == best_size[0]:
                best_solutions.append(set(cover_so_far))
            return
        
        # 若属性用完，则无法再覆盖
        if start_index >= len(attributes):
            return
        
        # 当前要处理的属性
        a = attributes[start_index]
        
        # 分支1: 选用属性 a
        coverset = {(x,y) for (x,y) in uncovered if a in matrix[(x,y)]}
        new_uncovered = uncovered - coverset
        
        cover_so_far.add(a)
        backtrack(cover_so_far, new_uncovered, start_index+1)
        cover_so_far.remove(a)

        # 分支2: 不选属性 a
        backtrack(cover_so_far, uncovered, start_index+1)

    # 初始 uncovered 全部冲突对
    uncovered_set = set(conflict_pairs)
    # 开始回溯
    backtrack(set(), uncovered_set, 0)

    if verbose:
        print(f"回溯完成, 最优大小 = {best_size[0]}")
        print(f"共有 {len(best_solutions)} 个最小覆盖解。")
        for sol in best_solutions:
            print("  解:", sol)

    return best_size[0], best_solutions
