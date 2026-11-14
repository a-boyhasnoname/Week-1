"""
Step 2: Data Cleaning

This script demonstrates how to:
- Remove duplicate rows
- Standardize inconsistent categorical values
- Handle missing values using different strategies:
    • Mean/Median imputation for numeric columns
    • Mode imputation for categorical columns
- Detect and handle outliers using the IQR method
"""

import pandas as pd
import numpy as np
import os

# ─── Load raw dataset ───
data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "employee_attrition.csv")
df = pd.read_csv(data_path)

print("=" * 70)
print("STEP 2: DATA CLEANING")
print("=" * 70)
print(f"\n📋 Original dataset shape: {df.shape}")

# ═══════════════════════════════════════════════════════════════════════
# 2.1 REMOVE DUPLICATE ROWS
# ═══════════════════════════════════════════════════════════════════════
duplicates_before = df.duplicated().sum()
df.drop_duplicates(inplace=True)
df.reset_index(drop=True, inplace=True)
print(f"\n✅ Removed {duplicates_before} duplicate rows → New shape: {df.shape}")

# ═══════════════════════════════════════════════════════════════════════
# 2.2 STANDARDIZE CATEGORICAL VALUES
# ═══════════════════════════════════════════════════════════════════════
print("\n--- Standardizing Categorical Columns ---")

# Gender: Map all variations to 'Male' / 'Female'
print(f"   Gender before: {df['Gender'].unique()}")
gender_map = {"male": "Male", "female": "Female", "M": "Male", "F": "Female"}
df["Gender"] = df["Gender"].replace(gender_map)
print(f"   Gender after:  {df['Gender'].unique()}")

# Department: Standardize to title case
print(f"   Department before: {df['Department'].unique()}")
df["Department"] = df["Department"].str.strip().str.title()
print(f"   Department after:  {df['Department'].unique()}")

# OverTime: Standardize to 'Yes' / 'No'
print(f"   OverTime before: {df['OverTime'].unique()}")
overtime_map = {"yes": "Yes", "no": "No", "YES": "Yes", "NO": "No"}
df["OverTime"] = df["OverTime"].replace(overtime_map)
print(f"   OverTime after:  {df['OverTime'].unique()}")

print("✅ Categorical values standardized")

# ═══════════════════════════════════════════════════════════════════════
# 2.3 HANDLE MISSING VALUES
# ═══════════════════════════════════════════════════════════════════════
print("\n--- Handling Missing Values ---")
print("Missing values before imputation:")
print(df.isnull().sum()[df.isnull().sum() > 0].to_string())

# Strategy for numeric columns: Use MEDIAN (robust to outliers)
numeric_cols_with_missing = ["Age", "YearsAtCompany", "MonthlySalary",
                              "SatisfactionScore", "DistanceFromHome"]

for col in numeric_cols_with_missing:
    if df[col].isnull().sum() > 0:
        median_val = df[col].median()
        df[col].fillna(median_val, inplace=True)
        print(f"   {col}: filled {col} NaNs with median = {median_val:.2f}")

# Strategy for categorical columns: Use MODE (most frequent value)
categorical_cols_with_missing = ["Department", "EducationLevel"]

for col in categorical_cols_with_missing:
    if df[col].isnull().sum() > 0:
        mode_val = df[col].mode()[0]
        df[col].fillna(mode_val, inplace=True)
        print(f"   {col}: filled NaNs with mode = '{mode_val}'")

print("\nMissing values after imputation:")
print(f"   Total missing: {df.isnull().sum().sum()}")
print("✅ All missing values handled")

# ═══════════════════════════════════════════════════════════════════════
# 2.4 DETECT AND HANDLE OUTLIERS (IQR Method)
# ═══════════════════════════════════════════════════════════════════════
print("\n--- Detecting Outliers using IQR Method ---")

def detect_outliers_iqr(dataframe, column):
    """Detect outliers using the Interquartile Range (IQR) method."""
    Q1 = dataframe[column].quantile(0.25)
    Q3 = dataframe[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = dataframe[(dataframe[column] < lower_bound) | (dataframe[column] > upper_bound)]
    return outliers, lower_bound, upper_bound

# Check outliers in key numeric columns
outlier_cols = ["MonthlySalary", "Age", "YearsAtCompany", "DistanceFromHome"]

for col in outlier_cols:
    outliers, lower, upper = detect_outliers_iqr(df, col)
    print(f"\n   {col}:")
    print(f"      IQR Bounds: [{lower:.2f}, {upper:.2f}]")
    print(f"      Outliers found: {len(outliers)}")

    if len(outliers) > 0:
        # Cap outliers at the boundaries (Winsorization)
        df[col] = df[col].clip(lower=lower, upper=upper)
        print(f"      ✅ Outliers capped (Winsorized) to [{lower:.2f}, {upper:.2f}]")

# ─── Save cleaned dataset ───
output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "employee_attrition_cleaned.csv")
df.to_csv(output_path, index=False)

print(f"\n{'=' * 70}")
print(f"CLEANING COMPLETE")
print(f"   Cleaned dataset saved: {output_path}")
print(f"   Final shape: {df.shape}")
print(f"   Missing values: {df.isnull().sum().sum()}")
print(f"   Duplicate rows: {df.duplicated().sum()}")
print(f"{'=' * 70}")
