from itertools import combinations
from typing import List, Set
from .Model import DecisionTable

# 判断在给定的属性子集subset_attrs下，能否区分决策表中所有故障对
def can_differentiate_all(decision_table: DecisionTable,
                          subset_attrs: Set[str]) -> bool:
    discrete_table = decision_table.discretize_three_levels()
    fault_ids = sorted(discrete_table.keys())  # 排序一下，便于成对遍历
    n = len(fault_ids)

    for i in range(n):
        for j in range(i+1, n):
            f1, f2 = fault_ids[i], fault_ids[j]
            # 检查 subset_attrs 下的所有属性是否都相同
            if all(discrete_table[f1][a] == discrete_table[f2][a] for a in subset_attrs):
                return False
    return True

# 求核属性集 Core
def find_core(decision_table: DecisionTable) -> Set[str]:
    """
    如果去掉某个属性 a 后，导致无法区分所有故障，则该属性 a 是核心属性。
    """
    all_attrs = set(decision_table.all_attributes)

    # 先判断全集是否能区分所有故障，如果不行则直接返回空集
    if not can_differentiate_all(decision_table, all_attrs):
        return set()

    core = set()
    for a in all_attrs:
        test_subset = all_attrs - {a}
        # 若去掉 a 导致无法区分，则 a ∈ core
        if not can_differentiate_all(decision_table, test_subset):
            core.add(a)
    return core

# 使用穷举的方式求最小覆盖属性集，可能返回多个同样大小的解（不唯一）
def find_min_covers_exhaustive(decision_table: DecisionTable) -> List[Set[str]]:
    """
    1. 先计算 core 属性集
    2. 若 core 无法区分所有故障，则需要额外属性
    3. 在非核心属性里从小到大组合，并与 core 并集后判断能否区分所有故障
    4. 一旦找到第一个大小 s 的可行组合，就收集全部同大小组合，然后停止
    """
    all_attrs = set(decision_table.all_attributes)
    core_set = find_core(decision_table)
    print(f"核心属性 core = {core_set}")

    # 非核心属性集合
    non_core = all_attrs - core_set
    total = len(non_core)

    solutions = []
    # 从 0..total 的子集大小中逐个尝试
    # 因为我们先固定选 core，所以只需要在 non_core 里选 s 个
    for s in range(total+1):
        found_any = False
        for combo in combinations(non_core, s):
            subset = core_set.union(combo)
            if can_differentiate_all(decision_table, subset):
                solutions.append(subset)
                found_any = True
        if found_any:
            # 找到最小大小 s + |core| 的可行解，就不往更大枚举
            break

    return solutions
