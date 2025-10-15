<<<<<<< HEAD
import pandas as pd
from scipy.spatial import cKDTree
import numpy as np

# ---------------- CONFIG ---------------- #
HIST_FILE = "india_solar_dataset_mean.csv"
FUTURE_FILE = "future_climate_dataset.csv"
OUTPUT_FILE = "merged_clean_dataset.csv"

# ---------------- LOAD DATA ---------------- #
print("Loading datasets...")
hist = pd.read_csv(HIST_FILE)
future = pd.read_csv(FUTURE_FILE)

print("Historical data shape:", hist.shape)
print("Future data shape:", future.shape)

# Round to reduce floating errors
hist["lat"] = hist["lat"].round(3)
hist["lon"] = hist["lon"].round(3)
future["lat"] = future["lat"].round(3)
future["lon"] = future["lon"].round(3)

# ---------------- NEAREST NEIGHBOR MERGE ---------------- #
print("Matching coordinates approximately...")

# Build KDTree for fast nearest-neighbor lookup
hist_coords = hist[["lat", "lon"]].to_numpy()
future_coords = future[["lat", "lon"]].to_numpy()

tree = cKDTree(future_coords)

# Find nearest neighbors within a tolerance (in degrees)
dist, idx = tree.query(hist_coords, distance_upper_bound=0.05)  # 0.05° ≈ 5–6 km

# Keep only valid matches (within tolerance)
valid = np.isfinite(dist)
hist_matched = hist.loc[valid].copy()
future_matched = future.iloc[idx[valid]].reset_index(drop=True)

# Merge matched rows
merged = pd.concat([hist_matched.reset_index(drop=True), future_matched.drop(columns=["lat", "lon"])], axis=1)

print("Merged dataset shape:", merged.shape)

# ---------------- CLEAN MISSING VALUES ---------------- #
#merged = merged.dropna()
merged = merged.fillna(merged.mean())
print("After cleaning, shape:", merged.shape)

# ---------------- SAVE FINAL DATASET ---------------- #
merged.to_csv(OUTPUT_FILE, index=False)
print("Clean merged dataset saved as:", OUTPUT_FILE)
print(merged.head())
=======
import pandas as pd
from scipy.spatial import cKDTree
import numpy as np

# ---------------- CONFIG ---------------- #
HIST_FILE = "india_solar_dataset_mean.csv"
FUTURE_FILE = "future_climate_dataset.csv"
OUTPUT_FILE = "merged_clean_dataset.csv"

# ---------------- LOAD DATA ---------------- #
print("Loading datasets...")
hist = pd.read_csv(HIST_FILE)
future = pd.read_csv(FUTURE_FILE)

print("Historical data shape:", hist.shape)
print("Future data shape:", future.shape)

# Round to reduce floating errors
hist["lat"] = hist["lat"].round(3)
hist["lon"] = hist["lon"].round(3)
future["lat"] = future["lat"].round(3)
future["lon"] = future["lon"].round(3)

# ---------------- NEAREST NEIGHBOR MERGE ---------------- #
print("Matching coordinates approximately...")

# Build KDTree for fast nearest-neighbor lookup
hist_coords = hist[["lat", "lon"]].to_numpy()
future_coords = future[["lat", "lon"]].to_numpy()

tree = cKDTree(future_coords)

# Find nearest neighbors within a tolerance (in degrees)
dist, idx = tree.query(hist_coords, distance_upper_bound=0.05)  # 0.05° ≈ 5–6 km

# Keep only valid matches (within tolerance)
valid = np.isfinite(dist)
hist_matched = hist.loc[valid].copy()
future_matched = future.iloc[idx[valid]].reset_index(drop=True)

# Merge matched rows
merged = pd.concat([hist_matched.reset_index(drop=True), future_matched.drop(columns=["lat", "lon"])], axis=1)

print("Merged dataset shape:", merged.shape)

# ---------------- CLEAN MISSING VALUES ---------------- #
#merged = merged.dropna()
merged = merged.fillna(merged.mean())
print("After cleaning, shape:", merged.shape)

# ---------------- SAVE FINAL DATASET ---------------- #
merged.to_csv(OUTPUT_FILE, index=False)
print("Clean merged dataset saved as:", OUTPUT_FILE)
print(merged.head())
>>>>>>> b43b991 (Initial commit of local folder)
