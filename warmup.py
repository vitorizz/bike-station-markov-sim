from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import StrMethodFormatter

from clean_data import MAX_MINUTES, OUT_PATH

# 1. Using the start and end times, compute each ride’s duration in minutes and plot a histogram of ride durations.

BIN_WIDTH = 5
FIGURE_PATH = Path(OUT_PATH).with_name("warmup_ride_durations.png")


def main():
    # clean_data.py computes duration_min from the elapsed seconds divided by 60.
    durations = pd.read_parquet(OUT_PATH, columns=["duration_min"])["duration_min"]
    valid_durations = durations.dropna()
    if valid_durations.empty:
        raise ValueError("The cleaned data has no valid ride durations to plot.")

    bins = range(0, MAX_MINUTES + 1, BIN_WIDTH)
    fig, ax = plt.subplots(figsize=(9, 5), layout="constrained")
    counts, _, _ = ax.hist(
        valid_durations, bins=bins, color="#24608A", edgecolor="white", linewidth=0.6
    )
    ax.set(
        title="NYC Citi Bike ride durations, August 2026",
        xlabel="Ride duration (minutes)",
        ylabel="Number of rides per 5-minute bin",
        xlim=(0, MAX_MINUTES),
        xticks=range(0, MAX_MINUTES + 1, 20),
    )
    ax.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
    ax.set_axisbelow(True)
    ax.grid(axis="y", alpha=0.25)
    fig.savefig(FIGURE_PATH, dpi=200)
    plt.close(fig)

    print(f"Rides plotted: {int(counts.sum()):,}")
    print(f"Rides excluded because duration is missing: {durations.isna().sum():,}")
    print(f"Saved {FIGURE_PATH}")


if __name__ == "__main__":
    main()
