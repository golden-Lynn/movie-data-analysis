# 电影数据采集与可视化分析

基于 TMDB 高分电影榜单，用 Python 完成「数据采集 → 数据清洗 → 统计分析 → 可视化出图」的完整链路。

> 数据来源：TMDB（themoviedb.org）公开榜单，仅用于技术学习。

## 项目效果

![电影数据分析四联图](Start/Pic/movie_analysis.png)

## 实现功能

- **数据采集**：爬取 TMDB 高分榜前 100 部电影，抓取片名、评分、年份、上映日期、时长、语言、标签共 7 个字段
- **数据清洗**：缺失值填充、日期格式提取、时长换算为分钟、异常值归类
- **统计分析**：按年份、语言、标签、评分四个维度做分布统计
- **可视化**：一张 2×2 画布输出折线图 + 柱状图 ×2 + 饼图，并自动保存为图片

## 技术栈

| 用途 | 库 |
|---|---|
| 网络请求 | requests |
| 页面解析 | lxml |
| 数据清洗与分析 | pandas |
| 数据可视化 | matplotlib |

## 目录结构

```
.
├── spider.py            # 数据采集（爬虫）
├── movie_analyze_n.py   # 数据清洗 + 可视化（函数式封装）
├── test.ipynb           # 分析过程的 Jupyter 探索记录
├── csv_file/
│   └── All_movies.csv   # 采集到的原始数据（100 条）
├── Start/Pic/
│   └── movie_analysis.png  # 输出的分析图
├── requirements.txt
└── README.md
```

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 直接出图（数据已附带在仓库中，无需先爬取）
python movie_analyze_n.py
```

生成的图片保存在 `Start/Pic/movie_analysis.png`。

如需重新采集数据，先运行：

```bash
python spider.py
```

> 注意：`spider.py` 需要能访问 themoviedb.org。若网络不通，可直接用仓库中已附带的 `csv_file/All_movies.csv` 进行后续分析。

## 代码结构说明

`movie_analyze_n.py` 采用函数式拆分，各模块职责单一：

| 函数 | 职责 |
|---|---|
| `load_data()` | 读取 CSV 并统一做缺失值与格式预处理 |
| `count_tags()` | 统计每个电影标签出现的次数 |
| `plot_year()` | 每年高分电影数量折线图 |
| `plot_language()` | 电影语言分布柱状图 |
| `plot_tags()` | 电影标签分布柱状图 |
| `plot_rate()` | 评分占比饼图（占比过小的评分区间合并为「其他」） |
| `main()` | 创建 2×2 画布，依次调用上述绘图函数并保存 |

## 开发中遇到的问题与解决

- **字典计数时键不存在**：直接用 `d[k] += 1` 会抛 `KeyError`，需要先判断键是否存在，或改用 `d.get(k, 0) + 1`
- **pandas 3 的 Copy-on-Write**：`df[col].fillna(x, inplace=True)` 不再生效，必须写成 `df[col] = df[col].fillna(x)`
- **多值字段的统计**：「电影标签」一个单元格内含多个用逗号分隔的标签，需先 `str.split(",")` 再遍历计数，否则统计到的是标签组合而非单个标签
- **饼图标签过多**：占比低于 3% 的评分区间合并为「其他」，避免饼图被切得太碎

## 待优化

- 柱状图标签数量较多时未做旋转或筛选
