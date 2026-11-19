# Step 3 - Feature Engineering (Encoding categorical variables + feature selection)

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import os

# load cleaned data
data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "employee_attrition_cleaned.csv")
df = pd.read_csv(data_path)

print("--- Feature Engineering ---\n")

# 1. Label Encoding - for columns that have an order or are binary

# EducationLevel has a natural order so we map it manually
edu_map = {"High School": 0, "Bachelor": 1, "Master": 2, "PhD": 3}
df["EducationLevel_Encoded"] = df["EducationLevel"].map(edu_map)
print(f"EducationLevel mapping: {edu_map}")

# for binary columns we can use LabelEncoder from sklearn
le = LabelEncoder()

df["Attrition_Encoded"] = le.fit_transform(df["Attrition"])
print(f"Attrition: No=0, Yes=1")

df["OverTime_Encoded"] = le.fit_transform(df["OverTime"])
print(f"OverTime: No=0, Yes=1")

df["Gender_Encoded"] = le.fit_transform(df["Gender"])
print(f"Gender: Female=0, Male=1")

# 2. One-Hot Encoding - for Department (no natural order)
print(f"\nDepartment values: {df['Department'].unique()}")
df = pd.get_dummies(df, columns=["Department"], prefix="Dept", dtype=int)

dept_cols = [c for c in df.columns if c.startswith("Dept_")]
print(f"One-hot encoded columns created: {dept_cols}")

# 3. Correlation analysis - to see which features relate to attrition
print("\n--- Correlation with Attrition ---")
numeric_df = df.select_dtypes(include=[np.number])
if "EmployeeID" in numeric_df.columns:
    numeric_df = numeric_df.drop(columns=["EmployeeID"])

corr_with_target = numeric_df.corr()["Attrition_Encoded"].drop("Attrition_Encoded").sort_values(ascending=False)
print(corr_with_target)

# check for highly correlated pairs (multicollinearity)
print("\nChecking for highly correlated feature pairs (|r| > 0.7):")
corr_matrix = numeric_df.corr()
found_any = False
for i in range(len(corr_matrix.columns)):
    for j in range(i + 1, len(corr_matrix.columns)):
        r = corr_matrix.iloc[i, j]
        if abs(r) > 0.7:
            print(f"  {corr_matrix.columns[i]} <-> {corr_matrix.columns[j]}: {r:.4f}")
            found_any = True
if not found_any:
    print("  None found - that's good!")

# drop original text columns since we have encoded versions now
df = df.drop(columns=["Gender", "EducationLevel", "OverTime", "Attrition", "EmployeeID"], errors="ignore")

print(f"\nFinal columns ({len(df.columns)}): {list(df.columns)}")

# save
output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "employee_attrition_encoded.csv")
df.to_csv(output_path, index=False)
print(f"Saved to: {output_path}")
