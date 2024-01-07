"""
reducingCSV.py - CSV Dataset Size Reduction Script

This script reduces the size of a CSV dataset by randomly sampling a specified percentage of rows. It utilizes the pandas
library to read the input CSV file, randomly sample rows, and save the reduced dataset to a new CSV file.

Usage:
- Replace 0.5 with the desired percentage of rows to keep (e.g., 0.5 for 50%).
"""

import pandas as pd


if __name__ == "__main__":
    input_file = 'csvFolder/dataset.csv'
    output_file = 'csvFolder/dataset75.csv'
    percentage_to_keep = 0.75
    df = pd.read_csv(input_file)
    num_rows_to_keep = int(len(df) * percentage_to_keep)
    reduced_df = df.sample(n=num_rows_to_keep)
    reduced_df.to_csv(output_file, index=False)