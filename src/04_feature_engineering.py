"""
Step 3: Feature Engineering — Encoding Categorical Variables & Feature Selection

This script demonstrates how to:
- Apply Label Encoding for ordinal categorical variables
- Apply One-Hot Encoding for nominal categorical variables
- Perform basic feature selection using correlation analysis
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import os

# ─── Load cleaned dataset ───
data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "employee_attrition_cleaned.csv")
df = pd.read_csv(data_path)

print("=" * 70)
print("STEP 3: FEATURE ENGINEERING")
print("=" * 70)

# ═══════════════════════════════════════════════════════════════════════
# 3.1 LABEL ENCODING (for ordinal variables)
# ═══════════════════════════════════════════════════════════════════════
print("\n--- 3.1 Label Encoding (Ordinal Variables) ---")

# EducationLevel has a natural order: High School < Bachelor < Master < PhD
education_order = {"High School": 0, "Bachelor": 1, "Master": 2, "PhD": 3}
df["EducationLevel_Encoded"] = df["EducationLevel"].map(education_order)
print(f"   EducationLevel mapping: {education_order}")
print(f"   Sample values: {df[['EducationLevel', 'EducationLevel_Encoded']].head(8).to_string()}")

# Attrition: Yes/No → 1/0 (binary target)
le_attrition = LabelEncoder()
df["Attrition_Encoded"] = le_attrition.fit_transform(df["Attrition"])
print(f"\n   Attrition: {dict(zip(le_attrition.classes_, le_attrition.transform(le_attrition.classes_)))}")

# OverTime: Yes/No → 1/0
le_overtime = LabelEncoder()
df["OverTime_Encoded"] = le_overtime.fit_transform(df["OverTime"])
print(f"   OverTime: {dict(zip(le_overtime.classes_, le_overtime.transform(le_overtime.classes_)))}")

# Gender: Male/Female → 1/0
le_gender = LabelEncoder()
df["Gender_Encoded"] = le_gender.fit_transform(df["Gender"])
print(f"   Gender: {dict(zip(le_gender.classes_, le_gender.transform(le_gender.classes_)))}")

print("✅ Label encoding complete")

# ═══════════════════════════════════════════════════════════════════════
# 3.2 ONE-HOT ENCODING (for nominal variables)
# ═══════════════════════════════════════════════════════════════════════
print("\n--- 3.2 One-Hot Encoding (Nominal Variables) ---")

# Department has no natural order → use One-Hot Encoding
print(f"   Department unique values: {df['Department'].unique()}")
df_encoded = pd.get_dummies(df, columns=["Department"], prefix="Dept", dtype=int)
dept_cols = [col for col in df_encoded.columns if col.startswith("Dept_")]
print(f"   Created columns: {dept_cols}")
print(f"   Sample one-hot encoding:")
print(df_encoded[["EmployeeID"] + dept_cols].head(5).to_string())

print("✅ One-hot encoding complete")

# ═══════════════════════════════════════════════════════════════════════
# 3.3 FEATURE SELECTION — Correlation Analysis
# ═══════════════════════════════════════════════════════════════════════
print("\n--- 3.3 Feature Selection (Correlation Analysis) ---")

# Select numeric columns for correlation
numeric_cols = df_encoded.select_dtypes(include=[np.number]).columns.tolist()
# Remove EmployeeID as it's just an identifier
if "EmployeeID" in numeric_cols:
    numeric_cols.remove("EmployeeID")

correlation_matrix = df_encoded[numeric_cols].corr()

# Show correlations with the target variable (Attrition_Encoded)
print("\n   Correlation with Attrition (target):")
target_corr = correlation_matrix["Attrition_Encoded"].drop("Attrition_Encoded").sort_values(ascending=False)
for feature, corr in target_corr.items():
    bar = "█" * int(abs(corr) * 40)
    sign = "+" if corr > 0 else "-"
    print(f"      {feature:<25} {sign}{abs(corr):.4f}  {bar}")

# Identify highly correlated feature pairs (potential multicollinearity)
print("\n   Highly Correlated Feature Pairs (|r| > 0.7):")
found = False
for i in range(len(numeric_cols)):
    for j in range(i + 1, len(numeric_cols)):
        corr = correlation_matrix.iloc[i, j]
        if abs(corr) > 0.7:
            print(f"      {numeric_cols[i]} ↔ {numeric_cols[j]}: {corr:.4f}")
            found = True
if not found:
    print("      No highly correlated pairs found (good!)")

# ─── Drop original categorical columns, keep encoded versions ───
cols_to_drop = ["Gender", "EducationLevel", "OverTime", "Attrition", "EmployeeID"]
df_final = df_encoded.drop(columns=cols_to_drop, errors="ignore")

print(f"\n   Final feature set ({len(df_final.columns)} columns): {list(df_final.columns)}")

# ─── Save ───
output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "employee_attrition_encoded.csv")
df_final.to_csv(output_path, index=False)
print(f"\n✅ Encoded dataset saved: {output_path}")

print(f"\n{'=' * 70}")
print("FEATURE ENGINEERING COMPLETE")
print(f"{'=' * 70}")
