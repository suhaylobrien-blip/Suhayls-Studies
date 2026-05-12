"""Generate diagrams used inside the Module 2 summary."""
import matplotlib.pyplot as plt
import matplotlib.patches as mp
import numpy as np
import os

OUT = r"C:\Users\SuhaylO'Brien\OneDrive - BrickField Canvas\Documents\NOVIA ONE\Module 2\diagrams"
os.makedirs(OUT, exist_ok=True)

NAVY  = "#121338"
ORANGE = "#D4471A"
BLUE  = "#2A5DB0"
GREEN = "#1F6E3A"
GREY  = "#888888"
SOFT  = "#EEF0F8"
TINT  = "#FFF3E6"


def save(fig, name, dpi=240):
    p = os.path.join(OUT, name)
    fig.savefig(p, dpi=dpi, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", p)


# 1. Supply & demand curves with equilibrium
def supply_demand():
    fig, ax = plt.subplots(figsize=(6.5, 4.0))
    q = np.linspace(0, 10, 200)
    demand = 10 - 0.8 * q
    supply = 1 + 0.7 * q
    ax.plot(q, demand, color=ORANGE, lw=2.2, label="Demand")
    ax.plot(q, supply, color=BLUE, lw=2.2, label="Supply")

    # Equilibrium intersect — 10 - 0.8q = 1 + 0.7q -> 1.5q = 9 -> q = 6, p = 10 - 4.8 = 5.2
    eq_q, eq_p = 6, 5.2
    ax.scatter([eq_q], [eq_p], color=GREEN, zorder=5, s=70)
    ax.axvline(eq_q, color=GREY, ls=":", lw=1)
    ax.axhline(eq_p, color=GREY, ls=":", lw=1)
    ax.text(eq_q + 0.3, eq_p + 0.4, "Equilibrium\nP* , Q*",
            fontsize=9, fontweight="bold", color=GREEN)

    ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    ax.set_xlabel("Quantity", fontsize=10); ax.set_ylabel("Price", fontsize=10)
    ax.set_xticks([]); ax.set_yticks([])
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#BBBBBB"); ax.spines["bottom"].set_color("#BBBBBB")
    ax.legend(loc="upper right", frameon=False, fontsize=9.5)
    ax.set_title("Supply &  demand intersect at the market-clearing price",
                 fontsize=10.5, color=NAVY, fontweight="bold", pad=10)
    save(fig, "supply_demand.png")


# 2. Business cycle (smooth sine wave with phases)
def business_cycle():
    fig, ax = plt.subplots(figsize=(7.8, 3.6))
    t = np.linspace(0, 4 * np.pi, 400)
    trend = 0.4 * t
    y = trend + 1.3 * np.sin(t)
    ax.plot(t, y, color=NAVY, lw=2.2)
    ax.plot(t, trend, color=GREY, ls="--", lw=1.2, label="Long-term trend")

    # Mark key points
    points = {
        "Trough": (3 * np.pi / 2, 1.3 * np.sin(3 * np.pi / 2) + 0.4 * 3 * np.pi / 2),
        "Peak":  (np.pi / 2,      1.3 * np.sin(np.pi / 2) + 0.4 * np.pi / 2),
    }
    # Add labels for phases
    ax.annotate("Expansion / Recovery", xy=(np.pi / 4 + 0.4, 1.3 * np.sin(np.pi / 4 + 0.4) + 0.4 * (np.pi / 4 + 0.4) + 0.3),
                fontsize=8.5, color=GREEN, fontweight="bold")
    ax.annotate("Contraction / Recession", xy=(np.pi + 0.2, 1.3 * np.sin(np.pi + 0.2) + 0.4 * (np.pi + 0.2) + 0.3),
                fontsize=8.5, color=ORANGE, fontweight="bold")
    ax.annotate("Peak", xy=(np.pi / 2, 1.3 + 0.4 * np.pi / 2), xytext=(np.pi / 2 + 0.2, 2.6),
                fontsize=9.5, color=NAVY, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=GREY))
    ax.annotate("Trough", xy=(3 * np.pi / 2, -1.3 + 0.4 * 3 * np.pi / 2),
                xytext=(3 * np.pi / 2 - 0.3, -0.4),
                fontsize=9.5, color=NAVY, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=GREY))
    ax.annotate("Peak", xy=(5 * np.pi / 2, 1.3 + 0.4 * 5 * np.pi / 2),
                xytext=(5 * np.pi / 2 + 0.1, 6.4),
                fontsize=9.5, color=NAVY, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=GREY))

    ax.set_xlabel("Time", fontsize=10); ax.set_ylabel("Real GDP", fontsize=10)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlim(0, 4 * np.pi + 0.3); ax.set_ylim(-1, 8)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#BBBBBB"); ax.spines["bottom"].set_color("#BBBBBB")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.set_title("The business cycle — fluctuations around long-term potential GDP",
                 fontsize=10.5, color=NAVY, fontweight="bold", pad=8)
    save(fig, "business_cycle.png")


