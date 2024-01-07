"""
liveMonitor.py - Real-Time System Monitoring with Anomaly Detection

This script provides a real-time monitoring solution with anomaly detection for system health.
It continuously monitors system metrics using the 'monitor_all' function and employs an anomaly detection model
loaded from 'anomaly_detector_model.pkl'.
The anomaly detection function filters out irrelevant data, predicts anomalies using the loaded model, and logs
warnings if anomalies are detected. It provides real-time feedback on the system's health, indicating whether it is
functioning correctly or if anomalies are detected.
"""
import logging
import time
import pandas as pd
from monitor import monitor_all
import pickle
from util import unchangingColumns


def detect_anomaly(new_data, loaded_model):
    my_dataframe = pd.DataFrame([new_data])
    prediction = loaded_model.predict(my_dataframe)[0]
    # the next part of the code (if..elif) is used only if the model is an unsupervised algorithm
    if prediction == 0:
        prediction_label = 'normal'
    elif prediction == 1:
        prediction_label = 'anomaly'
    else:
        prediction_label = prediction
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"{timestamp} - Detected: {prediction_label}"  # logging the result in the file
    logging.info(log_message)
    print(f"{timestamp} - Detected: {prediction_label}")
    if prediction_label == 'anomaly':
        print("System may not be working correctly.")
    else:
        print("System is working correctly.")


def liveMonitor(anomalies):
    with open('anomaly_detector/anomaly_detector_model.pkl', 'rb') as model_file:
        loaded_model = pickle.load(model_file)  # loading the model

    logging.basicConfig(filename=anomalies, level=logging.INFO, format='%(asctime)s - %(message)s')

    while True:
        new_data = monitor_all()  # capturing datas from the system
        excluded_columns = ["timestamp", "label"] + (unchangingColumns())  # find the columns with less variation
        filtered_dict = {key: value for key, value in new_data.items() if key not in excluded_columns}
        detect_anomaly(filtered_dict, loaded_model)  # using the observation and the model to detect anomalies


if __name__ == "__main__":
    liveMonitor("anomaly_detector/anomaly_detection_log.txt")
