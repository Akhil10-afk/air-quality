from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import csv
import os
from datetime import datetime

app = Flask(__name__)
model = joblib.load("model.pkl")

@app.route('/')
def home():
    return "Air Quality Prediction API is running! Use /predict to POST data or /dashboard to view logs."
@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    pm25 = data["pm25"]
    pm10 = data["pm10"]
    prediction = model.predict([[pm25, pm10]])[0]

    log_file = 'prediction_log.csv'
    file_exists = os.path.isfile(log_file)

    with open(log_file, 'a', newline='') as log:
        writer = csv.writer(log)
        if not file_exists:
            writer.writerow(['timestamp', 'pm25', 'pm10', 'predicted_aqi'])
        writer.writerow([datetime.now(), pm25, pm10, round(float(prediction), 2)])

    return jsonify({"predicted_aqi": round(float(prediction), 2)})

@app.route('/dashboard')
def dashboard():
    data = []
    timestamps, pm25_values, pm10_values, aqi_values = [], [], [], []

    try:
        with open('prediction_log.csv', newline='') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if len(row) == 4:
                    data.append(row)
                    timestamps.append(row[0])
                    pm25_values.append(float(row[1]))
                    pm10_values.append(float(row[2]))
                    aqi_values.append(float(row[3]))
    except FileNotFoundError:
        pass

    return render_template('dashboard.html',
                           data=data,
                           timestamps=timestamps,
                           pm25_values=pm25_values,
                           pm10_values=pm10_values,
                           aqi_values=aqi_values)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
