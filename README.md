# Data Analysis Template

データ処理・解析を行うためのプロジェクトテンプレートリポジトリです。

このリポジトリをテンプレートとして使用することで、統一された開発環境とコーディング規約に基づいたデータ解析プロジェクトを素早く開始できます。

## Table of Contents

- [Features](#features)
- [Directory Structure](#directory-structure)
- [Setup](#setup)
- [Usage](#usage)
- [Development Guidelines](#development-guidelines)
- [Technologies](#technologies)

## Features

- Python 3.12以上を使用したデータ解析環境
- uvによる高速なパッケージ管理
- Polarsを使用した効率的なデータ処理
- Matplotlibによる可視化
- Ruffによる自動フォーマット

## Directory Structure

```
data_analysis/
├── assets/               # 静的ファイル(フォントなど)
│   └── fonts/           # Tex Gyre Termesフォント
├── data/                # 入力データ(実験条件ごとにサブディレクトリを作成)
├── docs/                # ドキュメント(Markdown形式)
├── output/              # 処理結果(実験条件ごとにサブディレクトリを作成)
├── src/                 # メインコード
├── tests/               # テストコード
├── main.py              # エントリーポイント
└── pyproject.toml       # プロジェクト設定
```

## Setup

### Prerequisites

- Python 3.12以上
- [uv](https://github.com/astral-sh/uv) パッケージマネージャー

### Installation

1. このテンプレートから新しいリポジトリを作成

GitHubの「Use this template」ボタンをクリックして新しいリポジトリを作成します。

2. リポジトリをクローン

```bash
git clone <your-repository-url>
cd <your-repository-name>
```

3. 依存関係をインストール

```bash
uv sync
```

## Usage

### Basic Execution

```bash
uv run main.py
```

### Adding Dependencies

通常の依存関係を追加:

```bash
uv add <package-name>
```

開発用の依存関係を追加:

```bash
uv add --dev <package-name>
```

## Development Guidelines

### Code Style

- **型ヒント**: 可能な限り型ヒントを追加すること
  - Python 3.10以降の構文を使用(`list`, `dict`など組み込み型を使用)
- **Import**: ファイル冒頭にまとめること
- **ファイル操作**: `pathlib`を使用し、相対パスを使用すること
- **絵文字**: コードに絵文字を使用しないこと

### Data Processing

- **ライブラリ**: データ解析にはPolarsを使用すること
- **進捗表示**: ループ処理では進捗を表示すること
- **データ管理**: 多数のデータを処理する際は、データごとにディレクトリを分けること

### Visualization

- **ライブラリ**: Matplotlibを使用すること
- **フォント**: Tex Gyre Termes, Times New Romanを使用
- **言語**: グラフのタイトルや軸ラベルは英語を使用
- **必須要素**: タイトル、軸ラベル、凡例を必ず追加
- **レイアウト**: `tight_layout()`を使用
- **メモリ管理**: 連続描画時は`fig.close()`でメモリを解放

### Code Formatting

コード変更後、自動的にフォーマットを実行:

```bash
# フォーマット
uv run ruff format <file>

# Import文の整理
uv run ruff check --fix --select I <file>
```

### Documentation

- **形式**: Markdown形式で作成
- **目次**: 必ず目次を追加
- **保存先**: `docs/`ディレクトリ

### Workflow

- 作業項目が多い場合は段階的に進め、適宜`git commit`を実行
- Semantic Commitを使用

## Technologies

- **Python**: 3.12+
- **Package Manager**: uv
- **Data Processing**: Polars
- **Visualization**: Matplotlib
- **Code Formatting**: Ruff
- **File Operations**: pathlib
