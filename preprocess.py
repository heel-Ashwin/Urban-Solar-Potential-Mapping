<<<<<<< HEAD
import rasterio
import numpy as np
import pandas as pd
from rasterio.enums import Resampling

INDIA_BOUNDS = {"min_lon": 68.0, "max_lon": 98.0,
                "min_lat": 6.0, "max_lat": 37.0}

# Target resolution: 5 min ≈ 0.0833°, 10 min ≈ 0.1667°
TARGET_RES = 0.0833   

DATASETS = {
    "srad": "wc2.1_5m_srad_",
    "tmin": "wc2.1_5m_tmin_",
    "tmax": "wc2.1_5m_tmax_",
    "prec": "wc2.1_5m_prec_"
}
ELEV_FILE = "wc2.1_5m_elev.tif"

def preprocess_geotiff(file_path, var_name, target_res=TARGET_RES):
    with rasterio.open(file_path) as src:
        transform = rasterio.transform.from_origin(
            west=src.bounds.left, north=src.bounds.top,
            xsize=target_res, ysize=target_res
        )
        new_width = int((src.bounds.right - src.bounds.left) / target_res)
        new_height = int((src.bounds.top - src.bounds.bottom) / target_res)

        data = src.read(
            1,
            out_shape=(new_height, new_width),
            resampling=Resampling.bilinear
        )

        rows, cols = np.where(data != src.nodata)
        lats, lons, values = [], [], []

        for r, c in zip(rows, cols):
            lon, lat = transform * (c, r)
            if (INDIA_BOUNDS["min_lon"] <= lon <= INDIA_BOUNDS["max_lon"] and
                INDIA_BOUNDS["min_lat"] <= lat <= INDIA_BOUNDS["max_lat"]):
                lats.append(lat)
                lons.append(lon)
                values.append(data[r, c])

        return pd.DataFrame({"lat": lats, "lon": lons, var_name: values})


master_df = None

for var, base_path in DATASETS.items():
    for m in range(1, 13):
        month = f"{m:02d}" 
        file_path = f"{base_path}{month}.tif"
        var_name = f"{var}_{month}"

        print(f"Processing {var_name} ...")
        df = preprocess_geotiff(file_path, var_name)

        if master_df is None:
            master_df = df
        else:
            master_df = pd.merge(master_df, df, on=["lat", "lon"], how="inner")

print("Processing elevation ...")
df_elev = preprocess_geotiff(ELEV_FILE, "elev")
master_df = pd.merge(master_df, df_elev, on=["lat", "lon"], how="inner")

master_df.to_csv("india_solar_dataset_full.csv", index=False)
print("Master dataset saved: india_solar_dataset_full.csv")
print(master_df.head())
=======
import rasterio
import numpy as np
import pandas as pd
from rasterio.enums import Resampling

INDIA_BOUNDS = {"min_lon": 68.0, "max_lon": 98.0,
                "min_lat": 6.0, "max_lat": 37.0}

# Target resolution: 5 min ≈ 0.0833°, 10 min ≈ 0.1667°
TARGET_RES = 0.0833   

DATASETS = {
    "srad": "wc2.1_5m_srad_",
    "tmin": "wc2.1_5m_tmin_",
    "tmax": "wc2.1_5m_tmax_",
    "prec": "wc2.1_5m_prec_"
}
ELEV_FILE = "wc2.1_5m_elev.tif"

def preprocess_geotiff(file_path, var_name, target_res=TARGET_RES):
    with rasterio.open(file_path) as src:
        transform = rasterio.transform.from_origin(
            west=src.bounds.left, north=src.bounds.top,
            xsize=target_res, ysize=target_res
        )
        new_width = int((src.bounds.right - src.bounds.left) / target_res)
        new_height = int((src.bounds.top - src.bounds.bottom) / target_res)

        data = src.read(
            1,
            out_shape=(new_height, new_width),
            resampling=Resampling.bilinear
        )

        rows, cols = np.where(data != src.nodata)
        lats, lons, values = [], [], []

        for r, c in zip(rows, cols):
            lon, lat = transform * (c, r)
            if (INDIA_BOUNDS["min_lon"] <= lon <= INDIA_BOUNDS["max_lon"] and
                INDIA_BOUNDS["min_lat"] <= lat <= INDIA_BOUNDS["max_lat"]):
                lats.append(lat)
                lons.append(lon)
                values.append(data[r, c])

        return pd.DataFrame({"lat": lats, "lon": lons, var_name: values})


master_df = None

for var, base_path in DATASETS.items():
    for m in range(1, 13):
        month = f"{m:02d}" 
        file_path = f"{base_path}{month}.tif"
        var_name = f"{var}_{month}"

        print(f"Processing {var_name} ...")
        df = preprocess_geotiff(file_path, var_name)

        if master_df is None:
            master_df = df
        else:
            master_df = pd.merge(master_df, df, on=["lat", "lon"], how="inner")

print("Processing elevation ...")
df_elev = preprocess_geotiff(ELEV_FILE, "elev")
master_df = pd.merge(master_df, df_elev, on=["lat", "lon"], how="inner")

master_df.to_csv("india_solar_dataset_full.csv", index=False)
print("Master dataset saved: india_solar_dataset_full.csv")
print(master_df.head())
>>>>>>> b43b991 (Initial commit of local folder)
