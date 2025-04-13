import json
from typing import Dict, Set, List

class DecisionTable:
    """
    决策表类，用于存储并管理 “故障 -> {属性 -> 概率}” 的映射结构。
    对应论文中表3、表4的形式。

    主要功能：
    1. 增加、合并故障属性数据
    2. 从 JSON 文件导入
    3. 获取指定故障-属性的概率
    4. 离散化 (0/1/2) 形成“表4”
    5. 抽取部分属性(最小覆盖集)得到一个更小的 DecisionTable 形成表5
    6. 导出当前表

    self.prob_table:
      - 结构：{故障ID: {属性: 概率值}}
      - 例如 {"d1": {"m1":0.9, "m2":0.81}, "d2": {"m2":0.219, "m4":0.267}, ...}
    self.all_attributes:
      - 保存所有出现过的属性集合，便于统一处理
    """

    def __init__(self, prob_dict: Dict[str, Dict[str, float]] = None) -> None:
        """
        构造函数，可传入初始的 prob_dict。
        如果不传，则初始化一个空白表。
        """
        if prob_dict is None:
            prob_dict = {}

        self.prob_table = {}
        self.all_attributes = set()

        # 依次加载初始数据
        for fault_id, attr_map in prob_dict.items():
            self.add_fault_data(fault_id, attr_map)

    def __repr__(self) -> str:
        return (f"<DecisionTable num_faults={len(self.prob_table)} "
                f"num_attrs={len(self.all_attributes)}>\n"
                f"faults={list(self.prob_table.keys())}\n"
                f"attrs={list(self.all_attributes)}>")

    # 添加或更新某个故障的属性概率数据
    def add_fault_data(self, fault_id: str, attr_prob_map: Dict[str, float]) -> None:
        # 若故障不存在，则先初始化一行
        if fault_id not in self.prob_table:
            self.prob_table[fault_id] = {}
            # 给已有属性都置 0.0
            for attr in self.all_attributes:
                self.prob_table[fault_id][attr] = 0.0

        # 找出新出现的属性
        new_attrs = set(attr_prob_map.keys()) - self.all_attributes

        # 对现有故障，把这些新属性补 0.0
        for f_id in self.prob_table:
            if f_id != fault_id:
                for na in new_attrs:
                    self.prob_table[f_id][na] = 0.0

        # 更新整体属性集合
        self.all_attributes.update(new_attrs)

        # 更新/覆盖传入故障的属性值
        for a, val in attr_prob_map.items():
            self.prob_table[fault_id][a] = float(val)

    def import_from_json(self, filepath: str) -> None:
        """
        从 JSON 文件加载数据并合并到当前的 DecisionTable 中。
        JSON 格式示例：
        {
          "d1": {"m1":0.9, "m2":0.81},
          "d2": {"m2":0.219, "m4":0.267, "m8":0.816}
        }
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for fault_id, attr_map in data.items():
            self.add_fault_data(fault_id, attr_map)

    # 获取某个故障在某属性下的概率值
    def get_probability(self, fault_id: str, attr: str) -> float:
        if fault_id not in self.prob_table:
            return 0.0
        return self.prob_table[fault_id].get(attr, 0.0)

    # 离散化
    def discretize_three_levels(self) -> Dict[str, Dict[str, int]]:
        """
        将当前表中的 概率值 离散化为 0/1/2：
          - p > 0.5 => 2
          - 0 < p <= 0.5 => 1
          - p = 0 => 0

        返回一个新的字典（类似 “表4”），不会修改原 prob_table。
        """
        result = {}
        for fault_id, attr_map in self.prob_table.items():
            row = {}
            for a in self.all_attributes:
                p = attr_map.get(a, 0.0)
                if p > 0.5:
                    row[a] = 2
                elif p > 0:
                    row[a] = 1
                else:
                    row[a] = 0
            result[fault_id] = row
        return result

    def export_table3(self) -> Dict[str, Dict[str, float]]:
        """
        导出当前“表3”数据结构（故障->属性->概率值）。
        """
        return self.prob_table

    def export_table4(self) -> Dict[str, Dict[str, int]]:
        """
        导出离散化后的“表4”数据结构（故障->属性->(0/1/2)）。
        """
        return self.discretize_three_levels()

    # 根据给定的属性子集，构造并返回一个新的 DecisionTable
    def extract_attribute_subset(self, subset_attrs: Set[str]) -> "DecisionTable":
        new_prob_dict = {}
        for fault_id, old_attr_map in self.prob_table.items():
            new_attr_map = {}
            for a in subset_attrs:
                val = old_attr_map.get(a, 0.0)
                new_attr_map[a] = val
            new_prob_dict[fault_id] = new_attr_map

        return DecisionTable(new_prob_dict)

    def list_all_faults(self) -> List[str]:
        """返回当前所有故障ID的列表，如 ["d1","d2","d3",...]。"""
        return list(self.prob_table.keys())

    def list_all_attributes(self) -> List[str]:
        """返回当前所有属性的列表，如 ["m1","m2","m3",...]。"""
        return list(self.all_attributes)
