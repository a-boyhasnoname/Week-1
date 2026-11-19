# Step 1 - Loading and inspecting the dataset

import pandas as pd
import numpy as np
import os

# load csv file
data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "employee_attrition.csv")
df = pd.read_csv(data_path)

print("--- Data Loading and Inspection ---\n")

# checking shape
print(f"Number of rows: {df.shape[0]}")
print(f"Number of columns: {df.shape[1]}")

# looking at first few rows
print("\nFirst 5 rows:")
print(df.head())

# data types
print("\nData types:")
print(df.dtypes)

# basic info
print("\nDataset info:")
df.info()

# statistics for numbers
print("\nStatistics (numeric):")
print(df.describe())

# statistics for text columns
print("\nStatistics (categorical):")
print(df.describe(include="object"))

# checking missing values
print("\nMissing values:")
missing = df.isnull().sum()
print(missing[missing > 0])

# checking duplicates
print(f"\nDuplicate rows: {df.duplicated().sum()}")

# checking unique values in text columns
print("\nUnique values in each categorical column:")
for col in df.select_dtypes(include="object").columns:
    print(f"  {col}: {df[col].unique()}")

print("\n--- Issues found ---")
print("1. There are missing values in several columns")
print("2. Some duplicate rows exist")
print("3. Gender, Department, OverTime have inconsistent values (like 'Male' vs 'male' vs 'M')")
print("4. MonthlySalary has some suspicious extreme values")
