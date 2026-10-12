# -*- coding: utf-8 -*-
"""
first_look_v2.py - 三年岗位表汇总
================================
读 2024/2025/2026 三张表，输出每年的 rows/cols/total_null 三行表。
"""
import pandas as pd


def load_year(year):
    # 根据年份选 engine（2024 用 xlrd，其余 openpyxl）和 header（2026 用 1，其余 0）
    if year == 2024:
        return pd.read_excel('../data/2024_positions.xls', engine='xlrd', header=0)
    elif year == 2025:
        return pd.read_excel('../data/2025_positions.xlsx', engine='openpyxl', header=0)
    elif year == 2026:
        return pd.read_excel('../data/2026_positions.xlsx', engine='openpyxl', header=1)
    else:
        raise ValueError(f'不支持的年份: {year}')


def summarize(df, year):
    # 返回字典，main 会汇总成表格
    return {
        'year': year,
        'rows': df.shape[0],
        'cols': df.shape[1],
        'total_null': int(df.isnull().sum().sum()),
    }


def main():
    rows = [summarize(load_year(y), y) for y in (2024, 2025, 2026)]
    print(pd.DataFrame(rows).to_string(index=False))


if __name__ == '__main__':
    main()
