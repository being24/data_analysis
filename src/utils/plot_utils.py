"""
Plotting utilities for data visualization
データ可視化のためのユーティリティ関数
"""

from pathlib import Path

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.offsetbox import AnchoredOffsetbox, HPacker, TextArea


def set_xlabel_ja_en_math(
    ax,
    ja: str,
    en_math: str,
    ja_family="Noto Sans JP",
    en_family="TeX Gyre Termes",
    y=-0.12,
):
    fp_ja = FontProperties(family=ja_family)
    fp_en = FontProperties(family=en_family)

    t_ja = TextArea(ja, textprops=dict(fontproperties=fp_ja))
    t_en = TextArea(en_math, textprops=dict(fontproperties=fp_en))

    box = HPacker(children=[t_ja, t_en], align="center", pad=0, sep=0)
    anchored = AnchoredOffsetbox(
        loc="lower center",
        child=box,
        frameon=False,
        pad=0.0,
        borderpad=0.0,
        bbox_to_anchor=(0.5, y),
        bbox_transform=ax.transAxes,
    )

    ax.set_xlabel("")  # 元のxlabelは無効化
    ax.add_artist(anchored)  # 合成ラベルを追加


def setup_matplotlib_fonts(font_size: int = 12) -> None:
    """
    Matplotlibのフォント設定を行う

    Args:
        font_size: グラフ全体で使用するフォントサイズ
    """
    # TeX Gyre Termesフォントを使用(assetsディレクトリに保存されている前提)
    tex_font_path = Path("assets\\fonts\\texgyretermes\\texgyretermes-regular.otf")
    if tex_font_path.exists():
        fm.fontManager.addfont(str(tex_font_path))

    noto_sans_jp_path = Path(
        "assets\\fonts\\Noto_Sans_JP\\NotoSansJP-VariableFont_wght.ttf"
    )
    if noto_sans_jp_path.exists():
        fm.fontManager.addfont(str(noto_sans_jp_path))

    names = {f.name for f in fm.fontManager.ttflist}

    if "TeX Gyre Termes" not in names:
        print("Warning: 'TeX Gyre Termes' font not found. Using default font.")

    if "Noto Sans JP" not in names:
        print("Warning: 'Noto Sans JP' font not found. Using default font.")

    # グラフ全体のフォント設定を一括で適用
    plt.rcParams.update(
        {
            "font.family": [
                "TeX Gyre Termes",
                "Times New Roman",
                "Noto Sans JP",
            ],
            "font.size": font_size,
            "axes.labelsize": font_size,
            "axes.titlesize": font_size,
            "xtick.labelsize": font_size,
            "ytick.labelsize": font_size,
            "legend.fontsize": font_size,
            "mathtext.fontset": "custom",
            "mathtext.rm": "TeX Gyre Termes",
            "mathtext.it": "TeX Gyre Termes:italic",
            "mathtext.bf": "TeX Gyre Termes:bold",
        }
    )
