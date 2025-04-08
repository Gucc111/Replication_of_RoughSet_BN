from src.Simplify import *

def main():
    objects = ['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10']
    attributes = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9']
    decision = 'd'

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
    dec_table = DecisionTable(objects, attributes, decision, data)
    disc_matrix = DiscernibilityMatrix(dec_table)

    print(f'【可辨识矩阵】')
    for k, v in disc_matrix.matrix.items():
        print(f'{k}: {v}', end='\n')
    print()
    mini_set = get_greedy_cover(disc_matrix)
    mini_set = refine_cover(mini_set, disc_matrix)
    print(mini_set)

if __name__ == "__main__":
    main()
