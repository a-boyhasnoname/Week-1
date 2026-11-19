# Step 2 - Cleaning the data

import pandas as pd
import numpy as np
import os

# load data
data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "employee_attrition.csv")
df = pd.read_csv(data_path)

print("--- Data Cleaning ---\n")
print(f"Original shape: {df.shape}")

# 1. Remove duplicates
print(f"\nDuplicates found: {df.duplicated().sum()}")
df = df.drop_duplicates().reset_index(drop=True)
print(f"Shape after removing duplicates: {df.shape}")

# 2. Fix inconsistent categorical values
# Gender - there's Male, male, M, Female, female, F - need to make them consistent
print(f"\nGender before cleaning: {df['Gender'].unique()}")
df["Gender"] = df["Gender"].replace({"male": "Male", "female": "Female", "M": "Male", "F": "Female"})
print(f"Gender after cleaning: {df['Gender'].unique()}")

# Department - has mixed case like 'engineering' and 'Engineering'
print(f"\nDepartment before: {df['Department'].unique()}")
df["Department"] = df["Department"].str.strip().str.title()
print(f"Department after: {df['Department'].unique()}")

# OverTime - same issue
print(f"\nOverTime before: {df['OverTime'].unique()}")
df["OverTime"] = df["OverTime"].replace({"yes": "Yes", "no": "No", "YES": "Yes", "NO": "No"})
print(f"OverTime after: {df['OverTime'].unique()}")

# 3. Handle missing values
print(f"\n--- Missing values ---")
print(df.isnull().sum()[df.isnull().sum() > 0])

# for numeric columns - fill with median (better than mean because of outliers)
numeric_cols = ["Age", "YearsAtCompany", "MonthlySalary", "SatisfactionScore", "DistanceFromHome"]
for col in numeric_cols:
    if df[col].isnull().sum() > 0:
        med = df[col].median()
        df[col] = df[col].fillna(med)
        print(f"  Filled {col} missing values with median: {med}")

# for categorical columns - fill with mode (most common value)
cat_cols = ["Department", "EducationLevel"]
for col in cat_cols:
    if df[col].isnull().sum() > 0:
        most_common = df[col].mode()[0]
        df[col] = df[col].fillna(most_common)
        print(f"  Filled {col} missing values with mode: {most_common}")

print(f"\nMissing values remaining: {df.isnull().sum().sum()}")

# 4. Handle outliers using IQR method
print("\n--- Outlier detection (IQR method) ---")
for col in ["MonthlySalary", "Age", "YearsAtCompany", "DistanceFromHome"]:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = ((df[col] < lower) | (df[col] > upper)).sum()
    if outliers > 0:
        # clip/cap the outliers instead of removing them
        df[col] = df[col].clip(lower=lower, upper=upper)
        print(f"  {col}: found {outliers} outliers, capped to [{lower:.2f}, {upper:.2f}]")
    else:
        print(f"  {col}: no outliers found")

# save cleaned data
output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "employee_attrition_cleaned.csv")
df.to_csv(output_path, index=False)

print(f"\nCleaned data saved to: {output_path}")
print(f"Final shape: {df.shape}")
