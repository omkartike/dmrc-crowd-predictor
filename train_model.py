import os
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# 1. Load data safely
data_path = os.path.join("data", "ridership.csv")
if not os.path.exists(data_path):
    raise FileNotFoundError(
        f"Could not find '{data_path}'. Please run 'python3 simulate_data.py' first!"
    )

print(f"Loading expanded dataset from {data_path}...")
df = pd.read_csv(data_path)

print(f"\n--- Dataset Discovery Profile ---")
print(f"Total Rows Loaded : {len(df):,}")
print(f"Unique Metro Lines: {df['line'].nunique()}")
print(f"Unique Stations   : {df['station'].nunique()}")
print(f"---------------------------------")

# 2. Encode categorical columns dynamically
print("\nEncoding lines and stations into machine-readable numeric IDs...")
le_station = LabelEncoder()
le_line = LabelEncoder()

df["station_id"] = le_station.fit_transform(df["station"])
df["line_id"] = le_line.fit_transform(df["line"])

# 3. Select features
FEATURES = [
    "hour",
    "day_of_week",
    "is_peak",
    "is_weekend",
    "is_interchange",
    "station_id",
    "line_id",
]

X = df[FEATURES]
y = df["crowd_level"]

# 4. Train/test split with stratification for perfect class distribution
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 5. Train model (n_jobs=-1 handles the larger dataset efficiently using all CPU cores)
print(f"\nTraining Random Forest Classifier on {len(X_train):,} rows...")
model = RandomForestClassifier(
    n_estimators=100, max_depth=15, random_state=42, n_jobs=-1
)
model.fit(X_train, y_train)

# 6. Evaluate
print("\nEvaluating model performance on unseen test data...")
preds = model.predict(X_test)
print(f"Overall Model Accuracy: {accuracy_score(y_test, preds):.4f}")

print("\nDetailed Classification Report:")
print(classification_report(y_test, preds))

# 7. Feature importance
importances = pd.Series(model.feature_importances_, index=FEATURES)
print("\nFeature Importances (Which features mattered most?):")
print(importances.sort_values(ascending=False).to_string())

# 8. Save artifacts safely
os.makedirs("model", exist_ok=True)
model_path = os.path.join("model", "model.pkl")

artifacts = {
    "model": model,
    "station_encoder": le_station,
    "line_encoder": le_line,
    "features": FEATURES,
    "classes": list(model.classes_),
}

with open(model_path, "wb") as f:
    pickle.dump(artifacts, f)

print(f"\nSUCCESS! Model pipeline saved to absolute path:\n{os.path.abspath(model_path)}")