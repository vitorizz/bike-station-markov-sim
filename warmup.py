from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter

from clean_data import OUT_PATH

# Question 1 is in main(). Questions 2-6 are in print_warmup_results().

PLOT_MAX = 60
FIGURE_PATH = Path("figures/warmup_ride_durations.png")

plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
plt.rcParams["font.family"] = "Inter"


def print_probability(label, numerator, denominator):
    if denominator == 0:
        print(f"{label} is undefined (no rides in the denominator).")
        return
    print(f"{label} = {numerator:,} / {denominator:,} = {numerator / denominator:.4%}")


def print_warmup_results(trips):
    # Set up the duration and group filters used in Questions 2-6.
    durations = trips["duration_min"]
    is_member = trips["member_casual"].eq("member")
    is_electric = trips["rideable_type"].eq("electric_bike")
    is_classic = trips["rideable_type"].eq("classic_bike")
    over_20 = durations.gt(20)
    over_25 = durations.gt(25)
    under_10 = durations.lt(10)

    # Question 2. Mean, variance, and rides over 20 minutes
    print("\n2. Overall ride duration")
    print(f"Expected ride duration = {durations.mean():.4f} minutes")
    # Empirical variance is the mean of the squared deviations from the mean.
    print(f"Empirical variance = {durations.var(ddof=0):.4f} minutes squared")
    # Divide by the total number of rides with a valid duration.
    print_probability("P(duration > 20 minutes)", over_20.sum(), len(trips))

    # Question 3. Rides over 20 minutes given membership
    # The denominator is all member rides.
    print("\n3. Probability of a ride over 20 minutes given membership")
    print_probability(
        "P(duration > 20 minutes | member)", (over_20 & is_member).sum(), is_member.sum()
    )

    # Question 4. Membership given a ride over 25 minutes
    # The denominator is all rides over 25 minutes.
    print("\n4. Probability of membership given a ride over 25 minutes")
    print_probability(
        "P(member | duration > 25 minutes)", (is_member & over_25).sum(), over_25.sum()
    )

    # Question 5. Average duration by bike type
    print("\n5. Expected ride duration by bike type")
    print(f"Electric bike = {durations[is_electric].mean():.4f} minutes")
    print(f"Classic bike = {durations[is_classic].mean():.4f} minutes")

    # Question 6. Bike type given a ride under 10 minutes
    # Use all rides under 10 minutes as the denominator for both bike types.
    print("\n6. Bike type given a ride under 10 minutes")
    short_ride_count = under_10.sum()
    print_probability(
        "P(electric bike | duration < 10 minutes)", (is_electric & under_10).sum(), short_ride_count
    )
    print_probability(
        "P(classic bike | duration < 10 minutes)", (is_classic & under_10).sum(), short_ride_count
    )

    # Compare the short-ride shares with each bike type’s share of all rides.
    print("Bike-type shares across all rides")
    print_probability("P(electric bike)", is_electric.sum(), len(trips))
    print_probability("P(classic bike)", is_classic.sum(), len(trips))


def main():
    # Load the cleaned rides once for all six questions.
    # clean_data.py computes duration_min from the elapsed seconds divided by 60.
    trips = pd.read_parquet(
        OUT_PATH, columns=["duration_min", "member_casual", "rideable_type"]
    )
    valid_trips = trips.dropna(subset=["duration_min"])
    valid_durations = valid_trips["duration_min"]
    if valid_durations.empty:
        raise ValueError("The cleaned data has no valid ride durations to plot.")

    # Question 1. Ride duration histogram
    # 1 minute bins up to 60 minutes (report Figure 1)
    bins = np.arange(0, PLOT_MAX + 1, 1)
    counts, _ = np.histogram(valid_durations[valid_durations <= PLOT_MAX], bins=bins)
    median, mean = valid_durations.median(), valid_durations.mean()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(bins[:-1], counts, width=0.9, align="edge", color="#2a78d6")
    ax.set_xlim(0, PLOT_MAX)
    ax.set_xticks(range(0, PLOT_MAX + 1, 5))
    ax.set_xlabel("Ride duration (minutes)")
    ax.set_ylabel("Number of rides")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"{y / 1000:.0f}k" if y else "0"))
    ax.grid(axis="y", color="#e5e5e5")
    ax.set_axisbelow(True)

    summary = f"Median  {median:.1f} min\nMean  {mean:.1f} min\nRides  {len(valid_trips):,}"
    ax.text(0.96, 0.92, summary, transform=ax.transAxes, ha="right", va="top", linespacing=1.8)

    FIGURE_PATH.parent.mkdir(exist_ok=True)
    fig.savefig(FIGURE_PATH, dpi=240)
    plt.close(fig)

    over_60 = (valid_durations > PLOT_MAX).sum()
    peak = counts.argmax()
    print(f"Rides plotted: {int(counts.sum()):,}")
    print(f"Rides over {PLOT_MAX} minutes, left out of the plot: {over_60:,} ({over_60 / len(valid_trips):.1%})")
    print(f"Median {median:.1f} min, peak of the histogram at {bins[peak]}-{bins[peak + 1]} min")
    missing_durations = len(trips) - len(valid_trips)
    print(f"Rides excluded because duration is missing: {missing_durations:,}")
    print(f"Saved {FIGURE_PATH}")

    print_warmup_results(valid_trips)


if __name__ == "__main__":
    main()