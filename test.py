from src.Model import *
from src.Simplify import *
from src.utils import *

def main():
    dec_table = DecisionTable()
    dec_table.import_from_json('./Data/intensity.json')
    table3 = dec_table.export_table3()
    table4 = dec_table.export_table4()

    df_table3 = show_table(table3)
    df_table3.to_html('Results/table_4.html')
    print(df_table3)
    df_table4 = show_table(table4)
    df_table4.to_html('Results/table_4.html')
    print(df_table4)

    solutions = find_min_covers_exhaustive(dec_table)
    print(solutions)

    table_list = []
    for solution in solutions:
        table_list.append(dec_table.extract_attribute_subset(solution))

    for i in range(len(table_list)):
        table5 = table_list[i].export_table4
        df_table5 = show_table(table5)
        df_table5.to_html(f'Results/table_5_{i+1}.html')

if __name__ == "__main__":
    main()
