import pandas as pd

# Load your raw CSV
df = pd.read_csv("raw_aqi_data.csv")  # 👈 replace with your actual filename

# Keep only necessary columns
df = df[["AQI", "PM2.5", "PM10"]]

# Drop rows with any missing values
df = df.dropna()

# Optionally: drop rows where AQI is 0 (if many rows have AQI=0 due to bad data)
df = df[df["AQI"] > 0]

# Save cleaned data
df.to_csv("preprocessed_aqi.csv", index=False)

print("✅ Cleaned data saved to preprocessed_aqi.csv")
