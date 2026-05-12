"""Generate diagrams used inside the Module 3 summary."""
import matplotlib.pyplot as plt
import matplotlib.patches as mp
import os

OUT = r"C:\Users\SuhaylO'Brien\OneDrive - BrickField Canvas\Documents\NOVIA ONE\Module 3\diagrams"
os.makedirs(OUT, exist_ok=True)

NAVY  = "#121338"
ORANGE = "#D4471A"
WHITE = "#FFFFFF"
SOFT  = "#EEF0F8"
GREY  = "#888888"
GREEN = "#1F6E3A"


def save(fig, name, dpi=240):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", path)


# ===================== 1. Twin Peaks structure =====================
def twin_peaks():
    fig, ax = plt.subplots(figsize=(7.8, 4.2))
    ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")

    # Top: National Treasury / Minister of Finance
    top = mp.FancyBboxPatch((2.0, 4.9), 6.0, 0.9,
        boxstyle="round,pad=0.04", linewidth=0, facecolor=NAVY)
    ax.add_patch(top)
    ax.text(5, 5.35, "Minister of Finance / National Treasury",
            ha="center", va="center", color="white",
            fontsize=10.5, fontweight="bold")

    # Two peaks
    pa = mp.FancyBboxPatch((0.4, 2.4), 4.0, 1.6,
        boxstyle="round,pad=0.04", linewidth=0, facecolor=ORANGE)
    ax.add_patch(pa)
    ax.text(2.4, 3.55, "PRUDENTIAL AUTHORITY",
            ha="center", va="center", color="white", fontsize=10.5, fontweight="bold")
    ax.text(2.4, 3.05, "(within SARB)",
            ha="center", va="center", color="white", fontsize=9, style="italic")
    ax.text(2.4, 2.6, "Safety &  soundness of institutions",
            ha="center", va="center", color="white", fontsize=8.5)

    fs = mp.FancyBboxPatch((5.6, 2.4), 4.0, 1.6,
        boxstyle="round,pad=0.04", linewidth=0, facecolor="#2A5DB0")
    ax.add_patch(fs)
    ax.text(7.6, 3.55, "FSCA",
            ha="center", va="center", color="white", fontsize=10.5, fontweight="bold")
    ax.text(7.6, 3.05, "(Conduct Authority)",
            ha="center", va="center", color="white", fontsize=9, style="italic")
    ax.text(7.6, 2.6, "Market conduct  /  customer fairness",
            ha="center", va="center", color="white", fontsize=8.5)

    # Connecting lines from top to peaks
    ax.plot([5, 2.4], [4.9, 4.0], color=GREY, lw=1.2)
    ax.plot([5, 7.6], [4.9, 4.0], color=GREY, lw=1.2)

    # Regulated firms below
    firm = mp.FancyBboxPatch((1, 0.4), 8, 1.3,
        boxstyle="round,pad=0.04", linewidth=1.5, edgecolor=NAVY, facecolor=SOFT)
    ax.add_patch(firm)
    ax.text(5, 1.3, "Regulated firms — banks, insurers, asset managers, advisors, exchanges",
            ha="center", va="center", fontsize=9.5, fontweight="bold", color=NAVY)
    ax.text(5, 0.78, "Reports to BOTH peaks: prudential limits AND conduct standards",
            ha="center", va="center", fontsize=8, color=NAVY, style="italic")

    # Arrows down from peaks
    ax.annotate("", xy=(3.0, 1.75), xytext=(2.4, 2.4),
                arrowprops=dict(arrowstyle="->", color=GREY, lw=1.2))
    ax.annotate("", xy=(7.0, 1.75), xytext=(7.6, 2.4),
                arrowprops=dict(arrowstyle="->", color=GREY, lw=1.2))

    ax.set_title("South Africa's Twin Peaks Model (FSRA 9 of 2017, effective 1 April 2018)",
                 fontsize=10.5, color=NAVY, fontweight="bold", pad=10)
    save(fig, "twin_peaks.png")


# ===================== 2. Regulation 28 — horizontal bars =====================
def reg28():
    fig, ax = plt.subplots(figsize=(7.6, 4.0))
    items = [
        ("Equities",                 75),
        ("Foreign assets (offshore)", 45),
        ("Property",                  25),
        ("Hedge funds",               15),
        ("Private equity",            15),
    ]
    labels = [x[0] for x in items][::-1]
    values = [x[1] for x in items][::-1]
    colors = [ORANGE, "#5b7eb8", "#5b7eb8", "#5b7eb8", "#5b7eb8"][::-1]

    bars = ax.barh(labels, values, color=colors, height=0.55)
    ax.set_xlim(0, 100)
    ax.set_xlabel("Maximum % of fund value", fontsize=9)
    ax.set_xticks(range(0, 101, 10))
    ax.grid(axis="x", linestyle=":", alpha=0.4)
    ax.set_axisbelow(True)

    for b, v in zip(bars, values):
        ax.text(v + 1.2, b.get_y() + b.get_height() / 2, f"{v}%",
                va="center", fontsize=9, fontweight="bold", color=NAVY)

    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color("#BBBBBB")
    ax.spines["left"].set_color("#BBBBBB")

    ax.set_title("Regulation 28 of the Pension Funds Act — asset class caps",
                 fontsize=11, color=NAVY, fontweight="bold", pad=10)
    save(fig, "reg28_caps.png")


