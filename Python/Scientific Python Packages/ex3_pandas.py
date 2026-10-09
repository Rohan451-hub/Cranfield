import numpy as np
import pandas as pd

data = {
    "run_id":    list(range(1, 31)),
    "config":    ["A"] * 10 + ["B"] * 10 + ["C"] * 10,
    "alpha_deg": [0, 0, 2, 2, 4, 4, 6, 6, 8, 8] * 3,
    "CL": [0.11, 0.12, 0.34, 0.35, 0.57, 0.56, 0.79, 0.80, 1.00, np.nan,
           0.14, 0.13, 0.40, 0.41, 0.66, 0.65, 0.91, 0.92, 1.15, 1.16,
           0.09, 0.10, 0.28, 0.29, 0.47, np.nan, 0.65, 0.66, 0.82, 0.83],
    "CD": [0.0082, 0.0083, 0.0091, 0.0090, 0.0115, 0.0116, 0.0158, 0.0157, 0.0223, np.nan,
           0.0090, 0.0091, 0.0103, 0.0104, 0.0133, 0.0132, 0.0185, 0.0186, 0.0263, 0.0265,
           0.0078, 0.0079, 0.0085, 0.0086, 0.0104, np.nan, 0.0138, 0.0139, 0.0195, 0.0196],
}

# Write the raw data to disk, then read it back the way you would a real test file
pd.DataFrame(data).to_csv("wind_tunnel_raw.csv", index=False)
df = pd.read_csv("wind_tunnel_raw.csv")

# Task 1: inspect and clean
print(df.head())
print(df.info())
print(df.describe())
print(df.isna().sum())            # how many gaps in each column

clean = df.dropna(subset=["CL", "CD"])
print("Runs remaining:", len(clean))

clean = clean.copy()
clean["LD"] = clean["CL"] / clean["CD"]  # TODO: lift-to-drag ratio

# Task 2: per-configuration summary
summary = clean.groupby("config").agg(
    CL_mean = ("CL", "mean"),
    CD_mean = ("CD", "mean"),
    LD_mean = ("LD", "mean"),
    LD_max  = ("LD", "max"),
    n_runs  = ("run_id", "count"),
)
print(summary.round(3))

# Task 3: best operating point for each configuration
mean_ld = clean.groupby(["config", "alpha_deg"])["LD"].mean()
print(mean_ld.round(2))

best = mean_ld.groupby("config").idxmax()
for config, key in best.items():
    print(f"Config {config}: best alpha = {key[1]} deg, mean L/D = {mean_ld[key]:.2f}")

# Task 4: high-lift conditions and export
high_lift = clean[clean["CL"] > 0.70]  # TODO: rows of clean where CL > 0.70
pivot = high_lift.pivot_table(values="CD", index="alpha_deg",
                              columns="config", aggfunc="mean")
print(pivot)

clean.to_csv("wind_tunnel_cleaned.csv", index=False)
pivot.to_csv("wind_tunnel_pivot.csv")