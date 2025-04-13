from .Model import *
from itertools import combinations

# 判断 subset_attrs 这组属性能否区分表中所有故障(决策)对
def can_differentiate_all(decision_table: DecisionTable,
                          subset_attrs: set[str]) -> bool:
    discrete_table = decision_table.discretize_three_levels()
    faults = sorted(discrete_table.keys())
    n = len(faults)
    for i in range(n):
        for j in range(i+1, n):
            f1, f2 = faults[i], faults[j]
            # 如果在 subset_attrs 上都相同，则无法区分
            all_same = True
            for a in subset_attrs:
                if discrete_table[f1][a] != discrete_table[f2][a]:
                    all_same = False
                    break
            if all_same:
                return False  # 发现一对无法区分 => 整体失败
    return True

def find_core_attributes(decision_table: DecisionTable) -> set[str]:
    """
    按“删除属性后是否降低决策能力”来判定核心属性。
    需要一个 calc_decision_ability 函数或者 equivalent logic。
    这里用 can_differentiate_all 做简单替代:
      - 全集能区分 => True
      - 去掉某属性后若不能区分 => 该属性为core
    若需要更严格区分“决策能力”大小，可以使用之前的calc_decision_ability对比。
    """
    all_attrs = decision_table.all_attributes
    # 先看全集能否区分
    if not can_differentiate_all(decision_table, all_attrs):
        # 若全集都不能区分 => 不存在最小属性集
        return set()

    core = set()
    for a in list(all_attrs):
        # 去掉 a
        test_subset = all_attrs - {a}
        if not can_differentiate_all(decision_table, test_subset):
            core.add(a)
    return core

def find_all_min_covers_with_core(decisoin_table: DecisionTable) -> list[set[str]]:
    """
    1. 先求 core；
    2. 枚举属性子集大小从 |core| 到 全属性数;
       - 仅枚举包含 core 的子集
       - 检查能否区分全部故障
       - 找到第一批可行解就返回(获得所有同样大小解)
    """
    # 全属性
    all_attrs = decisoin_table.all_attributes

    core_set = find_core_attributes(decisoin_table)
    print(f"核心属性 core = {core_set}")

    # 如果 core 自己都无法区分 => 还需要更多属性
    # 逐渐增加
    non_core = all_attrs - core_set
    total = len(non_core)

    solutions = []
    # 枚举子集大小 s 从 c_size 到 total
    for s in range(1, total+1):
        # 枚举
        found_any = False
        for combo in combinations(non_core, s):
            subset = set(combo) | core_set
            # 测试是否能区分全部故障
            if can_differentiate_all(decisoin_table, subset):
                solutions.append(subset)
                found_any = True

        if found_any:
            # 已找到大小为 s 的可行解, 即最小 => 不再往下找
            break

    return solutions