# ===================== 3. AML hierarchy =====================
def aml():
    fig, ax = plt.subplots(figsize=(7.6, 3.8))
    ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis("off")

    boxes = [
        (2.5, 4.0, 5.0, 0.8, "FATF",
         "Global standard-setter (based in Paris)", ORANGE),
        (2.5, 2.8, 5.0, 0.8, "ESAAMLG",
         "Regional FATF body — Eastern & Southern Africa", "#2A5DB0"),
        (2.5, 1.6, 5.0, 0.8, "FICA",
         "SA national law — FIC Act 38 of 2001", NAVY),
        (2.5, 0.4, 5.0, 0.8, "FIC",
         "Financial Intelligence Centre — SA's AML hub", "#1F6E3A"),
    ]
    cx = 5
    for (x, y, w, h, label, sub, c) in boxes:
        ax.add_patch(mp.FancyBboxPatch((x, y), w, h,
            boxstyle="round,pad=0.04", linewidth=0, facecolor=c))
        ax.text(cx, y + h - 0.18, label, ha="center", va="top",
                color="white", fontsize=11, fontweight="bold")
        ax.text(cx, y + 0.18, sub, ha="center", va="bottom",
                color="white", fontsize=8.5, style="italic")
    # arrows
    for y1, y2 in [(4.0, 3.6), (2.8, 2.4), (1.6, 1.2)]:
        ax.annotate("", xy=(cx, y2), xytext=(cx, y1),
                    arrowprops=dict(arrowstyle="->", color=GREY, lw=1.4))

    ax.text(8.0, 4.40, "International", fontsize=8.5, color=GREY, style="italic")
    ax.text(8.0, 3.20, "Regional",      fontsize=8.5, color=GREY, style="italic")
    ax.text(8.0, 2.00, "National law",  fontsize=8.5, color=GREY, style="italic")
    ax.text(8.0, 0.80, "Implementer",   fontsize=8.5, color=GREY, style="italic")

    ax.set_title("AML / CFT regulatory hierarchy as it lands in South Africa",
                 fontsize=11, color=NAVY, fontweight="bold", pad=8)
    save(fig, "aml_hierarchy.png")


# ===================== 4. SA regulators map =====================
def sa_regulators():
    fig, ax = plt.subplots(figsize=(7.8, 4.6))
    ax.set_xlim(0, 12); ax.set_ylim(0, 8); ax.axis("off")

    # Top: Twin Peaks
    ax.add_patch(mp.FancyBboxPatch((3.5, 6.8), 5, 0.7,
        boxstyle="round,pad=0.04", linewidth=0, facecolor=NAVY))
    ax.text(6, 7.15, "FSRA 2017 — Twin Peaks",
            ha="center", va="center", color="white", fontsize=10, fontweight="bold")

    # Prudential block
    ax.add_patch(mp.FancyBboxPatch((0.4, 4.7), 5.0, 1.6,
        boxstyle="round,pad=0.04", linewidth=0, facecolor=ORANGE))
    ax.text(2.9, 5.95, "PRUDENTIAL AUTHORITY",
            ha="center", va="center", color="white", fontsize=10, fontweight="bold")
    ax.text(2.9, 5.50, "(housed within SARB)",
            ha="center", va="center", color="white", fontsize=8.5, style="italic")
    ax.text(2.9, 5.05, "Banks · Insurers · Market infrastructures",
            ha="center", va="center", color="white", fontsize=8.5)

    # Conduct block
    ax.add_patch(mp.FancyBboxPatch((6.6, 4.7), 5.0, 1.6,
        boxstyle="round,pad=0.04", linewidth=0, facecolor="#2A5DB0"))
    ax.text(9.1, 5.95, "FSCA — CONDUCT",
            ha="center", va="center", color="white", fontsize=10, fontweight="bold")
    ax.text(9.1, 5.50, "(successor to FSB)",
            ha="center", va="center", color="white", fontsize=8.5, style="italic")
    ax.text(9.1, 5.05, "TCF · Market abuse · FSP licensing",
            ha="center", va="center", color="white", fontsize=8.5)

    # Connector lines
    ax.plot([6, 2.9], [6.8, 6.3], color=GREY, lw=1.0)
    ax.plot([6, 9.1], [6.8, 6.3], color=GREY, lw=1.0)

    # Other regulators row
    others = [
        (0.4, 2.6, 2.6, "NCR",   "National Credit Act"),
        (3.2, 2.6, 2.6, "FIC",   "FICA — AML / CFT"),
        (6.0, 2.6, 2.6, "JSE",   "FMA — SRO &  exchange"),
        (8.8, 2.6, 2.6, "Treasury", "PFMA — fiscal &  debt"),
    ]
    for x, y, w, label, sub in others:
        ax.add_patch(mp.FancyBboxPatch((x, y), w, 1.4,
            boxstyle="round,pad=0.04", linewidth=1, edgecolor=NAVY, facecolor=SOFT))
        ax.text(x + w / 2, y + 1.0, label,
                ha="center", va="center", color=NAVY, fontsize=10, fontweight="bold")
        ax.text(x + w / 2, y + 0.4, sub,
                ha="center", va="center", color=NAVY, fontsize=8)

    # Regulated firms band
    ax.add_patch(mp.FancyBboxPatch((0.4, 0.4), 11.2, 1.3,
        boxstyle="round,pad=0.04", linewidth=1.5, edgecolor=NAVY, facecolor="white"))
    ax.text(6, 1.3, "Banks · Insurers · Asset managers · FSPs · CIS · Exchanges · Brokers",
            ha="center", va="center", fontsize=9.5, color=NAVY, fontweight="bold")
    ax.text(6, 0.8, "are supervised by the relevant combination of the bodies above",
            ha="center", va="center", fontsize=8.5, color=NAVY, style="italic")

    ax.set_title("South African financial regulatory architecture",
                 fontsize=11, color=NAVY, fontweight="bold", pad=8)
    save(fig, "sa_regulators.png")


if __name__ == "__main__":
    twin_peaks()
    reg28()
    aml()
    sa_regulators()
