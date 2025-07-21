import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# Load preprocessed data
df = pd.read_csv("preprocessed_aqi.csv")

# Features and target
X = df[["PM2.5", "PM10"]]
y = df["AQI"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
print("📊 R^2 Score:", r2_score(y_test, y_pred))
print("📉 MSE:", mean_squared_error(y_test, y_pred))

# Save the model
joblib.dump(model, "model.pkl")
print("✅ Model saved as model.pkl")
