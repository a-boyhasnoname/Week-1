"""
Step 4: Normalization & Scaling

This script demonstrates how to:
- Apply Min-Max Normalization (scales to [0, 1])
- Apply Standard Scaling / Z-score Normalization (mean=0, std=1)
- Compare distributions before and after scaling
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import os

# ─── Load encoded dataset ───
data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "employee_attrition_encoded.csv")
df = pd.read_csv(data_path)

print("=" * 70)
print("STEP 4: NORMALIZATION & SCALING")
print("=" * 70)

# Columns to normalize (continuous numeric features only)
cols_to_scale = ["Age", "YearsAtCompany", "MonthlySalary",
                 "SatisfactionScore", "DistanceFromHome"]

print(f"\n📋 Columns to normalize: {cols_to_scale}")
print(f"\n--- Before Scaling ---")
print(df[cols_to_scale].describe().round(3).to_string())

# ═══════════════════════════════════════════════════════════════════════
# 4.1 MIN-MAX NORMALIZATION (scales to [0, 1])
# ═══════════════════════════════════════════════════════════════════════
print("\n\n--- 4.1 Min-Max Normalization ---")
print("Formula: X_scaled = (X - X_min) / (X_max - X_min)")

scaler_minmax = MinMaxScaler()
df_minmax = df.copy()
df_minmax[cols_to_scale] = scaler_minmax.fit_transform(df[cols_to_scale])

print("\nAfter Min-Max Scaling:")
print(df_minmax[cols_to_scale].describe().round(3).to_string())

# Show the min-max parameters
print("\nMin-Max Parameters:")
for i, col in enumerate(cols_to_scale):
    print(f"   {col}: min={scaler_minmax.data_min_[i]:.2f}, max={scaler_minmax.data_max_[i]:.2f}")

# ═══════════════════════════════════════════════════════════════════════
# 4.2 STANDARD SCALING (Z-score Normalization)
# ═══════════════════════════════════════════════════════════════════════
print("\n\n--- 4.2 Standard Scaling (Z-score) ---")
print("Formula: X_scaled = (X - mean) / std")

scaler_standard = StandardScaler()
df_standard = df.copy()
df_standard[cols_to_scale] = scaler_standard.fit_transform(df[cols_to_scale])

print("\nAfter Standard Scaling:")
print(df_standard[cols_to_scale].describe().round(3).to_string())

# Show the standard scaler parameters
print("\nStandard Scaler Parameters:")
for i, col in enumerate(cols_to_scale):
    print(f"   {col}: mean={scaler_standard.mean_[i]:.2f}, std={scaler_standard.scale_[i]:.2f}")

# ═══════════════════════════════════════════════════════════════════════
# 4.3 COMPARISON
# ═══════════════════════════════════════════════════════════════════════
print("\n\n--- 4.3 Comparison: Original vs Min-Max vs Standard ---")
print(f"\n{'Column':<22} {'Original Range':>18} {'Min-Max Range':>18} {'Standard Range':>18}")
print("-" * 78)
for col in cols_to_scale:
    orig_range = f"[{df[col].min():.1f}, {df[col].max():.1f}]"
    mm_range = f"[{df_minmax[col].min():.3f}, {df_minmax[col].max():.3f}]"
    std_range = f"[{df_standard[col].min():.3f}, {df_standard[col].max():.3f}]"
    print(f"{col:<22} {orig_range:>18} {mm_range:>18} {std_range:>18}")

# ─── Save the Min-Max scaled version (commonly used for ML) ───
output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "employee_attrition_normalized.csv")
df_minmax.to_csv(output_path, index=False)
print(f"\n✅ Min-Max normalized dataset saved: {output_path}")

print(f"\n{'=' * 70}")
print("NORMALIZATION COMPLETE")
print("Key takeaways:")
print("  • Min-Max: Good when you need bounded values [0,1]")
print("  • Standard: Good when the algorithm assumes normally distributed data")
print("  • Choose based on your ML algorithm requirements")
print(f"{'=' * 70}")
