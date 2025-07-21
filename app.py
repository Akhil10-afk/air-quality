from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import csv
import os
from datetime import datetime
import requests
from pytz import timezone

app = Flask(__name__)
model = joblib.load("model.pkl")

@app.route('/')
def home():
    return "Air Quality Prediction API is running! Use /predict to POST data, /form to input manually, /auto_predict for live data, or /dashboard to view logs."

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    pm25 = data["pm25"]
    pm10 = data["pm10"]
    prediction = model.predict([[pm25, pm10]])[0]

    ist = timezone('Asia/Kolkata')
    timestamp = datetime.now(ist).strftime("%Y-%m-%d %I:%M:%S %p")

    log_file = 'prediction_log.csv'
    file_exists = os.path.isfile(log_file)

    with open(log_file, 'a', newline='') as log:
        writer = csv.writer(log)
        if not file_exists:
            writer.writerow(['timestamp', 'pm25', 'pm10', 'predicted_aqi'])
        writer.writerow([timestamp, pm25, pm10, round(float(prediction), 2)])

    return jsonify({"predicted_aqi": round(float(prediction), 2)})

@app.route('/auto_predict')
def auto_predict():
    pm25, pm10 = get_live_pm_values()
    if pm25 is None or pm10 is None:
        return jsonify({"error": "Live data unavailable."})

    prediction = model.predict([[pm25, pm10]])[0]

    ist = timezone('Asia/Kolkata')
    timestamp = datetime.now(ist).strftime("%Y-%m-%d %I:%M:%S %p")

    log_file = 'prediction_log.csv'
    file_exists = os.path.isfile(log_file)

    with open(log_file, 'a', newline='') as log:
        writer = csv.writer(log)
        if not file_exists:
            writer.writerow(['timestamp', 'pm25', 'pm10', 'predicted_aqi'])
        writer.writerow([timestamp, pm25, pm10, round(float(prediction), 2)])

    return jsonify({
        "live_pm25": pm25,
        "live_pm10": pm10,
        "predicted_aqi": round(float(prediction), 2)
    })

def get_live_pm_values(city="Hyderabad"):
    try:
        url = f"https://api.openaq.org/v3/latest?city={city}&parameter=pm25,pm10"
        response = requests.get(url)
        response.raise_for_status()
        results = response.json().get("results", [])

        for location in results:
            pm25 = pm10 = None
            for m in location.get("measurements", []):
                if m["parameter"] == "pm25":
                    pm25 = m["value"]
                elif m["parameter"] == "pm10":
                    pm10 = m["value"]
            if pm25 is not None and pm10 is not None:
                return pm25, pm10
    except Exception as e:
        print("❌ Error fetching live data:", e)
        return None, None

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
