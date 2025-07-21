import requests
import csv
import time

API_KEY = "8d3c00147209220507da1d0ae9475985"  # Your API key

cities = {
    "Hyderabad": (17.3850, 78.4867),
    "Mumbai": (19.0760, 72.8777),
    "Delhi": (28.7041, 77.1025),
    "Bengaluru": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707)
}

filename = "aqi_dataset.csv"

with open(filename, "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["City", "Lat", "Lon", "AQI", "PM2.5", "PM10"])  # CSV header
    
    for city, (lat, lon) in cities.items():
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            aqi = data["list"][0]["main"]["aqi"]
            pm25 = data["list"][0]["components"]["pm2_5"]
            pm10 = data["list"][0]["components"]["pm10"]
            writer.writerow([city, lat, lon, aqi, pm25, pm10])
            print(f"✅ {city} data written.")
        else:
            print(f"❌ Failed to fetch data for {city}. Status code: {response.status_code}")
        
        time.sleep(1)  # To avoid hitting rate limits
