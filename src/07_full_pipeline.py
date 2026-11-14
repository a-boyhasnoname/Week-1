"""
Step 6: Complete End-to-End Preprocessing Pipeline

This script combines all preprocessing steps into a single reusable pipeline:
1. Data Loading
2. Data Cleaning (duplicates, standardization, missing values, outliers)
3. Feature Engineering (encoding)
4. Normalization
5. Final dataset ready for Machine Learning

This demonstrates how a real-world preprocessing workflow operates.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import os
import warnings
warnings.filterwarnings("ignore")

# ─── Configuration ───
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "employee_attrition.csv")
FINAL_OUTPUT_PATH = os.path.join(BASE_DIR, "data", "employee_attrition_final.csv")


def load_data(filepath):
    """Load the raw CSV dataset."""
    print("📥 Loading dataset...")
    df = pd.read_csv(filepath)
    print(f"   Shape: {df.shape}")
    print(f"   Missing values: {df.isnull().sum().sum()}")
    print(f"   Duplicates: {df.duplicated().sum()}")
    return df


def remove_duplicates(df):
    """Remove duplicate rows."""
    before = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    removed = before - len(df)
    print(f"🗑️  Removed {removed} duplicate rows → {len(df)} rows remaining")
    return df


def standardize_categories(df):
    """Standardize inconsistent categorical values."""
    print("🔤 Standardizing categorical values...")

    # Gender
    df["Gender"] = df["Gender"].replace({"male": "Male", "female": "Female", "M": "Male", "F": "Female"})

    # Department
    df["Department"] = df["Department"].str.strip().str.title()

    # OverTime
    df["OverTime"] = df["OverTime"].replace({"yes": "Yes", "no": "No", "YES": "Yes", "NO": "No"})

    print("   ✅ Done")
    return df


def handle_missing_values(df):
    """Impute missing values: median for numeric, mode for categorical."""
    print("🩹 Handling missing values...")

    numeric_cols = ["Age", "YearsAtCompany", "MonthlySalary", "SatisfactionScore", "DistanceFromHome"]
    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            median_val = df[col].median()
            df[col].fillna(median_val, inplace=True)
            print(f"   {col}: filled with median = {median_val:.2f}")

    categorical_cols = ["Department", "EducationLevel"]
    for col in categorical_cols:
        if df[col].isnull().sum() > 0:
            mode_val = df[col].mode()[0]
            df[col].fillna(mode_val, inplace=True)
            print(f"   {col}: filled with mode = '{mode_val}'")

    print(f"   ✅ Remaining missing: {df.isnull().sum().sum()}")
    return df


def handle_outliers(df):
    """Cap outliers using the IQR method (Winsorization)."""
    print("📊 Handling outliers (IQR method)...")

    cols = ["MonthlySalary", "Age", "YearsAtCompany", "DistanceFromHome"]
    for col in cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        outliers = ((df[col] < lower) | (df[col] > upper)).sum()
        if outliers > 0:
            df[col] = df[col].clip(lower=lower, upper=upper)
            print(f"   {col}: capped {outliers} outliers to [{lower:.1f}, {upper:.1f}]")

    print("   ✅ Done")
    return df


def encode_features(df):
    """Encode categorical variables."""
    print("🏷️  Encoding features...")

    # Label encode ordinal & binary variables
    df["EducationLevel_Encoded"] = df["EducationLevel"].map(
        {"High School": 0, "Bachelor": 1, "Master": 2, "PhD": 3}
    )

    le = LabelEncoder()
    df["Attrition_Encoded"] = le.fit_transform(df["Attrition"])
    df["OverTime_Encoded"] = le.fit_transform(df["OverTime"])
    df["Gender_Encoded"] = le.fit_transform(df["Gender"])

    # One-hot encode Department
    df = pd.get_dummies(df, columns=["Department"], prefix="Dept", dtype=int)

    # Drop original categorical columns
    df.drop(columns=["Gender", "EducationLevel", "OverTime", "Attrition", "EmployeeID"],
            inplace=True, errors="ignore")

    print(f"   ✅ Final columns: {list(df.columns)}")
    return df


def normalize_features(df):
    """Apply Min-Max normalization to continuous features."""
    print("📐 Normalizing features...")

    cols_to_scale = ["Age", "YearsAtCompany", "MonthlySalary", "SatisfactionScore", "DistanceFromHome"]
    scaler = MinMaxScaler()
    df[cols_to_scale] = scaler.fit_transform(df[cols_to_scale])

    print(f"   ✅ Scaled columns: {cols_to_scale}")
    return df


# ═══════════════════════════════════════════════════════════════════════
# MAIN PIPELINE
# ═══════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 70)
    print("COMPLETE DATA PREPROCESSING PIPELINE")
    print("=" * 70)

    # Step 1: Load
    df = load_data(RAW_DATA_PATH)

    # Step 2: Clean
    print(f"\n{'─' * 50}")
    df = remove_duplicates(df)
    df = standardize_categories(df)
    df = handle_missing_values(df)
    df = handle_outliers(df)

    # Step 3: Encode
    print(f"\n{'─' * 50}")
    df = encode_features(df)

    # Step 4: Normalize
    print(f"\n{'─' * 50}")
    df = normalize_features(df)

    # Step 5: Save
    print(f"\n{'─' * 50}")
    df.to_csv(FINAL_OUTPUT_PATH, index=False)
    print(f"💾 Final preprocessed dataset saved: {FINAL_OUTPUT_PATH}")
    print(f"   Shape: {df.shape}")

    print(f"\n{'=' * 70}")
    print("✅ PIPELINE COMPLETE — Dataset is ready for Machine Learning!")
    print(f"{'=' * 70}")

    # Show final sample
    print("\n📋 Sample of final dataset:")
    print(df.head().to_string())
