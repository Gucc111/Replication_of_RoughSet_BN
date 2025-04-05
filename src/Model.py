class DecisionTable:
    def __init__(self, objects: list[str], attributes: list[str], decision: str, data: dict[str, dict]):
        self.objects = objects # ["x1","x2",...]
        self.attributes = attributes # ["a1","a2",...]
        self.decision = decision # "d"
        self.data = data # data: {object -> {attr1->val1, ..., decision->dec_val}}

    # 返回某对象的决策值(字符串或其他类型)
    def get_decision(self, obj: str) -> str:
        return self.data[obj][self.decision]

    # 返回某对象在某条件属性上的取值
    def get_value(self, obj: str, attr: str):
        return self.data[obj][attr]

    # 枚举所有决策冲突对象
    def list_conflict_pairs(self) -> list[tuple[str, str]]:
        conflict_pairs = []
        n = len(self.objects)
        for i in range(n):
            for j in range(i+1, n):
                x = self.objects[i]
                y = self.objects[j]
                if self.get_decision(x) != self.get_decision(y):
                    conflict_pairs.append((x,y))
        return conflict_pairs


class DiscernibilityMatrix:
    def __init__(self, decision_table: DecisionTable):
        """
        构造可辨识矩阵:
        1) 先从 decision_table 获取决策冲突的对象对；
        2) 对每对 (x,y) 计算可辨识属性集，即属性取值不同。
        """
        self.decision_table = decision_table
        self.conflict_pairs = decision_table.list_conflict_pairs()
        self.matrix: dict[tuple[str,str], set[str]] = {}

        # 构造可辨识属性集
        for (x,y) in self.conflict_pairs:
            diff_attrs = set()
            for a in decision_table.attributes:
                if decision_table.get_value(x, a) != decision_table.get_value(y, a):
                    diff_attrs.add(a)
            self.matrix[(x,y)] = diff_attrs

    # 返回对象对 (x,y) 的可辨识属性集
    def get_discern_set(self, x: str, y: str) -> set[str]:
        if (x,y) in self.matrix:
            return self.matrix[(x,y)]
        else:
            return set()  # 不在冲突对中或无区别

    # 返回所有在决策上有冲突的对象对
    def all_conflict_pairs(self) -> list[tuple[str, str]]:
        return self.conflict_pairs
