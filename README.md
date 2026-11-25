# NYC Citi Bike: Markov chain station model (ORIE 5530, Fall 2026)

## Requirements

Python 3.12 or newer with `pandas`, `numpy`, `matplotlib`, `pyarrow`, `scipy`, and Jupyter for the notebooks.

```
pip install pandas numpy matplotlib pyarrow scipy
```

## Data

The trip data is not in this repo: the CSVs total about 1 GB and the cleaned parquet
file is about 270 MB, while GitHub rejects files over 100 MB. Everything in `data/` is
gitignored and can be rebuilt from the raw CSVs.

Download `202608-citibike-tripdata.zip` (the NYC archive, not `JC-`) from
https://s3.amazonaws.com/tripdata/index.html, unzip it, and put the six CSV files in
`data/raw/`:

```
data/raw/202608-citibike-tripdata_1.csv
...
data/raw/202608-citibike-tripdata_6.csv
```

## Steps

Run everything from the repo root, in this order.

1. `python clean_data.py`: combines the CSVs, removes rides longer than 3 hours or with
   negative duration, prints the cleaning report, and writes `data/trips_clean.parquet`.
2. `python warmup.py`: prints the answers to the warm-up questions and saves the histogram
   of ride durations to `figures/warmup_ride_durations.png`.
3. `exploration.ipynb`: run all cells (warm-up extras and choice of the stations).
4. `part1_markov_chains.ipynb`: run all cells (Part I).
5. `part2_simulation.ipynb`: run all cells (Part II).

## Where each figure and table comes from

| Report    | Code                                                      | File                                                                      |
| --------- | --------------------------------------------------------- | ------------------------------------------------------------------------- |
| Figure 1  | `warmup.py`                                               | `figures/warmup_ride_durations.png`                                       |
| Figure 2  | `part1_markov_chains.ipynb`, section 4                    | `figures/p1_matrix_15s_5min.png`                                          |
| Figure 3  | `part1_markov_chains.ipynb`, section 7                    | `figures/p1_matrix_rows.png`                                              |
| Figure 4  | `part1_markov_chains.ipynb`, section 7                    | `figures/p1_matrices.png`                                                 |
| Figure 5  | `part1_markov_chains.ipynb`, section 7                    | `figures/p1_matrix_edges.png`                                             |
| Figure 6  | `part1_markov_chains.ipynb`, section 9                    | `figures/p1_stationary.png`                                               |
| Figure 7  | `part2_simulation.ipynb`, section 2                       | `figures/p2_sample_paths.png`                                             |
| Figure 8  | `part2_simulation.ipynb`, section 3                       | `figures/p2_recommendation.png`                                           |
| Table 1   | `clean_data.py`                                           | printed                                                                   |
| Table 2   | `exploration.ipynb`, section 5                            | in the notebook                                                           |
| Table 3   | `part1_markov_chains.ipynb`, section 4                    | in the notebook                                                           |
| Table 4   | `part1_markov_chains.ipynb`, section 5                    | in the notebook                                                           |
| Table 5   | `part1_markov_chains.ipynb`, section 6                    | in the notebook                                                           |
| Table 6   | `part1_markov_chains.ipynb`, section 7                    | in the notebook, full matrices in `outputs/matrices/`                     |
| Table 7   | `part1_markov_chains.ipynb`, section 8                    | in the notebook                                                           |
| Table 8   | `part1_markov_chains.ipynb`, section 9                    | in the notebook                                                           |
| Table 9   | `part2_simulation.ipynb`, section 2                       | in the notebook                                                           |
| Table 10  | `part2_simulation.ipynb`, section 3                       | in the notebook                                                           |
| Table 11  | `part2_simulation.ipynb`, section 5                       | in the notebook                                                           |
| Table 12  | `exploration.ipynb`, section 4                            | in the notebook                                                           |
| Table 13  | `exploration.ipynb`, section 6                            | in the notebook                                                           |

All figures use the Inter font, version 4.1 (https://rsms.me/inter). Without it matplotlib prints a warning and uses its default font.

## Warm-up and choice of the stations

`warmup.py` answers Q1 to Q6 and draws Figure 1. `exploration.ipynb` computes the other numbers of these sections. It groups rides by station name, which gives the 2,390 stations of the report, while Part I uses station IDs. Nothing in it is random.

| Notebook section                  | Report                                                                        |
| --------------------------------- | ----------------------------------------------------------------------------- |
| 1. Warm-up extras                 | Median, casual rates, Bayes' rule in Q4, splits by user type in Q5, Q6 shares |
| 2. Rides across the city by hour  | Hourly peaks, member shares in "Stations and time blocks"                     |
| 3. The two storm days             | Share of normal rides on August 20 and 27                                     |
| 4. Candidate stations             | Table 12                                                                      |
| 5. The three stations we model    | Table 2, distance between W 21 St and Ave A                                   |
| 6. Morning net flow on single days | Table 13                                                                     |

## Part I: Markov chains

`part1_markov_chains.ipynb` builds the transition matrices for W 21 St & 6 Ave, Ave A & E 14 St and 7 Ave & Central Park South, for weekday mornings (7-10am) and evenings (4-7pm), with a 5 minute step. Run `clean_data.py` first, then run all cells of the notebook. Nothing in Part I is random, so no seed is needed. The docks are checked against the station feed saved in `station_feed/`.

| Notebook section                 | Report                    |
| -------------------------------- | ------------------------- |
| 4. Choosing the step             | Table 3, Figure 2         |
| 5. Rule and step                 | Table 4                   |
| 6. Checks of the assumptions     | Table 5                   |
| 7. Summary of the matrices       | Table 6, Figures 3, 4, 5  |
| 8. Stationary distributions      | Table 7                   |
| 9. What happens within one block | Table 8, Figure 6         |
| 10. Bikes moved by staff         | Day swing at Ave A        |

Figures are saved in `figures/` and the 6 full transition matrices in `outputs/matrices/`, where row i and column j give P(i, j).

## Part II: Simulation

`part2_simulation.ipynb` simulates the six chains of Part I and tests moving bikes between
W 21 St and Ave A. It reads the transition matrices from `outputs/matrices/`. Sections 1 to 4
need nothing else. Section 5 checks the recommendation against the rides themselves and reads
`data/trips_clean.parquet`, like Part I. Run `part1_markov_chains.ipynb` first if the matrices
are not there, then run all cells of the notebook.

Settings, all in the first cell of the notebook:

| Setting                                  | Value                                                          |
| ---------------------------------------- | -------------------------------------------------------------- |
| Random seed                              | 5530                                                           |
| Simulation runs per case                 | 10,000                                                         |
| Steps per block                          | 36 steps of 5 minutes                                          |
| Starting state                           | Half full: 37 bikes at W 21 St, 20 at Ave A, 40 at 7 Ave & CPS |
| Resamples of the 21 weekdays (section 5) | 500, same seed                                                 |

Each simulated case uses its own random stream built from the seed, the station, the block
and the starting state, so the results are the same on every run and in any cell order.

| Notebook section                                   | Report                                             |
| -------------------------------------------------- | -------------------------------------------------- |
| 2. Runs for each station and block                 | Figure 7, Table 9, starting state paragraph        |
| 3. Recommendation                                  | Figure 8, Table 10                                 |
| 4. When the move does not help                     | Last paragraph of the recommendation               |
| 5. Checks of the recommendation with the trip data | Table 11                                           |

The notebook saves `figures/p2_sample_paths.png` and `figures/p2_recommendation.png`.
