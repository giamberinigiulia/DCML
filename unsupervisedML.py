"""
unsupervisedML.py
This script is focused on training various anomaly detection models on a dataset.
It reads a CSV dataset, splits it into training and testing sets, and then trains multiple anomaly detection models
using the PyOD library.
The training function iterates through different configurations of the anomaly detection models, measures training and
testing durations, computes accuracy, and prints the results. The results are then stored in a list for further analysis
or comparison.
"""
import os
import pickle

import pandas
import sklearn
from pyod.models.abod import ABOD
from pyod.models.copod import COPOD
from pyod.models.hbos import HBOS
from sklearn.model_selection import train_test_split
from util import current_ms, getDestinationFolder, unchangingColumns


def training():
    my_df = pandas.read_csv(getDestinationFolder() + "dataset.csv", sep=',')

    y = my_df["label"].map({'normal': 0, 'anomaly': 1})
    x = my_df.drop(columns=["timestamp", "label"] + (
        unchangingColumns()))  # filter the dataset excluding the columns with less variation

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, shuffle=False)  # splitting the dataset
    classifiers = [HBOS(alpha=0.01, contamination=0.1, n_bins=20),
                   HBOS(alpha=0.5, contamination=0.5, n_bins=5),
                   HBOS(alpha=0.01, contamination=0.1, n_bins=45),
                   HBOS(alpha=0.1, contamination=0.3, n_bins=100),
                   ABOD(contamination=0.5),
                   ABOD(contamination=0.1),
                   ABOD(contamination=0.001),
                   ABOD(contamination=0.000000001),
                   COPOD(contamination=0.1)]
    clf_results = []
    for i, clf in enumerate(classifiers):
        start_time_training = current_ms()
        clf = clf.fit(x_train)
        end_time_training = current_ms()
        predicted_labels = clf.predict(x_test)
        end_time = current_ms()
        accuracy = sklearn.metrics.accuracy_score(y_test, predicted_labels)
        print(f"Classifier: {classifiers[i]}, Accuracy: {accuracy}, "
              f"Training duration: {end_time_training - start_time_training}, Testing duration: {end_time - end_time_training}")
        clf_results.append({
            'classifier': classifiers[i],
            'accuracy': accuracy,
            'training_duration': end_time_training - start_time_training,
            'testing_duration': end_time - end_time_training
        })
    model = findBest(clf_results)
    clf_model = model['classifier'].fit(x_train)
    if not os.path.exists("anomaly_detector"):
        os.makedirs("anomaly_detector")
    with open('anomaly_detector/anomaly_detector_model.pkl', 'wb') as model_file:
        pickle.dump(clf_model, model_file)
    return clf_results


def findBest(results):
    best = {'classifier': "", 'accuracy': 0}
    for r in results:
        if r['accuracy'] > best['accuracy']:
            best['accuracy'] = r['accuracy']
            best['classifier'] = r['classifier']
    print("The best classifier is: ", best['classifier'], "with accuracy: ", best['accuracy'])
    return best


if __name__ == "__main__":
    training()
