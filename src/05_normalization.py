# Step 4 - Normalization and Scaling

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import os

# load encoded data
data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "employee_attrition_encoded.csv")
df = pd.read_csv(data_path)

print("--- Normalization & Scaling ---\n")

# these are the continuous columns we want to scale
cols_to_scale = ["Age", "YearsAtCompany", "MonthlySalary", "SatisfactionScore", "DistanceFromHome"]

print("Before scaling:")
print(df[cols_to_scale].describe().round(2))

# Method 1: Min-Max Scaling (puts everything between 0 and 1)
# formula: (x - min) / (max - min)
print("\n\n--- Min-Max Scaling ---")
minmax = MinMaxScaler()
df_minmax = df.copy()
df_minmax[cols_to_scale] = minmax.fit_transform(df[cols_to_scale])
print(df_minmax[cols_to_scale].describe().round(3))

# Method 2: Standard Scaling (mean becomes 0, std becomes 1)
# formula: (x - mean) / std
print("\n--- Standard Scaling (Z-score) ---")
standard = StandardScaler()
df_standard = df.copy()
df_standard[cols_to_scale] = standard.fit_transform(df[cols_to_scale])
print(df_standard[cols_to_scale].describe().round(3))

# comparing the ranges
print("\n--- Comparison ---")
print(f"{'Column':<22} {'Original':>16} {'Min-Max':>16} {'Standard':>16}")
print("-" * 72)
for col in cols_to_scale:
    orig = f"[{df[col].min():.1f}, {df[col].max():.1f}]"
    mm = f"[{df_minmax[col].min():.3f}, {df_minmax[col].max():.3f}]"
    std = f"[{df_standard[col].min():.3f}, {df_standard[col].max():.3f}]"
    print(f"{col:<22} {orig:>16} {mm:>16} {std:>16}")

# saving the min-max version since its more commonly used
output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "employee_attrition_normalized.csv")
df_minmax.to_csv(output_path, index=False)
print(f"\nSaved normalized data to: {output_path}")

print("\nNote: Min-Max is good when you need values in [0,1]")
print("      Standard scaling is good when algorithm expects normal distribution")
