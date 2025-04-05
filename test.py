from src.Simplify import *

def main():
    # 1) 定义一个测试用例
    objects = ['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10']
    attributes = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9']
    decision = 'd'

    # 根据需求自定义数据(属性值 0/1/2 + 决策 "故障1/2/3"等)
    data = {
        'x1':  {'a1': 2, 'a2': 2, 'a3': 0, 'a4': 0, 'a5': 1, 'a6': 0, 'a7': 1, 'a8': 0, 'a9': 0, 'd': '故障1'},
        'x2':  {'a1': 0, 'a2': 1, 'a3': 0, 'a4': 1, 'a5': 0, 'a6': 0, 'a7': 0, 'a8': 2, 'a9': 0, 'd': '故障2'},
        'x3':  {'a1': 0, 'a2': 2, 'a3': 0, 'a4': 0, 'a5': 1, 'a6': 0, 'a7': 1, 'a8': 0, 'a9': 0, 'd': '故障3'},
        'x4':  {'a1': 0, 'a2': 0, 'a3': 0, 'a4': 0, 'a5': 2, 'a6': 2, 'a7': 2, 'a8': 2, 'a9': 0, 'd': '故障4'},
        'x5':  {'a1': 0, 'a2': 0, 'a3': 0, 'a4': 2, 'a5': 0, 'a6': 0, 'a7': 0, 'a8': 0, 'a9': 2, 'd': '故障5'},
        'x6':  {'a1': 0, 'a2': 2, 'a3': 2, 'a4': 0, 'a5': 1, 'a6': 0, 'a7': 0, 'a8': 0, 'a9': 0, 'd': '故障6'},
        'x7':  {'a1': 0, 'a2': 0, 'a3': 0, 'a4': 0, 'a5': 2, 'a6': 0, 'a7': 2, 'a8': 0, 'a9': 0, 'd': '故障7'},
        'x8':  {'a1': 0, 'a2': 0, 'a3': 0, 'a4': 1, 'a5': 2, 'a6': 0, 'a7': 2, 'a8': 2, 'a9': 0, 'd': '故障8'},
        'x9':  {'a1': 0, 'a2': 1, 'a3': 0, 'a4': 0, 'a5': 2, 'a6': 2, 'a7': 2, 'a8': 2, 'a9': 0, 'd': '故障9'},
        'x10':  {'a1': 0, 'a2': 1, 'a3': 0, 'a4': 2, 'a5': 2, 'a6': 0, 'a7': 2, 'a8': 0, 'a9': 0, 'd': '故障10'},
    }

    # 2) 构造决策表
    dec_table = DecisionTable(objects, attributes, decision, data)

    # 3) 生成可辨识矩阵
    disc_matrix = DiscernibilityMatrix(dec_table)

    # (可选)查看部分结果
    print(f'【冲突对象对列表】，共{len(disc_matrix.all_conflict_pairs())}对')
    for pair in disc_matrix.all_conflict_pairs():
        d1 = dec_table.get_decision(pair[0])
        d2 = dec_table.get_decision(pair[1])
        print(f"  {pair}: {d1} vs {d2}")
    print()

    for k, v in disc_matrix.matrix.items():
        print(f'{k}: {v}', end='\n')
    
    core = get_core(disc_matrix)
    print(core)

if __name__ == "__main__":
    main()
