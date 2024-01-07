"""
labeling.py - Dataset Labeling for Anomaly Detection

This script reads monitored data from 'csvFolder/monitorResult.csv' and injection timestamps from
'csvFolder/injection_timestamps.csv'. It labels anomalies based on whether the timestamps fall within the injection
periods. The labeled dataset is then saved to 'csvFolder/dataset.csv' with an additional 'label' column indicating
'normal' or 'anomaly' for each observation.
"""

import csv


def labeling(data_csv_file='csvFolder/monitorResult.csv',
             injection_timestamps_csv_file='csvFolder/injection_timestamps.csv',
             output_csv_file='csvFolder/dataset.csv'):
    injection_timestamps = []
    with open(injection_timestamps_csv_file, 'r') as ts_file:
        reader = csv.DictReader(ts_file)
        for row in reader:
            start_time = int(row['start_time'])
            end_time = int(row['end_time'])
            injection_timestamps.append((start_time, end_time))  # saving all the timestamp in a list

    with open(data_csv_file, 'r') as data_file:
        reader = csv.DictReader(data_file)
        labeled_data = []  # create a list to store labeled data
        for row in reader:
            timestamp = int(row['timestamp'])
            is_anomaly = any(start_time <= timestamp <= end_time for start_time, end_time in
                             injection_timestamps)  # check if the timestamp falls between any injection timestamps
            row['label'] = 'anomaly' if is_anomaly else 'normal'  # add the 'label' column to the row based on anomaly
            # detection
            labeled_data.append(row)  # append the labeled row to the list

    fieldnames = list(reader.fieldnames) + ['label']  # write the labeled data to a new CSV file

    with open(output_csv_file, 'w', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(labeled_data)


if __name__ == "__main__":
    labeling()
