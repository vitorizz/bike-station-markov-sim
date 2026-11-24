# NYC Citi Bike: Markov chain station model (ORIE 5530, Fall 2026)

## Requirements

Python 3.13 with `pandas`, `numpy`, `matplotlib`, `pyarrow`, `scipy`.

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

## Part I: Markov chains

`part1_markov_chains.ipynb` builds the transition matrices for W 21 St & 6 Ave, Ave A & E 14 St and 7 Ave & Central Park South, for weekday mornings (7-10am) and evenings (4-7pm), with a 5 minute step. Run `clean_data.py` first, then run all cells of the notebook. Nothing in Part I is random, so no seed is needed.

| Notebook section                 | Report                              |
| -------------------------------- | ----------------------------------- |
| 4. Choosing the step             | Table 5                             |
| 5. Rule and step                 | Table 6                             |
| 6. Checks of the assumptions     | Table 7                             |
| 7. Summary of the matrices       | Table 8, Figure 3, appendix figures |
| 8. Stationary distributions      | Table 9                             |
| 9. What happens within one block | Table 10, Figure 6                  |
| 10. Bikes moved by staff         | Day swing at Ave A                  |

Figures are saved in `figures/` and the 6 full transition matrices in `outputs/matrices/`, where row i and column j give P(i, j).

## Part II: Simulation

`part2_simulation.ipynb` simulates the six chains of Part I and tests moving bikes between W 21 St and Ave A. It reads the transition matrices from `outputs/matrices/`, so it does not need the trip data. Run `part1_markov_chains.ipynb` first if the matrices are not there, then run all cells of the notebook.

Settings, all in the first cell of the notebook:

| Setting                  | Value                                                          |
| ------------------------ | -------------------------------------------------------------- |
| Random seed              | 5530                                                           |
| Simulation runs per case | 10,000                                                         |
| Steps per block          | 36 steps of 5 minutes                                          |
| Starting state           | Half full: 37 bikes at W 21 St, 20 at Ave A, 40 at 7 Ave & CPS |

Each simulated case uses its own random stream built from the seed, the station, the block and the starting state, so the results are the same on every run and in any cell order.

| Notebook section                   | Report                               |
| ---------------------------------- | ------------------------------------ |
| 2. Runs for each station and block | Figure 7, Table 9                    |
| 3. Recommendation                  | Figure 8, Table 10                   |
| 4. When the move does not help     | Last paragraph of the recommendation |

The notebook saves `figures/p2_sample_paths.png` and `figures/p2_recommendation.png`.
