from src.Model import DecisionTable
from src.Simplify import find_min_covers_exhaustive
from src.Reasoning import reasoning
from src.utils import show_table
import sys

def main():
    dec_table = DecisionTable()
    dec_table.import_from_json('./Data/data.json')
    
    solutions = find_min_covers_exhaustive(dec_table)
    print('最小覆盖集分别是：')
    for i, s in enumerate(solutions):
        print(sorted(s))
        show_table(dec_table.extract_attribute_subset(s).export_table4()).to_html(f'Results/table_5_{i+1}.html')
    print()

    dec_table = dec_table.extract_attribute_subset(solutions[0])
    print('【表5】 最小故障诊断决策表')
    print(show_table(dec_table.export_table4()))
    print()

    ab_attr = sys.stdin.readline().strip().split()
    print()

    decision, results = reasoning(dec_table, ab_attr)
    print(f'{decision} 故障概率最大')
    print('【表7】各故障原因概率')
    print(results)

if __name__ == "__main__":
    main()
