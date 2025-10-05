import pandas as pd

# Load the full monthly dataset you already generated
df = pd.read_csv("india_solar_dataset_full.csv")

# Compute annual means for each variable
for var in ["srad", "tmin", "tmax", "prec"]:
    month_cols = [f"{var}_{i:02d}" for i in range(1, 13)]
    df[f"{var}_mean"] = df[month_cols].mean(axis=1)

# Select only the mean + elevation columns
mean_df = df[["lat", "lon", "srad_mean", "tmin_mean", "tmax_mean", "prec_mean", "elev"]]

# Save the new mean dataset
mean_df.to_csv("india_solar_dataset_mean.csv", index=False)

print("Mean dataset saved: india_solar_dataset_mean.csv")
print(mean_df.head())
