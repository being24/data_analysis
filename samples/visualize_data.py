"""
Data visualization examples
様々なグラフの描画例
"""

import sys
from pathlib import Path
import polars as pl
import matplotlib.pyplot as plt

# プロジェクトルートをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.plot_utils import setup_matplotlib_fonts

FONT_SIZE = 12

# フォント設定の適用
setup_matplotlib_fonts(FONT_SIZE)

# 出力先ディレクトリの作成
output_dir = Path("output/sample")
output_dir.mkdir(parents=True, exist_ok=True)

# データの読み込み
# pathlibのPathオブジェクトは文字列に変換して使用
data_path = Path("data/sample_TimeSeriesResult_20251120185837186.csv")
df = pl.read_csv(data_path)

print(f"Loaded data from {data_path}")
print(f"Data shape: {df.shape}")
print(f"Columns: {df.columns}")

# データの前処理
# 年度から「年」という文字を削除して整数に変換
df = df.with_columns(pl.col("時点").str.replace("年", "").cast(pl.Int32).alias("year"))

print(f"First few rows:\n{df.head()}")


# 1. Line Plot (折れ線グラフ)
# 時系列データの可視化に最適
print("1. Creating line plot for time series data...")

fig, ax = plt.subplots(figsize=(12, 6))

# 年度順にソートしてから描画
df_sorted = df.sort("year")

ax.plot(
    df_sorted["year"],  # x軸データ
    df_sorted["大学・大学院生【人】"],  # y軸データ
    linewidth=2,  # 線の太さを2に設定
    color="#2C3E50",  # 色をダークブルーに変更
    marker="o",  # データポイントにマーカーを表示
    markersize=3,  # マーカーのサイズを3に設定
    alpha=0.8,  # 線の透明度を0.8に設定
)

ax.set_xlabel("Year")
ax.set_ylabel("Number of University Students")
ax.set_title("University and Graduate Students in Kanagawa Prefecture (1975-2023)")
ax.grid(True, alpha=0.3)

# X軸の目盛りを調整(5年ごとに表示)
ax.set_xticks(range(1975, 2024, 5))

plt.tight_layout()  # レイアウトの自動調整
plt.savefig(output_dir / "timeseries_line_plot.svg", format="svg")
plt.close(fig)  # メモリ解放のため明示的にクローズ

print(f"  Saved: {output_dir / 'timeseries_line_plot.svg'}")


# 2. Scatter Plot (散布図)
# データポイントの詳細な分布を確認
print("2. Creating scatter plot...")

fig, ax = plt.subplots(figsize=(12, 6))

ax.scatter(
    df["year"],
    df["大学・大学院生【人】"],
    color="#E74C3C",
    alpha=0.6,
    s=50,  # マーカーサイズ
    edgecolors="black",
    linewidths=0.5,
)

ax.set_xlabel("Year")
ax.set_ylabel("Number of University Students")
ax.set_title("University and Graduate Students Distribution")
ax.grid(True, alpha=0.3)
ax.set_xticks(range(1975, 2024, 5))

plt.tight_layout()
plt.savefig(output_dir / "timeseries_scatter_plot.svg", format="svg")
plt.close(fig)

print(f"  Saved: {output_dir / 'timeseries_scatter_plot.svg'}")


# 3. Bar Plot (棒グラフ)
# 10年ごとのデータを比較
print("3. Creating bar plot for decade comparison...")

fig, ax = plt.subplots(figsize=(10, 6))

# 10年ごとのデータを抽出(1980, 1990, 2000, 2010, 2020年)
decade_years = [1980, 1990, 2000, 2010, 2020]
decade_data = df.filter(pl.col("year").is_in(decade_years)).sort("year")

colors_decade = ["#3498DB", "#2ECC71", "#F39C12", "#9B59B6", "#E74C3C"]

ax.bar(
    decade_data["year"].cast(str),
    decade_data["大学・大学院生【人】"],
    color=colors_decade,
    alpha=0.7,
    edgecolor="black",
)

ax.set_xlabel("Year")
ax.set_ylabel("Number of University Students")
ax.set_title("University Students by Decade")
ax.grid(True, axis="y", alpha=0.3)

# Y軸の値をカンマ区切りで表示
ax.yaxis.set_major_formatter(
    plt.matplotlib.ticker.FuncFormatter(lambda x, p: f"{int(x):,}")
)

plt.tight_layout()
plt.savefig(output_dir / "decade_bar_plot.svg", format="svg")
plt.close(fig)

print(f"  Saved: {output_dir / 'decade_bar_plot.svg'}")


