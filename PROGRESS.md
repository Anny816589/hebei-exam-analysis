# Week 2 开发日志



## Day 1 (2026-10-12)



### 完成
- 启动 PROGRESS.md：记录开发过程


- 环境验证：PATH 上有 4 个 python，目前 `python` 指向 uv cpython-3.11（含 pandas，可用）

- first\_look.py：2026 岗位表基础勘查（shape 6487×11，缺失 2585）

- first\_look\_v2.py：三年汇总（2024=6372/2413、2025=7143/3190、2026=6487/2585）

-### 待办
- ~~`git push -u origin main` 等 GitHub 网络恢复~~ ✅ 2026-10-17 19:01 完成，SSH 方案
  远端：git@github.com:Anny816589/hebei-exam-analysis.git


### 踩坑

- 2026 xlsx 第 0 行是免责声明，必须 `header=1`；2024 是 .xls 老格式，必须 `engine='xlrd'`

- 重要数字必须文本复制粘贴，截图 OCR 两次失真

- 多个 python 共存 + cwd 切换时，先 `pwd` 再写路径



### 明天 Day 2

- 2026 深入：考区分布、学历要求、招录人数

- 启动 PROBLEMS.md：固化 4 个 python 解释器问题
## Day 2 (2026-10-16)

### 今日目标
- PROBLEMS.md 启动
- scripts/explore_2026.py 三大分析

### 完成
- PROBLEMS.md 启动：沉淀 P001-P006 系统性陷阱
- explore_2026.py：考区分布跑通，15 个考区，合计 6487 ✓
- 工具切换：Git Bash `python` 实测 = hermes venv（全套包），PyCharm 解释器已指向它

### 踩坑
- PyCharm 里 uv cpython-3.11 无 pandas（只有 pip/setuptools），必须选 hermes venv
- PyCharm 工作目录默认是项目根，`'../data/'` 会指向错路径 → 新脚本改用 `__file__` 拼绝对路径
- README.md 等 .md 是 GBK 编码，PyCharm 默认 UTF-8 读会乱码 → 重新加载(GBK)后再转 UTF-8


## Day 3 (2026-10-18)

### 今日目标
- 学历要求分布
- 招录人数求和（groupby）
- 交叉分析：保定+石家庄的本科岗（选做）

### 完成
（待填）

### 踩坑
（待填）

