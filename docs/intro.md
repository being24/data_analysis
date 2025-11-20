# Python Data Analysis Introduction

## Table of Contents

1. [Python入門](#python入門)
2. [開発環境のセットアップ](#開発環境のセットアップ)
3. [サンプルプログラム](#サンプルプログラム)
4. [実践例題](#実践例題)

## Python入門

### Google Colabで学ぶPython

Pythonの基本文法を学ぶには、以下のリソースを推奨します:

- **Python Boot Camp**: [https://www.python.jp/train/index.html](https://www.python.jp/train/index.html)
  - Google Colabを使ってブラウザ上でPythonを学習できます
  - 環境構築不要で、すぐに始められます
  - 基本的な文法から学べる初心者向けコンテンツです

### 教科書

より体系的に学びたい方には、以下の教科書を推奨します:

- **京都大学 全学共通科目「プログラミング演習(Python)」**: [https://repository.kulib.kyoto-u.ac.jp/dspace/handle/2433/245698](https://repository.kulib.kyoto-u.ac.jp/dspace/handle/2433/245698)
  - 大学の授業で使用されている教材です
  - Pythonの基礎から応用まで体系的に学べます

## 開発環境のセットアップ

### uvのインストール

以下のURLを参考に、uvをインストールしてください:

```plaintext
https://docs.astral.sh/uv/getting-started/installation/
```

Windowsの場合、PowerShellを管理者権限で開き、以下のコマンドを実行して実行ポリシーを設定します:

```powershell
Set-ExecutionPolicy RemoteSigned
```

### gitのインストール

以下のURLを参考に、gitをインストールしてください:

```plaintext
https://git-scm.com/book/ja/v2/%E4%BD%BF%E3%81%84%E5%A7%8B%E3%82%81%E3%82%8B-Git%E3%81%AE%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB
```

### VSCodeのインストール

以下のURLを参考に、Visual Studio Codeをインストールしてください:

```plaintext
https://code.visualstudio.com/download
```

### プロジェクトのセットアップ

1. 以下のURLを開きます:

```plaintext
https://github.com/being24/data_analysis
```

1. 右上の「Code」ボタンをクリックし、「Download ZIP」を選択してプロジェクトをダウンロードします。

2. VSCodeでプロジェクトディレクトリを開きます。

3. 依存パッケージをインストールします:

```powershell
uv sync
```

## サンプルプログラム

### 基本的なデータ可視化

以下のサンプルプログラムでは、CSVファイルからデータを読み込み、様々なグラフを描画してSVG形式で保存する方法を説明します。

#### サンプルデータについて

このチュートリアルでは、神奈川県の大学・大学院生数の時系列データ(1975年〜2023年)を使用します。

データは `data/sample_TimeSeriesResult_20251120185837186.csv` に保存されており、以下のような構造になっています:

```csv
時点,地域コード,地域,大学・大学院生【人】,注記
1975年,14000,神奈川県,49549,
1976年,14000,神奈川県,52355,
...
```

各列の意味:

- `時点`: 年度
- `地域コード`: 地域を識別するコード
- `地域`: 都道府県名
- `大学・大学院生【人】`: その年の大学・大学院生数
- `注記`: 追加情報(通常は空)

#### データの読み込みと可視化

次に、CSVデータを読み込み、様々な種類のグラフを描画します:

```python
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
    df_sorted["year"], # x軸データ
    df_sorted["大学・大学院生【人】"], # y軸データ
    linewidth=2, # 線の太さを2に設定
    color="#2C3E50", # 色をダークブルーに変更
    marker="o",  # データポイントにマーカーを表示
    markersize=3, # マーカーのサイズを3に設定
    alpha=0.8, # 線の透明度を0.8に設定
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
```

### プログラムの実行方法

可視化スクリプトを実行します:

```powershell
uv run python samples/visualize_data.py
```

生成されたSVGファイルは`output/sample/`ディレクトリに保存されます。

### コードの重要なポイント

#### Polarsの使用

```python
import polars as pl

# CSVファイルの読み込み
df = pl.read_csv("data/sample_TimeSeriesResult_20251120185837186.csv")

# データのフィルタリング
# 特定の年のデータのみを抽出
subset = df.filter(pl.col("year").is_in([1980, 1990, 2000]))

# 文字列の処理と型変換
# "1975年" → 1975 (整数)
df = df.with_columns(
    pl.col("時点").str.replace("年", "").cast(pl.Int32).alias("year")
)

# グループ化と集計
# 10年区切りでグループ化して統計量を計算
df_with_decade = df.with_columns(
    ((pl.col("year") // 10) * 10).alias("decade")
)
result = df_with_decade.group_by("decade").agg(
    pl.col("大学・大学院生【人】").mean().alias("average"),
    pl.col("大学・大学院生【人】").min().alias("minimum"),
    pl.col("大学・大学院生【人】").max().alias("maximum"),
)

# CSVファイルへの書き込み
df.write_csv("output.csv")
```

Polarsは、pandasよりも高速で効率的なデータ処理が可能です。特に大規模データセットでその効果が顕著です。

#### pathlibの使用

```python
from pathlib import Path

# パスの作成(OSに依存しない)
data_dir = Path("data/sample")

# ディレクトリの作成
data_dir.mkdir(parents=True, exist_ok=True)

# ファイルパスの結合
file_path = data_dir / "sample_data.csv"

# ファイルの存在確認
if file_path.exists():
    print("File exists")
```

pathlibを使うことで、Windows・macOS・Linux間でのパス表記の違いを気にする必要がなくなります。

#### Matplotlibのフォント設定

フォント設定は共通ユーティリティとして `src/utils/plot_utils.py` に定義されています:

```python
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


def setup_matplotlib_fonts(font_size: int = 12) -> None:
    """
    Matplotlibのフォント設定を行う

    Args:
        font_size: グラフ全体で使用するフォントサイズ
    """
    # TeX Gyre Termesフォントを使用(assetsディレクトリに保存されている前提)
    font_path = Path("assets/fonts/texgyretermes-regular.otf")
    if font_path.exists():
        fm.fontManager.addfont(str(font_path))

    # グラフ全体のフォント設定を一括で適用
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["TeX Gyre Termes", "Times New Roman"],
            "font.size": font_size,
            "axes.labelsize": font_size,
            "axes.titlesize": font_size,
            "xtick.labelsize": font_size,
            "ytick.labelsize": font_size,
            "legend.fontsize": font_size,
            "mathtext.fontset": "stix",
            "mathtext.rm": "serif",
        }
    )
```

スクリプトでの使用方法:

```python
from src.utils.plot_utils import setup_matplotlib_fonts

# フォント設定を適用
setup_matplotlib_fonts(font_size=12)
```

この関数を使うことで、すべてのスクリプトで統一されたフォント設定を簡単に適用できます。

#### 時系列データの扱い

```python
# データのソート
df_sorted = df.sort("year")

# X軸の目盛りを調整
ax.set_xticks(range(1975, 2024, 5))  # 5年ごとに表示

# Y軸の値をカンマ区切りで表示
ax.yaxis.set_major_formatter(
    plt.matplotlib.ticker.FuncFormatter(lambda x, p: f'{int(x):,}')
)
```

時系列データを扱う際は、データを年代順にソートし、軸の目盛りを適切に設定することで見やすいグラフになります。

#### SVGでの保存

```python
plt.savefig("output/plot.svg", format="svg")
```

SVG形式で保存することで、拡大縮小しても画質が劣化しないベクター画像として保存できます。論文やプレゼンテーションに適しています。

## 実践例題

### 例題1: 期間ごとの成長率分析

サンプルデータを使って、各年代(1970年代、1980年代など)の大学生数の変化率を分析してみましょう。

**課題:**

1. 各年代の最初の年と最後の年のデータを抽出する
2. 年代ごとの増加率を計算する
3. 棒グラフで年代ごとの成長率を可視化する
4. SVG形式で保存する

**ヒント:**

```python
# 各年代の最初と最後の年を取得
df_with_decade = df.with_columns(
    ((pl.col("year") // 10) * 10).alias("decade")
)

# 各年代の最小年と最大年のデータを取得
decade_stats = df_with_decade.group_by("decade").agg([
    pl.col("year").min().alias("start_year"),
    pl.col("year").max().alias("end_year"),
])
```

### 例題2: トレンドラインの追加

時系列データに近似直線を追加して、全体的な傾向を視覚化してみましょう。

**課題:**

1. CSVファイルを読み込む
2. 元のデータを折れ線グラフで描画する
3. NumPyの`polyfit`を使って1次近似(線形回帰)を計算する
4. 近似直線を元のグラフに重ねて表示する
5. SVG形式で保存する

**解答例:**

```python
import sys
from pathlib import Path
import polars as pl
import matplotlib.pyplot as plt
import numpy as np

# プロジェクトルートをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.plot_utils import setup_matplotlib_fonts

# フォント設定
setup_matplotlib_fonts()

# データの読み込みと前処理
data_path = Path("data/sample_TimeSeriesResult_20251120185837186.csv")
df = pl.read_csv(data_path)
df = df.with_columns(
    pl.col("時点").str.replace("年", "").cast(pl.Int32).alias("year")
)

# データを取得
years = df["year"].to_numpy()
students = df["大学・大学院生【人】"].to_numpy()

# 1次近似(線形回帰)
coefficients = np.polyfit(years, students, 1)
trend_line = np.poly1d(coefficients)

# グラフの作成
fig, ax = plt.subplots(figsize=(12, 6))

# 元のデータをプロット
ax.plot(years, students, linewidth=2, color="#2C3E50",
        marker="o", markersize=3, label="Actual Data", alpha=0.7)

# トレンドラインを追加
ax.plot(years, trend_line(years), linewidth=2, color="#E74C3C",
        linestyle="--", label="Trend Line", alpha=0.8)

ax.set_xlabel("Year")
ax.set_ylabel("Number of University Students")
ax.set_title("University Students with Trend Line")
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_xticks(range(1975, 2024, 5))

plt.tight_layout()
plt.savefig("output/trend_analysis.svg", format="svg")
plt.close(fig)

print(f"Trend equation: y = {coefficients[0]:.2f}x + {coefficients[1]:.2f}")
```

### 例題3: 統計サマリーの作成とファイル出力

データの基本統計量を計算し、結果をテキストファイルとCSVファイルに出力してみましょう。

**課題:**

1. 年代ごとにデータをグループ化する
2. 各年代の平均値、中央値、標準偏差、最大値、最小値を計算する
3. 結果をCSVファイルに保存する
4. 読みやすい形式でテキストファイルにも保存する

**解答例:**

```python
from pathlib import Path
import polars as pl

# データの読み込みと前処理
data_path = Path("data/sample_TimeSeriesResult_20251120185837186.csv")
df = pl.read_csv(data_path)
df = df.with_columns(
    pl.col("時点").str.replace("年", "").cast(pl.Int32).alias("year")
)

# 年代ごとの統計量を計算
df_with_decade = df.with_columns(
    ((pl.col("year") // 10) * 10).alias("decade")
)

stats = df_with_decade.group_by("decade").agg([
    pl.col("大学・大学院生【人】").mean().alias("average"),
    pl.col("大学・大学院生【人】").median().alias("median"),
    pl.col("大学・大学院生【人】").std().alias("std_dev"),
    pl.col("大学・大学院生【人】").min().alias("minimum"),
    pl.col("大学・大学院生【人】").max().alias("maximum"),
    pl.col("大学・大学院生【人】").count().alias("count"),
]).sort("decade")

# 出力ディレクトリの作成
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

# CSVファイルに保存
stats.write_csv(output_dir / "decade_statistics.csv")
print(f"Statistics saved to {output_dir / 'decade_statistics.csv'}")

# テキストファイルに整形して保存
with open(output_dir / "decade_statistics.txt", "w", encoding="utf-8") as f:
    f.write("University Students Statistics by Decade\n")
    f.write("=" * 80 + "\n\n")
    
    for row in stats.iter_rows(named=True):
        f.write(f"Decade: {int(row['decade'])}s\n")
        f.write(f"  Count:      {int(row['count'])}\n")
        f.write(f"  Average:    {row['average']:,.2f}\n")
        f.write(f"  Median:     {row['median']:,.2f}\n")
        f.write(f"  Std Dev:    {row['std_dev']:,.2f}\n")
        f.write(f"  Minimum:    {int(row['minimum']):,}\n")
        f.write(f"  Maximum:    {int(row['maximum']):,}\n")
        f.write("\n")

print(f"Formatted statistics saved to {output_dir / 'decade_statistics.txt'}")
print("\nStatistics summary:")
print(stats)
```

### 発展課題

1. **移動平均の追加**: 5年移動平均を計算してグラフに追加し、短期的な変動を平滑化する
2. **年代間比較**: 異なる年代間での学生数の差を可視化する
3. **予測モデル**: 過去のデータから将来の学生数を予測する簡単なモデルを作成する
4. **複数地域の比較**: 他の都道府県のデータを追加し、地域間で比較する

## まとめ

このドキュメントでは、以下の内容を学びました:

1. Python学習のためのリソース
2. uvを使った開発環境のセットアップ
3. Polarsを使った時系列データの読み込みと操作
4. Matplotlibを使った様々なグラフの描画
   - 折れ線グラフ(時系列データ)
   - 散布図
   - 棒グラフ(年代比較)
   - 箱ひげ図(分布の可視化)
   - 複数グラフの配置
5. SVG形式でのグラフ保存
6. 統計量の計算とファイル出力

これらの基礎を身につけることで、実際のデータ分析の第一歩を踏み出すことができます。

### 次のステップ

- より高度なデータ処理手法(結合、ピボット、ウィンドウ関数など)
- 統計分析の基礎
- 機械学習への入門
- インタラクティブな可視化(Plotlyなど)

### 参考リンク

- [Polars公式ドキュメント](https://pola-rs.github.io/polars/)
- [Matplotlib公式ドキュメント](https://matplotlib.org/)
- [Python公式ドキュメント](https://docs.python.org/ja/3/)
