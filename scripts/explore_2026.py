# -*- coding: utf-8 -*-
"""
explore_2026.py - 2026 岗位表分析
Day 2: 考区分布
Day 3: 学历要求分布 + 招录人数求和
"""
import os
import pandas as pd

# 用 __file__ 拼绝对路径，不管从哪个目录运行都找得到文件
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', '2026_positions.xlsx')


def load():
    # 2026 第 0 行是免责声明，必须 header=1
    df = pd.read_excel(DATA_PATH, engine='openpyxl', header=1)
    return df


def by_region(df):
    # 数岗位个数：一列里每个值出现几次
    return df['考区'].value_counts()


def by_education(df):
    # 学历要求分布。政府表常有"本科及以上""仅限本科"等变体，先看原始值
    return df['学历低限'].value_counts()


def by_recruitment(df):
    # 按考区分组，只对"招录人数"这一列求和，再降序排
    return df.groupby('考区')['招录人数'].sum().sort_values(ascending=False)


def main():
    df = load()

    print('=== 1. 各考区岗位数 ===')
    print(by_region(df))
    print('合计岗位数：', df.shape[0])

    print()
    print('=== 2. 学历要求分布 ===')
    print(by_education(df))

    print()
    print('=== 3. 各考区招录人数 ===')
    print(by_recruitment(df))
    print('全省招录总数：', df['招录人数'].sum())


if __name__ == '__main__':
    main()
