import requests

API_KEY = "8d3c00147209220507da1d0ae9475985"
LAT = 17.3850   # Latitude of Hyderabad
LON = 78.4867   # Longitude of Hyderabad

url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={LAT}&lon={LON}&appid={API_KEY}"

response = requests.get(url)

print("Status Code:", response.status_code)
print("Response Text:")
print(response.text)
