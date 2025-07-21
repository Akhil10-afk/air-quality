import requests

API_KEY = "8d3c00147209220507da1d0ae9475985"  # Replace with your working key

cities = {
    "Hyderabad": (17.3850, 78.4867),
    "Mumbai": (19.0760, 72.8777),
    "Delhi": (28.7041, 77.1025),
    "Bengaluru": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707)
}

for city, (lat, lon) in cities.items():
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        aqi = data["list"][0]["main"]["aqi"]
        pm25 = data["list"][0]["components"]["pm2_5"]
        pm10 = data["list"][0]["components"]["pm10"]
        print(f"\n📍 {city}")
        print(f"AQI: {aqi} | PM2.5: {pm25} | PM10: {pm10}")
    else:
        print(f"\nFailed to fetch data for {city}. Status: {response.status_code}")
