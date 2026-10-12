
import pandas as pd

df = pd.read_excel('../data/2026_positions.xlsx',header=1)

print('=== 基本信息 ===')
print('行数 x 列数:', df.shape)
print()

print('=== 列名清单 ===')
for i, col in enumerate(df.columns):
    print(f'{i+1}. {col} (类型: {df[col].dtype})')
print()

print('=== 前 3 行预览 ===')
print(df.head(3))
print()

print('=== 各列缺失值数量 ===')
print(df.isnull().sum())