# 4. Box Plot (箱ひげ図)
# 10年区切りでデータの分布を比較
print("4. Creating box plot for decade distribution...")

fig, ax = plt.subplots(figsize=(10, 6))

# 10年区切りのカテゴリを作成
df_with_decade = df.with_columns(((pl.col("year") // 10) * 10).alias("decade"))

# 各年代のデータを準備
decades = sorted(df_with_decade["decade"].unique().to_list())
data_by_decade = [
    df_with_decade.filter(pl.col("decade") == decade)["大学・大学院生【人】"].to_list()
    for decade in decades
]

bp = ax.boxplot(
    data_by_decade,
    tick_labels=[f"{int(d)}s" for d in decades],
    patch_artist=True,
    widths=0.6,
)

# ボックスに色を付ける
for patch, color in zip(
    bp["boxes"], ["#3498DB", "#2ECC71", "#F39C12", "#9B59B6", "#E74C3C"]
):
    patch.set_facecolor(color)
    patch.set_alpha(0.6)

ax.set_xlabel("Decade")
ax.set_ylabel("Number of University Students")
ax.set_title("Distribution of University Students by Decade")
ax.grid(True, axis="y", alpha=0.3)
ax.yaxis.set_major_formatter(
    plt.matplotlib.ticker.FuncFormatter(lambda x, p: f"{int(x):,}")
)

plt.tight_layout()
plt.savefig(output_dir / "decade_box_plot.svg", format="svg")
plt.close(fig)

print(f"  Saved: {output_dir / 'decade_box_plot.svg'}")


# 5. Multiple Subplots (複数グラフの配置)
# 複数の視点からデータを分析
print("5. Creating comprehensive analysis with multiple plots...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 左上: 折れ線グラフ(全期間)
df_sorted = df.sort("year")
axes[0, 0].plot(
    df_sorted["year"],
    df_sorted["大学・大学院生【人】"],
    linewidth=2,
    color="#2C3E50",
    marker="o",
    markersize=2,
)
axes[0, 0].set_xlabel("Year")
axes[0, 0].set_ylabel("Number of Students")
axes[0, 0].set_title("Time Series (1975-2023)")
axes[0, 0].grid(True, alpha=0.3)
axes[0, 0].set_xticks(range(1975, 2024, 10))

# 右上: 10年ごとの棒グラフ
axes[0, 1].bar(
    decade_data["year"].cast(str),
    decade_data["大学・大学院生【人】"],
    color=colors_decade,
    alpha=0.7,
    edgecolor="black",
)
axes[0, 1].set_xlabel("Year")
axes[0, 1].set_ylabel("Number of Students")
axes[0, 1].set_title("Decade Comparison")
axes[0, 1].grid(True, axis="y", alpha=0.3)
axes[0, 1].yaxis.set_major_formatter(
    plt.matplotlib.ticker.FuncFormatter(lambda x, p: f"{int(x):,}")
)

# 左下: 箱ひげ図
bp = axes[1, 0].boxplot(
    data_by_decade,
    tick_labels=[f"{int(d)}s" for d in decades],
    patch_artist=True,
    widths=0.6,
)
for patch, color in zip(
    bp["boxes"], ["#3498DB", "#2ECC71", "#F39C12", "#9B59B6", "#E74C3C"]
):
    patch.set_facecolor(color)
    patch.set_alpha(0.6)
axes[1, 0].set_xlabel("Decade")
axes[1, 0].set_ylabel("Number of Students")
axes[1, 0].set_title("Distribution by Decade")
axes[1, 0].grid(True, axis="y", alpha=0.3)
axes[1, 0].yaxis.set_major_formatter(
    plt.matplotlib.ticker.FuncFormatter(lambda x, p: f"{int(x):,}")
)

# 右下: 散布図
axes[1, 1].scatter(
    df["year"],
    df["大学・大学院生【人】"],
    color="#E74C3C",
    alpha=0.6,
    s=30,
    edgecolors="black",
    linewidths=0.5,
)
axes[1, 1].set_xlabel("Year")
axes[1, 1].set_ylabel("Number of Students")
axes[1, 1].set_title("Scatter Plot")
axes[1, 1].grid(True, alpha=0.3)
axes[1, 1].set_xticks(range(1975, 2024, 10))

plt.tight_layout()
plt.savefig(output_dir / "comprehensive_analysis.svg", format="svg")
plt.close(fig)

print(f"  Saved: {output_dir / 'comprehensive_analysis.svg'}")

print("All plots have been saved successfully!")
