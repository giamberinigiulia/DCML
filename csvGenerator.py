"""
csvGenerator.py - CSV File Generator Utility

This script contains utility functions to flatten dictionaries, print values to a CSV file, and manage file paths.
It is used in various components of the system monitoring and anomaly detection project to handle CSV file operations.
"""

import csv
import os
from util import getDestinationFolder

""" elif isinstance(v, tuple):
            for i, item in enumerate(v):
                items.append((f"{new_key}{sep}{i}", item))"""


def flatten(d, parent_key='', sep='_'):
    items = []
    if isinstance(d, dict):  # check if it is a dict or a tuple
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k  # rename the field
            if isinstance(v, dict):
                items.extend(flatten(v, new_key, sep=sep).items())  # call again the function
            else:
                items.append((new_key, v))
    else:
        for i, item in enumerate(d):
            key = f"{parent_key}{sep}{i}" if parent_key else str(i)  # rename the field
            if isinstance(item, tuple):
                items += flatten(item, key, sep)  # call again the function
            else:
                items.append((key, item))
    return dict(items)


def printCsv(values, out_filename):
    destinationFolder = getDestinationFolder()
    if not os.path.exists(destinationFolder):
        os.makedirs(destinationFolder)
    out_filename = destinationFolder + out_filename

    file_exists = os.path.exists(out_filename)  # check if the file exists

    with open(out_filename, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=values.keys())
        if not file_exists or csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow(values)
