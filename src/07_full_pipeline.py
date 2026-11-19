# Full preprocessing pipeline - combines all steps into one script

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import os
import warnings
warnings.filterwarnings("ignore")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_PATH = os.path.join(BASE_DIR, "data", "employee_attrition.csv")
FINAL_PATH = os.path.join(BASE_DIR, "data", "employee_attrition_final.csv")

print("=== Complete Preprocessing Pipeline ===\n")

# --- Step 1: Load data ---
df = pd.read_csv(RAW_PATH)
print(f"Loaded data: {df.shape}")
print(f"Missing values: {df.isnull().sum().sum()}")
print(f"Duplicates: {df.duplicated().sum()}")

# --- Step 2: Remove duplicates ---
before = len(df)
df = df.drop_duplicates().reset_index(drop=True)
print(f"\nRemoved {before - len(df)} duplicates -> {len(df)} rows")

# --- Step 3: Standardize categorical values ---
df["Gender"] = df["Gender"].replace({"male": "Male", "female": "Female", "M": "Male", "F": "Female"})
df["Department"] = df["Department"].str.strip().str.title()
df["OverTime"] = df["OverTime"].replace({"yes": "Yes", "no": "No", "YES": "Yes", "NO": "No"})
print("Standardized categorical values")

# --- Step 4: Fill missing values ---
# numeric -> median, categorical -> mode
for col in ["Age", "YearsAtCompany", "MonthlySalary", "SatisfactionScore", "DistanceFromHome"]:
    if df[col].isnull().sum() > 0:
        df[col] = df[col].fillna(df[col].median())

for col in ["Department", "EducationLevel"]:
    if df[col].isnull().sum() > 0:
        df[col] = df[col].fillna(df[col].mode()[0])

print(f"Filled missing values (remaining: {df.isnull().sum().sum()})")

# --- Step 5: Handle outliers ---
for col in ["MonthlySalary", "Age", "YearsAtCompany", "DistanceFromHome"]:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers = ((df[col] < lower) | (df[col] > upper)).sum()
    if outliers > 0:
        df[col] = df[col].clip(lower=lower, upper=upper)
        print(f"  Capped {outliers} outliers in {col}")

# --- Step 6: Encode features ---
# ordinal encoding for education
df["EducationLevel_Encoded"] = df["EducationLevel"].map(
    {"High School": 0, "Bachelor": 1, "Master": 2, "PhD": 3}
)

# label encoding for binary columns
le = LabelEncoder()
df["Attrition_Encoded"] = le.fit_transform(df["Attrition"])
df["OverTime_Encoded"] = le.fit_transform(df["OverTime"])
df["Gender_Encoded"] = le.fit_transform(df["Gender"])

# one-hot encoding for department
df = pd.get_dummies(df, columns=["Department"], prefix="Dept", dtype=int)

# drop original text columns
df = df.drop(columns=["Gender", "EducationLevel", "OverTime", "Attrition", "EmployeeID"], errors="ignore")
print(f"Encoded features: {list(df.columns)}")

# --- Step 7: Normalize ---
cols_to_scale = ["Age", "YearsAtCompany", "MonthlySalary", "SatisfactionScore", "DistanceFromHome"]
scaler = MinMaxScaler()
df[cols_to_scale] = scaler.fit_transform(df[cols_to_scale])
print("Normalized numeric features to [0, 1]")

# --- Save ---
df.to_csv(FINAL_PATH, index=False)
print(f"\nFinal dataset saved: {FINAL_PATH}")
print(f"Shape: {df.shape}")
print("\nPipeline complete! Dataset is ready for ML.")
print("\nSample:")
print(df.head())
