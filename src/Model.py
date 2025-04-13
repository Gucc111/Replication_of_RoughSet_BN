import json

class DecisionTable:
    def __init__(self, prob_dict: dict[str, dict[str,float]] = None):
        """
        初始化: 传入一个 {故障: {属性: 概率}} 结构, 或不传(空表).
        """
        if prob_dict is None:
            prob_dict = {}
        self.prob_table = {}
        # 用来记录所有属性的并集, 便于后续统一处理
        self.all_attributes = set()
        # 一次性加载
        for fault_id, attr_map in prob_dict.items():
            self.add_fault_data(fault_id, attr_map)

    # 对已存在属性做更新, 对未知属性自动补0给别的故障
    def add_fault_data(self, fault_id: str, attr_prob_map: dict[str, float]):
        # 若故障不存在, 初始化空dict
        if fault_id not in self.prob_table:
            self.prob_table[fault_id] = {}
            # 先给已有属性都置0
            for attr in self.all_attributes:
                self.prob_table[fault_id][attr] = 0.0
        
        # 先记录要新加的属性名
        new_attrs = set(attr_prob_map.keys()) - self.all_attributes
        for f_id in self.prob_table.keys():
            if f_id != fault_id:
                for na in new_attrs:
                    self.prob_table[f_id][na] = 0.0
        
        # 更新并集
        self.all_attributes.update(new_attrs)

        # 更新当前fault的数据
        for a, val in attr_prob_map.items():
            # 若 a 在 old_attributes, 直接赋值; 不在就由上面流程补0
            self.prob_table[fault_id][a] = float(val)

    def import_from_json(self, filepath: str):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # data 应该是一个 {故障: {属性: 值}} 结构
        for fault_id, attr_map in data.items():
            self.add_fault_data(fault_id, attr_map)

    # 返回 fault_id 在属性 attr 下的概率
    def get_probability(self, fault_id: str, attr: str) -> float:
        if fault_id not in self.prob_table:
            return 0.0
        return self.prob_table[fault_id].get(attr, 0.0)

    # 离散化处理
    def discretize_three_levels(self) -> dict[str, dict[str, int]]:
        """
        将 self.prob_table (故障->属性->概率) 离散化为三等级:
        - p>0.5 => 2
        - 0 < p <= 0.5 => 1
        - p=0 => 0
        """
        result = {}
        for fault_id, attr_map in self.prob_table.items():
            row = {}
            for a in self.all_attributes:
                p = attr_map.get(a, 0.0)
                if p > 0.5:
                    row[a] = 2
                elif p > 0:  # 0 < p <= 0.5
                    row[a] = 1
                else:        # p == 0
                    row[a] = 0
            result[fault_id] = row
        return result

    def export_table3(self) -> dict[str, dict[str,float]]:
        return self.prob_table

    def export_table4(self) -> dict[str, dict[str,int]]:
        return self.discretize_three_levels()

    def list_all_faults(self):
        """返回当前所有故障的列表(类似 d1,d2,...)."""
        return list(self.prob_table.keys())

    def list_all_attributes(self):
        """返回所有属性(类似 m1,m2,m3,m4,...)."""
        return list(self.all_attributes)
