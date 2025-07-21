import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Updated path
file_path = "aqi_dataset.csv"

df = pd.read_csv(file_path)

scaler = MinMaxScaler()
df[["AQI", "PM2.5", "PM10"]] = scaler.fit_transform(df[["AQI", "PM2.5", "PM10"]])

df.to_csv("preprocessed_aqi.csv", index=False)

print("✅ Preprocessing complete. Saved as 'preprocessed_aqi.csv'")
