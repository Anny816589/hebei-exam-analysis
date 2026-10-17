# -*- coding: utf-8 -*-
"""
explore_2026.py - 2026 岗位表考区分布分析（Day 2）
"""
import os
import pandas as pd

# 用 __file__ 拼绝对路径：不管从哪个目录运行都不会找不到文件
# __file__ = 本文件路径(scripts/explore_2026.py)
# dirname 一次 = scripts/，dirname 两次 = 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', '2026_positions.xlsx')


def load():
    df = pd.read_excel(DATA_PATH, engine='openpyxl', header=1)
    return df


def by_region(df):
    # 新动词 value_counts()：数一列里每个值出现几次，从高到低排
    return df['考区'].value_counts()


def main():
    df = load()
    print('2026 考区分布（岗位数）：')
    print(by_region(df))
    print('合计岗位数：', df.shape[0])


if __name__ == '__main__':
    main()
