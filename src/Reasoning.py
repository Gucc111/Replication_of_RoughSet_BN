import numpy as np
from .Simplify import *
from .utils import *
from typing import List, Tuple

# 根据指定的列名，将一个 DataFrame 拆分成两个部分
def split_dataframe_by_columns(df: pd.DataFrame, target_columns: List[str]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df_target = df[target_columns]
    df_rest = df.drop(columns=target_columns)
    return df_target, df_rest

# 对一个 DataFrame 沿列方向（axis=1）进行逐行连乘，并返回每一行的乘积结果
def rowwise_product(df: pd.DataFrame) -> pd.Series:
    return df.prod(axis=1)


def reasoning(decision_table: DecisionTable, ab_attr: List[str]) -> Tuple[str, pd.DataFrame]:
    prior_prob = np.array(list(decision_table.fault_prior.values()))
    
    prob_table = show_table(decision_table.export_table3())
    intensity_plus, intensity_minus = split_dataframe_by_columns(prob_table, ab_attr)
    intensity_minus = 1 - intensity_minus

    results = (rowwise_product(intensity_plus) * rowwise_product(intensity_minus) * prior_prob).round(4)
    decision = results.idxmax()

    results = pd.DataFrame([results], index=['Prob'])

    return decision, results
