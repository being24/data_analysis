"""
Plotting utilities for data visualization
データ可視化のためのユーティリティ関数
"""

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
