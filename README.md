# NYC Citi Bike: Markov chain station model (ORIE 5530, Fall 2026)

## Requirements

Python 3.12 or newer with `pandas`, `numpy`, `matplotlib`, `pyarrow`, `scipy`.

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
   of ride durations to `data/warmup_ride_durations.png`.
3. `part1_markov_chains.ipynb`: run all cells (Part I).
4. `part2_simulation.ipynb`: run all cells (Part II).

## Part I: Markov chains

`part1_markov_chains.ipynb` builds the transition matrices for W 21 St & 6 Ave, Ave A & E 14 St and 7 Ave & Central Park South, for weekday mornings (7-10am) and evenings (4-7pm), with a 5 minute step. Run `clean_data.py` first, then run all cells of the notebook. Nothing in Part I is random, so no seed is needed.

| Notebook section                 | Report                    |
| -------------------------------- | ------------------------- |
| 4. Choosing the step             | Table 3                   |
| 5. Rule and step                 | Table 4                   |
| 6. Checks of the assumptions     | Table 5                   |
| 7. Summary of the matrices       | Table 6, Figures 3, 4, 5  |
| 8. Stationary distributions      | Table 7                   |
| 9. What happens within one block | Table 8, Figure 6         |
| 10. Bikes moved by staff         | Day swing at Ave A        |

| File in `figures/`      | Report figure                                           |
| ----------------------- | ------------------------------------------------------- |
| `p1_matrix_rows.png`    | Figure 3 (evening title reads 16-7pm instead of 4-7pm)  |
| `p1_matrices.png`       | Figure 4 (same matrices, 3x2 panels instead of 2x3)     |
| `p1_matrix_edges.png`   | Figure 5 (same states, 3x2 panels instead of 2x3)       |
| `p1_stationary.png`     | Figure 6                                                |
| `p2_sample_paths.png`   | Figure 7 (3x2 panels instead of 2x3)                    |
| `p2_recommendation.png` | Figure 8                                                |

Figure 2 (W 21 St morning, states 54 to 74, 15 second and 5 minute steps) has no code or file in this repo yet.

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
