# NYC Citi Bike: Markov chain station model (ORIE 5530, Fall 2026)

## Requirements

Python 3.13 with `pandas`, `numpy`, `matplotlib`, `pyarrow`.

```
pip install pandas numpy matplotlib pyarrow
```

## Data

The trip data is not in this repo: the CSVs total about 1 GB and the cleaned parquet
file is about 270 MB, while GitHub rejects files over 100 MB. Everything in `data/` is
gitignored and can be rebuilt from the raw CSVs.

**Shortcut for group members:** `trips_clean.parquet` is in the group's shared Drive
folder, copy it to `data/trips_clean.parquet` and skip step 1 below.

**Full reproduction:** download `202608-citibike-tripdata.zip`
(the NYC archive, not `JC-`) from https://s3.amazonaws.com/tripdata/index.html,
unzip it, and put the six CSV files in `data/raw/`:

```
data/raw/202608-citibike-tripdata_1.csv
...
data/raw/202608-citibike-tripdata_6.csv
```

## Steps

Run all scripts from the repo root.

1. `python clean_data.py`: combines the CSVs, removes rides longer than 3 hours or with
   negative duration, prints the cleaning report, and writes `data/trips_clean.parquet`.
