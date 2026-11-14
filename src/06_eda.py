"""
Step 5: Exploratory Data Analysis (EDA)

This script demonstrates how to:
- Visualize distributions of numeric features
- Analyze categorical variable frequencies
- Create correlation heatmaps
- Generate box plots for outlier analysis
- Explore relationships between features and the target
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for saving plots
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ─── Setup ───
output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs")
os.makedirs(output_dir, exist_ok=True)

data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "employee_attrition_cleaned.csv")
df = pd.read_csv(data_path)

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

print("=" * 70)
print("STEP 5: EXPLORATORY DATA ANALYSIS (EDA)")
print("=" * 70)

# ═══════════════════════════════════════════════════════════════════════
# 5.1 DISTRIBUTION OF NUMERIC FEATURES
# ═══════════════════════════════════════════════════════════════════════
print("\n--- 5.1 Distribution of Numeric Features ---")

numeric_cols = ["Age", "YearsAtCompany", "MonthlySalary", "SatisfactionScore", "DistanceFromHome"]

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
axes = axes.flatten()

for i, col in enumerate(numeric_cols):
    axes[i].hist(df[col].dropna(), bins=30, color="steelblue", edgecolor="black", alpha=0.7)
    axes[i].set_title(f"Distribution of {col}", fontsize=12)
    axes[i].set_xlabel(col)
    axes[i].set_ylabel("Frequency")
    axes[i].axvline(df[col].mean(), color="red", linestyle="--", label=f"Mean: {df[col].mean():.1f}")
    axes[i].axvline(df[col].median(), color="green", linestyle="-.", label=f"Median: {df[col].median():.1f}")
    axes[i].legend(fontsize=8)

axes[-1].set_visible(False)  # Hide extra subplot
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "01_numeric_distributions.png"), dpi=150)
plt.close()
print("   ✅ Saved: 01_numeric_distributions.png")

# ═══════════════════════════════════════════════════════════════════════
# 5.2 CATEGORICAL VARIABLE FREQUENCIES
# ═══════════════════════════════════════════════════════════════════════
print("\n--- 5.2 Categorical Variable Frequencies ---")

cat_cols = ["Gender", "Department", "EducationLevel", "OverTime", "Attrition"]
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
axes = axes.flatten()

colors = ["#4C72B0", "#55A868", "#C44E52", "#8172B2", "#CCB974"]

for i, col in enumerate(cat_cols):
    counts = df[col].value_counts()
    axes[i].bar(counts.index, counts.values, color=colors, edgecolor="black")
    axes[i].set_title(f"{col} Distribution", fontsize=12)
    axes[i].set_xlabel(col)
    axes[i].set_ylabel("Count")
    axes[i].tick_params(axis="x", rotation=45)
    # Add value labels on bars
    for j, (val, count) in enumerate(zip(counts.index, counts.values)):
        axes[i].text(j, count + 2, str(count), ha="center", fontsize=9)

axes[-1].set_visible(False)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "02_categorical_distributions.png"), dpi=150)
plt.close()
print("   ✅ Saved: 02_categorical_distributions.png")

# ═══════════════════════════════════════════════════════════════════════
# 5.3 CORRELATION HEATMAP
# ═══════════════════════════════════════════════════════════════════════
print("\n--- 5.3 Correlation Heatmap ---")

# Encode for correlation
df_corr = df.copy()
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
for col in ["Gender", "OverTime", "Attrition"]:
    df_corr[col] = le.fit_transform(df_corr[col])
df_corr["EducationLevel"] = df_corr["EducationLevel"].map(
    {"High School": 0, "Bachelor": 1, "Master": 2, "PhD": 3}
)
df_corr.drop(columns=["EmployeeID", "Department"], inplace=True, errors="ignore")

fig, ax = plt.subplots(figsize=(12, 9))
corr_matrix = df_corr.corr()
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt=".2f", cmap="RdBu_r",
            center=0, linewidths=0.5, ax=ax, vmin=-1, vmax=1)
ax.set_title("Feature Correlation Heatmap", fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "03_correlation_heatmap.png"), dpi=150)
plt.close()
print("   ✅ Saved: 03_correlation_heatmap.png")

# ═══════════════════════════════════════════════════════════════════════
# 5.4 BOX PLOTS (Outlier Analysis)
# ═══════════════════════════════════════════════════════════════════════
print("\n--- 5.4 Box Plots ---")

fig, axes = plt.subplots(1, 5, figsize=(18, 5))
for i, col in enumerate(numeric_cols):
    sns.boxplot(y=df[col], ax=axes[i], color="lightblue")
    axes[i].set_title(f"{col}", fontsize=11)

plt.suptitle("Box Plots of Numeric Features (Post-Cleaning)", fontsize=14, y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "04_box_plots.png"), dpi=150, bbox_inches="tight")
plt.close()
print("   ✅ Saved: 04_box_plots.png")

# ═══════════════════════════════════════════════════════════════════════
# 5.5 ATTRITION ANALYSIS
# ═══════════════════════════════════════════════════════════════════════
print("\n--- 5.5 Attrition Analysis ---")

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Attrition by Department
pd.crosstab(df["Department"], df["Attrition"]).plot(kind="bar", ax=axes[0], color=["#55A868", "#C44E52"])
axes[0].set_title("Attrition by Department")
axes[0].set_ylabel("Count")
axes[0].tick_params(axis="x", rotation=45)

# Attrition by OverTime
pd.crosstab(df["OverTime"], df["Attrition"]).plot(kind="bar", ax=axes[1], color=["#55A868", "#C44E52"])
axes[1].set_title("Attrition by OverTime")
axes[1].set_ylabel("Count")

# Salary distribution by Attrition
for label, color in zip(["No", "Yes"], ["#55A868", "#C44E52"]):
    subset = df[df["Attrition"] == label]["MonthlySalary"]
    axes[2].hist(subset, bins=25, alpha=0.6, label=f"Attrition={label}", color=color, edgecolor="black")
axes[2].set_title("Salary Distribution by Attrition")
axes[2].set_xlabel("Monthly Salary")
axes[2].legend()

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "05_attrition_analysis.png"), dpi=150)
plt.close()
print("   ✅ Saved: 05_attrition_analysis.png")

# ═══════════════════════════════════════════════════════════════════════
# 5.6 PAIRPLOT (Key Features)
# ═══════════════════════════════════════════════════════════════════════
print("\n--- 5.6 Pair Plot ---")
pair_cols = ["Age", "MonthlySalary", "SatisfactionScore", "YearsAtCompany", "Attrition"]
g = sns.pairplot(df[pair_cols], hue="Attrition", palette={"Yes": "#C44E52", "No": "#55A868"},
                 diag_kind="hist", plot_kws={"alpha": 0.5, "s": 20})
g.figure.suptitle("Pair Plot of Key Features", y=1.02)
plt.savefig(os.path.join(output_dir, "06_pair_plot.png"), dpi=120, bbox_inches="tight")
plt.close()
print("   ✅ Saved: 06_pair_plot.png")

# ─── Summary Statistics ───
print(f"\n{'=' * 70}")
print("EDA COMPLETE — Key Insights:")
print(f"   • Dataset has {len(df)} records after cleaning")
print(f"   • Attrition rate: {(df['Attrition'] == 'Yes').mean() * 100:.1f}%")
print(f"   • Average salary: ${df['MonthlySalary'].mean():,.0f}")
print(f"   • Average satisfaction: {df['SatisfactionScore'].mean():.2f}/5")
print(f"   • All plots saved to: {output_dir}")
print(f"{'=' * 70}")
