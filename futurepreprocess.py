<<<<<<< HEAD
import rasterio
import pandas as pd
import numpy as np
import os

# India geographic bounds
INDIA_BOUNDS = {"min_lon": 68.0, "max_lon": 98.0,
                "min_lat": 6.0, "max_lat": 37.0}

def preprocess_single_geotiff(file_path, var_name):
    print(f"Processing {var_name} ...")
    with rasterio.open(file_path) as src:
        arr = src.read(1)
        arr = np.where(arr == src.nodata, np.nan, arr)

        # Create latitude and longitude grids
        lon_vals = np.linspace(src.bounds.left, src.bounds.right, src.width)
        lat_vals = np.linspace(src.bounds.top, src.bounds.bottom, src.height)
        lon, lat = np.meshgrid(lon_vals, lat_vals)

        # Flatten arrays
        lat_flat = lat.flatten()
        lon_flat = lon.flatten()
        val_flat = arr.flatten()

        # Filter only India region
        mask = (
            (lon_flat >= INDIA_BOUNDS["min_lon"]) &
            (lon_flat <= INDIA_BOUNDS["max_lon"]) &
            (lat_flat >= INDIA_BOUNDS["min_lat"]) &
            (lat_flat <= INDIA_BOUNDS["max_lat"])
        )

        df = pd.DataFrame({
            "lat": lat_flat[mask],
            "lon": lon_flat[mask],
            var_name: val_flat[mask]
        })

    return df

tmin_path = os.path.join("wc2.1_5m_tmin_MPI-ESM1-2-HR_ssp245_2021-2040.tif")
tmax_path = os.path.join("wc2.1_5m_tmax_MPI-ESM1-2-HR_ssp245_2021-2040.tif")
prec_path = os.path.join("wc2.1_5m_prec_MPI-ESM1-2-HR_ssp245_2021-2040.tif")

# Process each variable
tmin_df = preprocess_single_geotiff(tmin_path, "tmin_future")
tmax_df = preprocess_single_geotiff(tmax_path, "tmax_future")
prec_df = preprocess_single_geotiff(prec_path, "prec_future")

# Merge all into one dataframe
print("Merging all variables ...")
merged = tmin_df.merge(tmax_df, on=["lat", "lon"], how="outer")
merged = merged.merge(prec_df, on=["lat", "lon"], how="outer")

# Save final file
merged.to_csv("future_climate_dataset.csv", index=False)
print("Future dataset saved as future_climate_dataset.csv")
=======
import rasterio
import pandas as pd
import numpy as np
import os

# India geographic bounds
INDIA_BOUNDS = {"min_lon": 68.0, "max_lon": 98.0,
                "min_lat": 6.0, "max_lat": 37.0}

def preprocess_single_geotiff(file_path, var_name):
    print(f"Processing {var_name} ...")
    with rasterio.open(file_path) as src:
        arr = src.read(1)
        arr = np.where(arr == src.nodata, np.nan, arr)

        # Create latitude and longitude grids
        lon_vals = np.linspace(src.bounds.left, src.bounds.right, src.width)
        lat_vals = np.linspace(src.bounds.top, src.bounds.bottom, src.height)
        lon, lat = np.meshgrid(lon_vals, lat_vals)

        # Flatten arrays
        lat_flat = lat.flatten()
        lon_flat = lon.flatten()
        val_flat = arr.flatten()

        # Filter only India region
        mask = (
            (lon_flat >= INDIA_BOUNDS["min_lon"]) &
            (lon_flat <= INDIA_BOUNDS["max_lon"]) &
            (lat_flat >= INDIA_BOUNDS["min_lat"]) &
            (lat_flat <= INDIA_BOUNDS["max_lat"])
        )

        df = pd.DataFrame({
            "lat": lat_flat[mask],
            "lon": lon_flat[mask],
            var_name: val_flat[mask]
        })

    return df

tmin_path = os.path.join("wc2.1_5m_tmin_MPI-ESM1-2-HR_ssp245_2021-2040.tif")
tmax_path = os.path.join("wc2.1_5m_tmax_MPI-ESM1-2-HR_ssp245_2021-2040.tif")
prec_path = os.path.join("wc2.1_5m_prec_MPI-ESM1-2-HR_ssp245_2021-2040.tif")

# Process each variable
tmin_df = preprocess_single_geotiff(tmin_path, "tmin_future")
tmax_df = preprocess_single_geotiff(tmax_path, "tmax_future")
prec_df = preprocess_single_geotiff(prec_path, "prec_future")

# Merge all into one dataframe
print("Merging all variables ...")
merged = tmin_df.merge(tmax_df, on=["lat", "lon"], how="outer")
merged = merged.merge(prec_df, on=["lat", "lon"], how="outer")

# Save final file
merged.to_csv("future_climate_dataset.csv", index=False)
print("Future dataset saved as future_climate_dataset.csv")
>>>>>>> b43b991 (Initial commit of local folder)