# 3. GDP components — exploded donut/pie
def gdp_components():
    fig, ax = plt.subplots(figsize=(5.8, 4.3))
    labels = ["Consumption (C)", "Investment (I)", "Government (G)", "Net Exports (X-M)"]
    sizes  = [60, 18, 20, 2]
    colors = [ORANGE, BLUE, NAVY, GREEN]
    wedges, _, _ = ax.pie(sizes, labels=labels, colors=colors,
                          autopct="%.0f%%", startangle=90,
                          textprops=dict(fontsize=9, color=NAVY),
                          pctdistance=0.78,
                          wedgeprops=dict(width=0.4, edgecolor="white", linewidth=2))
    ax.text(0, 0, "GDP\nY = C+I+G+(X−M)",
            ha="center", va="center", fontsize=10, fontweight="bold", color=NAVY)
    ax.set_title("Components of GDP (expenditure approach — typical SA mix)",
                 fontsize=10.5, color=NAVY, fontweight="bold", pad=10)
    save(fig, "gdp_components.png")


# 4. Price ceiling vs price floor mini-chart
def price_controls():
    fig, axes = plt.subplots(1, 2, figsize=(8.0, 3.4))
    q = np.linspace(0, 10, 200)
    demand = 10 - 0.8 * q
    supply = 1 + 0.7 * q
    for ax, kind in zip(axes, ["ceiling", "floor"]):
        ax.plot(q, demand, color=ORANGE, lw=2); ax.plot(q, supply, color=BLUE, lw=2)
        ax.set_xlim(0, 10); ax.set_ylim(0, 10)
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_xlabel("Quantity"); ax.set_ylabel("Price")
        ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#BBBBBB"); ax.spines["bottom"].set_color("#BBBBBB")
        if kind == "ceiling":
            ax.axhline(3.5, color=ORANGE, ls="--", lw=1.6)
            ax.text(0.2, 3.7, "Price ceiling (max)", color=ORANGE, fontsize=9, fontweight="bold")
            ax.axvspan(3.6, 8.2, color="#FFEDE0", alpha=0.7)
            ax.text(5.7, 1.1, "Shortage", color=ORANGE, fontsize=10, fontweight="bold")
            ax.set_title("Price ceiling → shortage", fontsize=10.5, color=NAVY, fontweight="bold")
        else:
            ax.axhline(7.5, color=BLUE, ls="--", lw=1.6)
            ax.text(0.2, 7.7, "Price floor (min)", color=BLUE, fontsize=9, fontweight="bold")
            ax.axvspan(1.6, 3.2, color="#E2EAF6", alpha=0.7)
            ax.text(0.4, 8.4, "Surplus", color=BLUE, fontsize=10, fontweight="bold")
            ax.set_title("Price floor → surplus", fontsize=10.5, color=NAVY, fontweight="bold")
    plt.tight_layout()
    save(fig, "price_controls.png")


if __name__ == "__main__":
    supply_demand()
    business_cycle()
    gdp_components()
    price_controls()
