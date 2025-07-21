import requests

API_KEY = "8d3c00147209220507da1d0ae9475985"  # Make sure this is the same working key
LAT = 17.3850   # Hyderabad latitude
LON = 78.4867   # Hyderabad longitude

url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={LAT}&lon={LON}&appid={API_KEY}"

response = requests.get(url)

print("Status Code:", response.status_code)

if response.status_code == 200:
    data = response.json()
    aqi = data['list'][0]['main']['aqi']
    pm25 = data['list'][0]['components']['pm2_5']
    pm10 = data['list'][0]['components']['pm10']
    print(f"AQI Level: {aqi}")
    print(f"PM2.5: {pm25}")
    print(f"PM10: {pm10}")
else:
    print("Failed to fetch data:", response.text)
