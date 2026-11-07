"""Step 0: load and clean the August 2026 NYC Citi Bike trip data.

Combines all data/raw/202608-citibike-tripdata_*.csv files, computes ride durations,
applies the cleaning rules required by the project, prints a cleaning report,
and saves the cleaned data to data/trips_clean.parquet for later steps.

Cleaning rules (required by the assignment):
  1. Remove rides lasting more than 3 hours (duration > 180 min).
  2. Remove rides with negative duration.

Additional decisions (documented, NOT removed here):
  - Rides that started on July 31 but ended in August are kept. The published
    file is grouped by ride end date; their durations are valid.
  - Rides with missing start/end station are kept. Their durations are valid
    for the warm-up questions. They cannot be assigned to a station, so they
    drop out of the station-level Markov analysis on their own.
"""
import glob
import os

import pandas as pd

DATA_GLOB = os.path.join("data", "raw", "202608-citibike-tripdata_*.csv")
OUT_PATH = os.path.join("data", "trips_clean.parquet")
MAX_MINUTES = 180


def load_raw(pattern=DATA_GLOB):
    files = sorted(glob.glob(pattern))
    if not files:
        raise FileNotFoundError(f"No files match {pattern}")
    print(f"Loading {len(files)} files: {', '.join(files)}")
    ids = {"start_station_id": str, "end_station_id": str}
    return pd.concat([pd.read_csv(f, dtype=ids) for f in files], ignore_index=True)


def clean(df):
    n_rows, n_cols = df.shape
    print(f"\nBefore cleaning: {n_rows:,} rows x {n_cols} columns")

    df["started_at"] = pd.to_datetime(df["started_at"], format="mixed")
    df["ended_at"] = pd.to_datetime(df["ended_at"], format="mixed")
    df["duration_min"] = (df["ended_at"] - df["started_at"]).dt.total_seconds() / 60

    too_long = df["duration_min"] > MAX_MINUTES
    negative = df["duration_min"] < 0
    print(f"Removed, duration > {MAX_MINUTES} min: {too_long.sum():,}")
    print(f"Removed, negative duration:     {negative.sum():,}")

    out = df.loc[~(too_long | negative)].reset_index(drop=True)
    print(f"Retained: {len(out):,} rows ({len(out) / n_rows:.2%})")

    # Facts about the data that are kept, not removed.
    print("\nNotes on the retained data (kept, not removed):")
    print(f"  Zero-duration rides:                {(out['duration_min'] == 0).sum():,}")
    print(f"  Shortest ride (min):                {out['duration_min'].min():.3f}")
    print(f"  Rides starting before Aug 1:        {(out['started_at'] < '2026-08-01').sum():,}")
    print(f"  Missing start station:              {out['start_station_id'].isna().sum():,}")
    print(f"  Missing end station:                {out['end_station_id'].isna().sum():,}")
    print(f"  Duplicate ride_id:                  {out['ride_id'].duplicated().sum():,}")
    return out


if __name__ == "__main__":
    trips = clean(load_raw())
    os.makedirs("data", exist_ok=True)
    trips.to_parquet(OUT_PATH, index=False)
    print(f"\nSaved {OUT_PATH}")
