# -*- coding: utf-8 -*-
"""pool_by_year.py - 用同一套口径跑 2024 / 2025 / 2026，看我的可用池趋势

复用 explore_2026.my_pool。
注意：三年的表头行不同（2026 第 0 行是免责声明），文件后缀不同
（2024 是 .xls，要 xlrd），这些差异都写在 YEARS 里。
"""
import os
import pandas as pd

from explore_2026 import my_pool

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 年份 -> (文件名, 引擎, 表头行)
YEARS = {
    2024: ('2024_positions.xls', 'xlrd', 0),
    2025: ('2025_positions.xlsx', 'openpyxl', 0),
    2026: ('2026_positions.xlsx', 'openpyxl', 1),
}


def load(year):
    fname, engine, header = YEARS[year]
    df = pd.read_excel(os.path.join(BASE_DIR, 'data', fname),
                       engine=engine, header=header)
    # 2024 写作「雄安新区（保定）」，统一后才能跨年比
    df['考区'] = df['考区'].str.replace('雄安新区（保定）', '雄安新区', regex=False)
    return df


def check_hukou_wording(year, df):
    """户籍措辞检查。

    my_pool 里的户籍判定写死了「张家口市所辖|阳原县」，这是照 2026 的措辞写的。
    别的年份如果换写法，我的阳原身份就识别不出来，会静默丢岗。
    所以每年都要先看原文，再决定要不要改判定词。
    """
    req = df['其他要求'].fillna('')
    hk = req[req.str.contains('户籍|生源')]
    hit = hk[hk.str.contains('张家口|阳原')]
    print('  户籍岗全省 %d 个，其中涉张家口/阳原 %d 个' % (hk.shape[0], hit.shape[0]))
    print(hit.value_counts().to_string())
    print()


def main():
    for year in sorted(YEARS):
        df = load(year)
        print('=' * 55)
        print(year, '| 全省岗位', df.shape[0], '| 招录', df['招录人数'].sum())
        check_hukou_wording(year, df)
        pool, favor = my_pool(df, as_fresh=True)
        print('  → 可用池 %d 个岗位，%d 人，平均每岗 %.2f 人'
              % (pool.shape[0], pool['招录人数'].sum(),
                 pool['招录人数'].sum() / pool.shape[0]))
        print()


if __name__ == '__main__':
    main()
