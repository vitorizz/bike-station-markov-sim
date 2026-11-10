from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import StrMethodFormatter

from clean_data import MAX_MINUTES, OUT_PATH

# Question 1 is in main(). Questions 2-6 are in print_warmup_results().

BIN_WIDTH = 5
FIGURE_PATH = Path(OUT_PATH).with_name("warmup_ride_durations.png")


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

    # Question 2. Mean, variance, and rides over 20 minutes ---
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
    missing_durations = len(trips) - len(valid_trips)
    print(f"Rides excluded because duration is missing: {missing_durations:,}")
    print(f"Saved {FIGURE_PATH}")

    print_warmup_results(valid_trips)


if __name__ == "__main__":
    main()