import pandas as pd
import numpy as np
import os
import joblib

# =====================================
# LOAD DATA
# =====================================
df = pd.read_csv("dataset.csv")

# Clean zone_id
df["zone_id"] = (
    df["zone_id"]
    .astype(str)
    .str.lower()
    .str.replace("zone_", "", regex=False)
    .str.strip()
    .astype(int)
)

print(df.head())

# =====================================
# FEATURES & TARGET
# =====================================
x = df.drop(columns=["incident_count"])
y = df["incident_count"]

print("Feature columns:", x.columns)

# =====================================
# TRAIN-TEST SPLIT (TIME-AWARE)
# =====================================
training_size = 0.8
split_index = int(len(df) * training_size)

training_x = x.iloc[:split_index]
testing_x  = x.iloc[split_index:]

training_y = y.iloc[:split_index]
testing_y  = y.iloc[split_index:]

# Save feature order (VERY IMPORTANT)
FEATURE_COLUMNS = training_x.columns.tolist()

# =====================================
# MODEL: RANDOM FOREST REGRESSOR
# =====================================
from sklearn.ensemble import RandomForestRegressor

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

# =====================================
# CROSS-VALIDATION (UPGRADE 1)
# =====================================
from sklearn.model_selection import TimeSeriesSplit, cross_val_score

tscv = TimeSeriesSplit(n_splits=5)

cv_scores = cross_val_score(
    model,
    training_x,
    training_y,
    cv=tscv,
    scoring="neg_mean_absolute_error"
)

print("Cross-Validation MAE:", -cv_scores.mean())

# =====================================
# FINAL TRAINING
# =====================================
model.fit(training_x, training_y)

# =====================================
# PREDICTION
# =====================================
y_predict = model.predict(testing_x)

# =====================================
# MODEL EVALUATION
# =====================================
from sklearn.metrics import mean_absolute_error

MAE = mean_absolute_error(testing_y, y_predict)
print(MAE, "this is the MAE")

# =====================================
# DEPLOYMENT LOGIC (UNCHANGED)
# =====================================
def deployment_plan(y_predict):
    if y_predict >= 7:
        return {
            "ambulance": 3,
            "police": 2,
            "fire": 1,
            "priority": "HIGH"
        }
    elif y_predict >= 4:
        return {
            "ambulance": 2,
            "police": 1,
            "fire": 0,
            "priority": "MEDIUM"
        }
    else:
        return {
            "ambulance": 1,
            "police": 0,
            "fire": 0,
            "priority": "LOW"
        }

# =====================================
# PREDICTION UNCERTAINTY (UPGRADE 2)
# =====================================
def prediction_uncertainty(model, X, n_runs=30):
    predictions = []
    for _ in range(n_runs):
        predictions.append(model.predict(X))
    return np.std(predictions, axis=0)

uncertainty = prediction_uncertainty(model, testing_x)
print("Average prediction uncertainty:", uncertainty.mean())

# =====================================
# FEATURE IMPORTANCE SAVE (UPGRADE 3)
# =====================================
feature_importance = pd.DataFrame({
    "feature": FEATURE_COLUMNS,
    "importance": model.feature_importances_
}).sort_values("importance", ascending=False)

feature_importance.to_csv("feature_importance.csv", index=False)

# =====================================
# DATA DRIFT BASELINE (UPGRADE 4)
# =====================================
training_stats = training_x.describe()
training_stats.to_csv("training_data_stats.csv")

# =====================================
# MODEL VERSIONING & SAVE (UPGRADE 5)
# =====================================
MODEL_VERSION = "v1.2"

print("Saving files in:", os.getcwd())

joblib.dump(model, "rf_model_v1.2.pkl")
joblib.dump(FEATURE_COLUMNS, "feature_columns_v1.2.pkl")


print(f"Model and metadata saved successfully (version {MODEL_VERSION})")
