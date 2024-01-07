"""
util.py - Utility Functions for Monitoring System

This module provides utility functions used in the monitoring system. It includes functions for flattening nested dictionaries
and printing values to a CSV file. These utilities are designed to support various aspects of the system, such as data
processing and file output.

Functions:
- `flatten_dict`: Recursively flattens nested dictionaries into a flat structure, handling tuples as well.
- `printCsv`: Writes values to a CSV file, creating the file and header if necessary.
"""

import time
import sys

import pandas as pd


def current_ms():
    return round(time.time() * 1000)


def getDestinationFolder():
    return "csvFolder/"


def print_progress_bar(iteration, total, prefix='', suffix='', length=50, fill='█', print_end='\r'):
    percent = "{0:.1f}".format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)

    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}', )
    sys.stdout.flush()


def unchangingColumns():
    df = pd.read_csv("csvFolder/monitorResult.csv")
    low_variation_columns = [col for col in df.columns if df[col].nunique() <= len(df) * 0.05]
    return low_variation_columns

