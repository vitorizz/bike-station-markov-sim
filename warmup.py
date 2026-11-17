"""Warm-up questions 1-6 on the cleaned August 2026 Citi Bike data.

Input:  data/trips_clean.parquet  (produced by clean_data.py)
Output: figures/duration_histogram.png
        results/warmup_results.csv
All probabilities are empirical frequencies over the cleaned rides.
Thresholds are strict: "more than 20 min" means duration > 20, "less than 10 min" means < 10.
"""
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

IN_PATH = os.path.join("data", "trips_clean.parquet")
FIG_PATH = os.path.join("figures", "duration_histogram.png")
RES_PATH = os.path.join("results", "warmup_results.csv")

BLUE = "#2a78d6"
INK = "#0b0b0b"
INK_2 = "#52514e"
GRID = "#e4e3df"


def plot_histogram(d):
    """Q1: histogram of ride durations. Two panels: the bulk (0-60 min) and the full tail (log scale)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

    ax1.hist(d[d <= 60], bins=np.arange(0, 61, 1), color=BLUE, edgecolor="white", linewidth=0.6)
    ax1.set_title("Rides up to 60 minutes (1-minute bins)", loc="left", color=INK, fontsize=11)
    ax1.set_ylabel("Number of rides")
    ax1.axvline(d.mean(), color=INK, linewidth=1, linestyle="--")
    ax1.text(d.mean() + 1, ax1.get_ylim()[1] * 0.9, f"mean {d.mean():.1f} min", color=INK, fontsize=9)
    ax1.text(60, ax1.get_ylim()[1] * 0.9, f"{(d > 60).mean():.1%} of rides\nare over 60 min",
             color=INK_2, fontsize=9, ha="right")

    ax2.hist(d, bins=np.arange(0, 181, 2), color=BLUE, edgecolor="white", linewidth=0.4)
    ax2.set_yscale("log")
    ax2.set_title("All rides, 0-180 minutes (2-minute bins, log scale)", loc="left", color=INK, fontsize=11)

    for ax in (ax1, ax2):
        ax.set_xlabel("Ride duration (minutes)")
        ax.grid(axis="y", color=GRID, linewidth=0.6)
        ax.set_axisbelow(True)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        ax.spines["left"].set_color(INK_2)
        ax.spines["bottom"].set_color(INK_2)
        ax.tick_params(colors=INK_2)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v / 1000:.0f}k"))

    fig.suptitle(f"Citi Bike ride durations, August 2026 (n = {len(d):,} rides)",
                 x=0.01, ha="left", color=INK, fontsize=13)
    fig.tight_layout()
    os.makedirs("figures", exist_ok=True)
    fig.savefig(FIG_PATH, dpi=200)
    plt.close(fig)
    print(f"Saved {FIG_PATH}")


def main():
    trips = pd.read_parquet(IN_PATH, columns=["duration_min", "member_casual", "rideable_type"])
    d = trips["duration_min"]
    member = trips["member_casual"] == "member"
    electric = trips["rideable_type"] == "electric_bike"
    classic = trips["rideable_type"] == "classic_bike"
    print(f"Rides: {len(trips):,}")
    print("Rideable types:", trips["rideable_type"].value_counts().to_dict())
    print("Membership:", trips["member_casual"].value_counts().to_dict())

    # Q1
    plot_histogram(d)

    rows = []

    def report(q, name, value, fmt="{:.4f}"):
        rows.append({"question": q, "quantity": name, "value": value})
        print(f"  {name}: {fmt.format(value)}")

    print("\nQ2")
    report("Q2", "E[D] mean duration (min)", d.mean())
    report("Q2", "Var(D) sample variance (min^2, ddof=1)", d.var(ddof=1))
    report("Q2", "SD(D) (min)", d.std(ddof=1))
    report("Q2", "P(D > 20)", (d > 20).mean())

    print("\nQ3")
    report("Q3", "P(D > 20 | member)", (d[member] > 20).mean())
    report("Q3", "P(D > 20 | casual) [for comparison]", (d[~member] > 20).mean())

    print("\nQ4")
    long25 = d > 25
    p_member_given_long = member[long25].mean()
    report("Q4", "P(member | D > 25)", p_member_given_long)
    report("Q4", "P(member) [prior, for comparison]", member.mean())
    # Bayes cross-check: P(member | D>25) = P(D>25 | member) P(member) / P(D>25)
    bayes = (d[member] > 25).mean() * member.mean() / long25.mean()
    assert np.isclose(bayes, p_member_given_long), "Bayes cross-check failed"
    print(f"  (Bayes cross-check agrees: {bayes:.4f})")

    print("\nQ5")
    report("Q5", "E[D | electric] (min)", d[electric].mean())
    report("Q5", "E[D | classic] (min)", d[classic].mean())

    print("\nQ6")
    short10 = d < 10
    report("Q6", "P(electric | D < 10)", electric[short10].mean())
    report("Q6", "P(classic | D < 10)", classic[short10].mean())
    report("Q6", "P(electric) [overall, for comparison]", electric.mean())
    report("Q6", "P(classic) [overall, for comparison]", classic.mean())
    report("Q6", "P(D < 10 | electric) [for comparison]", (d[electric] < 10).mean())
    report("Q6", "P(D < 10 | classic) [for comparison]", (d[classic] < 10).mean())

    os.makedirs("results", exist_ok=True)
    pd.DataFrame(rows).to_csv(RES_PATH, index=False)
    print(f"\nSaved {RES_PATH}")


if __name__ == "__main__":
    main()
