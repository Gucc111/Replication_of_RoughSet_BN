import pandas as pd
import re

# 将 'd1' 'd2' 'd10' 转化为数字(1,2,10), 用于排序
def parse_d_key(d_str: str) -> int:
    # 提取 d 后面的数字
    match = re.match(r"d(\d+)", d_str)
    if match:
        return int(match.group(1))
    else:
        # 如果不符合 d + 数字 的格式, 返回 0 或做其他处理
        return 0

# 将 'm1','m2','m10' 转化为数字(1,2,10) 用于排序
def parse_m_key(m_str: str) -> int:
    match = re.match(r"m(\d+)", m_str)
    if match:
        return int(match.group(1))
    else:
        return 0

# 针对表3或表4的字典数据, 生成一个DataFrame
def show_table(table: dict[str, dict[str, float]]) -> pd.DataFrame:
    # 收集所有行(故障ID)与列(属性名)
    fault_ids = list(table.keys())
    all_attrs = set()
    for _, attr_map in table.items():
        all_attrs.update(attr_map.keys())

    # 分别按照 d? 中数字 & m? 中数字 进行排序
    fault_ids_sorted = sorted(fault_ids, key=parse_d_key)
    attrs_sorted = sorted(all_attrs, key=parse_m_key)

    # 构造 DataFrame
    df = pd.DataFrame(
        index=fault_ids_sorted,
        columns=attrs_sorted
    )
    df = df.fillna(0)  # 缺省填 0

    for d_id, attr_map in table.items():
        for m_id, val in attr_map.items():
            df.loc[d_id, m_id] = val
    
    df.index.name = "Fault_ID"
    
    return df
