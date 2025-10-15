import pandas as pd
import numpy as np
import joblib
import warnings
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor

warnings.filterwarnings("ignore")

# ======================================================
# LOAD DATA
# ======================================================
df = pd.read_csv("merged_clean_dataset.csv")
print("Dataset loaded successfully. Shape:", df.shape)



# ======================================================
# DEFINE FEATURES AND TARGETS
# ======================================================
X_train = df[["tmin_mean", "tmax_mean", "prec_mean", "elev"]]
y_train = df["srad_mean"]
X_future = df[["tmin_future", "tmax_future", "prec_future", "elev"]]

# ======================================================
# DEFINE MODELS
# ======================================================
models = {
    "RandomForest": RandomForestRegressor(
        n_estimators=100, max_depth=10, random_state=42, n_jobs=-1
    ),
    "XGBoost": XGBRegressor(
        n_estimators=120,
        learning_rate=0.05,
        max_depth=8,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        tree_method="hist"
    ),
    "LightGBM": LGBMRegressor(
        n_estimators=120,
        learning_rate=0.05,
        max_depth=8,
        num_leaves=31,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42
    ),
    "CatBoost": CatBoostRegressor(
        iterations=120,
        depth=8,
        learning_rate=0.1,
        random_seed=42,
        verbose=0
    )
}

# ======================================================
# TRAIN AND EVALUATE MODELS
# ======================================================
results = []
print("\nTraining and evaluating models...")

for name, model in models.items():
    print(f"\nTraining {name} ...")
    model.fit(X_train, y_train)
    preds = model.predict(X_train)

    r2 = r2_score(y_train, preds)
    rmse = np.sqrt(mean_squared_error(y_train, preds))


    results.append((name, r2, rmse))
    print(f"{name} -> R²: {r2:.4f}, RMSE: {rmse:.4f}")

# ======================================================
# COMPARISON RESULTS
# ======================================================
results_df = pd.DataFrame(results, columns=["Model", "R2", "RMSE"])
print("\nModel Comparison:\n", results_df)

# Plot model performance for visualization
plt.figure(figsize=(8, 5))
plt.bar(results_df["Model"], results_df["R2"], color="skyblue")
plt.title("Model Comparison - R² Score")
plt.xlabel("Algorithm")
plt.ylabel("R² Score")
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig("model_comparison.png")
plt.show()

# ======================================================
# SELECT BEST MODEL
# ======================================================
best_model_name = results_df.sort_values("R2", ascending=False).iloc[0]["Model"]
best_model = models[best_model_name]
print(f"\nBest model selected: {best_model_name}")

# ======================================================
# FINAL TRAINING AND FUTURE PREDICTION
# ======================================================
best_model.fit(X_train, y_train)
X_future_renamed = X_future.rename(
    columns={
        "tmin_future": "tmin_mean",
        "tmax_future": "tmax_mean",
        "prec_future": "prec_mean"
    }
)
df["predicted_solar_future"] = best_model.predict(X_future_renamed)

# ======================================================
# SAVE OUTPUTS
# ======================================================
df.to_csv("solar_predictions.csv", index=False)
joblib.dump(best_model, "best_solar_model.pkl")

print("\nSaved predictions -> solar_predictions.csv")
print("Saved trained model -> best_solar_model.pkl")

print("\nSample Output:")
print(df[["lat", "lon", "srad_mean", "predicted_solar_future"]].head())
