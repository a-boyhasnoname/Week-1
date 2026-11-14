"""
Step 1: Data Loading & Inspection

This script demonstrates how to:
- Load a CSV dataset using Pandas
- Inspect dataset structure, shape, and data types
- Generate initial statistical summaries
- Identify potential data quality issues
"""

import pandas as pd
import numpy as np
import os

# ─── 1.1 Load the dataset ───
data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "employee_attrition.csv")
df = pd.read_csv(data_path)

print("=" * 70)
print("STEP 1: DATA LOADING & INSPECTION")
print("=" * 70)

# ─── 1.2 Basic dataset info ───
print("\n📋 Dataset Shape:")
print(f"   Rows: {df.shape[0]}, Columns: {df.shape[1]}")

print("\n📋 Column Names and Data Types:")
print(df.dtypes.to_string())

print("\n📋 First 5 Rows:")
print(df.head().to_string())

print("\n📋 Last 5 Rows:")
print(df.tail().to_string())

# ─── 1.3 Dataset info (memory, non-null counts) ───
print("\n📋 Dataset Info:")
df.info()

# ─── 1.4 Statistical summary for numeric columns ───
print("\n📊 Statistical Summary (Numeric Columns):")
print(df.describe().to_string())

# ─── 1.5 Statistical summary for categorical columns ───
print("\n📊 Statistical Summary (Categorical Columns):")
print(df.describe(include="object").to_string())

# ─── 1.6 Check for missing values ───
print("\n⚠️  Missing Values per Column:")
missing = df.isnull().sum()
missing_pct = (df.isnull().sum() / len(df) * 100).round(2)
missing_df = pd.DataFrame({"Missing Count": missing, "Missing %": missing_pct})
print(missing_df[missing_df["Missing Count"] > 0].to_string())

# ─── 1.7 Check for duplicate rows ───
duplicates = df.duplicated().sum()
print(f"\n⚠️  Duplicate Rows: {duplicates}")

# ─── 1.8 Unique values in categorical columns ───
print("\n📊 Unique Values in Categorical Columns:")
for col in df.select_dtypes(include="object").columns:
    print(f"   {col}: {df[col].nunique()} unique → {df[col].unique()}")

print("\n" + "=" * 70)
print("INSPECTION COMPLETE — Issues identified for cleaning:")
print("  1. Missing values in multiple columns")
print("  2. Duplicate rows present")
print("  3. Inconsistent categorical values (mixed case)")
print("  4. Potential outliers in numeric columns")
print("=" * 70)
