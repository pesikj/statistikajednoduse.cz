import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib.patches as mpatches
import scipy.stats
from scipy.stats import norm
from tails import Tail
from colour import Color
import numpy as np


def create_critical_region_plot(
    distribution="norm",
    tails=Tail.TWO_TAILED,
    alphas=[
        0.1,
        0.05,
        0.01,
    ],
    x_min=-3,
    y_max=0.5,
):

    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    alphas = sorted(alphas, reverse=True)
    x_max = x_min * (-1)

    red = Color("#f44336")
    colors = list(red.range_to(Color("white"), len(alphas) + 1))
    alphas_with_colors = [(alphas[i], colors[-i - 2]) for i in range(0, len(alphas))]

    x = np.linspace(x_min, x_max, 100)
    y = scipy.stats.norm.pdf(x)
    axis.plot(x, y, color="black")

    def generate_area(x1, x2, color):
        pt1 = x1
        axis.plot([pt1, pt1], [0.0, scipy.stats.norm.pdf(pt1)], color="black")

        pt2 = x2
        axis.plot([pt2, pt2], [0.0, scipy.stats.norm.pdf(pt2)], color="black")

        ptx = np.linspace(pt1, pt2, 10)
        pty = scipy.stats.norm.pdf(ptx)

        axis.fill_between(ptx, pty, color=color, alpha=1.0)

    legend_patches = []
    for alpha, color in alphas_with_colors:
        if tails == Tail.TWO_TAILED:
            generate_area(x_min, norm.ppf(alpha / 2), str(color))
            generate_area(norm.ppf(1 - alpha / 2), x_max, str(color))
        elif tails == Tail.LEFT_TAILED:
            generate_area(x_min, norm.ppf(alpha), str(color))
        elif tails == Tail.RIGHT_TAILED:
            generate_area(norm.ppf(1 - alpha), x_max, str(color))
        legend_patches.append(
            mpatches.Patch(color=str(color), label=r"$\alpha = {:.2f} $".format(alpha))
        )

    axis.legend(handles=legend_patches)

    axis.grid()

    axis.set_xlim(x_min, x_max)
    axis.set_ylim(0, y_max)

    axis.set_title("Kritické obory pro z-test", fontsize=10)
    axis.set_xlabel("x")
    axis.set_ylabel("f(x)")

    return fig
