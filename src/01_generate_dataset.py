"""
Step 0: Generate a synthetic Employee Attrition dataset with realistic data quality issues.

This script creates a CSV file that mimics real-world messy data:
- Missing values in multiple columns
- Duplicate rows
- Outliers in salary and satisfaction scores
- Inconsistent categorical values
"""

import numpy as np
import pandas as pd
import os

np.random.seed(42)

N = 500  # Number of employee records

# ─── Generate base features ───
employee_ids = np.arange(1001, 1001 + N)

ages = np.random.randint(22, 62, size=N).astype(float)

genders = np.random.choice(["Male", "Female", "male", "female", "M", "F"], size=N)

departments = np.random.choice(
    ["Sales", "Engineering", "HR", "Marketing", "Finance", "sales", "engineering", np.nan],
    size=N,
)

education_levels = np.random.choice(
    ["High School", "Bachelor", "Master", "PhD", None], size=N, p=[0.2, 0.35, 0.25, 0.1, 0.1]
)

years_at_company = np.random.randint(0, 30, size=N).astype(float)

monthly_salary = np.random.normal(5500, 1500, size=N).round(2)
# Inject outliers
outlier_indices = np.random.choice(N, size=10, replace=False)
monthly_salary[outlier_indices] = np.random.choice([150, 200, 25000, 30000, 50000], size=10)

satisfaction_score = np.random.uniform(1, 5, size=N).round(2)

performance_rating = np.random.choice([1, 2, 3, 4, 5], size=N, p=[0.05, 0.15, 0.40, 0.30, 0.10])

distance_from_home = np.random.randint(1, 60, size=N).astype(float)

overtime = np.random.choice(["Yes", "No", "yes", "no", "YES", "NO"], size=N)

attrition = np.random.choice(["Yes", "No"], size=N, p=[0.25, 0.75])

# ─── Build DataFrame ───
df = pd.DataFrame({
    "EmployeeID": employee_ids,
    "Age": ages,
    "Gender": genders,
    "Department": departments,
    "EducationLevel": education_levels,
    "YearsAtCompany": years_at_company,
    "MonthlySalary": monthly_salary,
    "SatisfactionScore": satisfaction_score,
    "PerformanceRating": performance_rating,
    "DistanceFromHome": distance_from_home,
    "OverTime": overtime,
    "Attrition": attrition,
})

# ─── Inject missing values randomly ───
for col in ["Age", "YearsAtCompany", "MonthlySalary", "SatisfactionScore", "DistanceFromHome"]:
    missing_idx = np.random.choice(N, size=int(N * 0.05), replace=False)
    df.loc[missing_idx, col] = np.nan

# ─── Add duplicate rows ───
duplicate_rows = df.sample(n=15, random_state=42)
df = pd.concat([df, duplicate_rows], ignore_index=True)

# ─── Shuffle the dataset ───
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# ─── Save to CSV ───
output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "employee_attrition.csv")
df.to_csv(output_path, index=False)

print(f"✅ Dataset generated successfully!")
print(f"   Path: {output_path}")
print(f"   Shape: {df.shape}")
print(f"   Columns: {list(df.columns)}")
print(f"\nData quality issues injected:")
print(f"   - ~5% missing values in numeric columns")
print(f"   - Inconsistent categorical values (mixed case)")
print(f"   - {len(duplicate_rows)} duplicate rows")
print(f"   - Outliers in MonthlySalary")
print(f"   - None/NaN in EducationLevel and Department")
