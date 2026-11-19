# Step 5 - Exploratory Data Analysis (EDA) with visualizations

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
import os

# setup
output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs")
os.makedirs(output_dir, exist_ok=True)

data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "employee_attrition_cleaned.csv")
df = pd.read_csv(data_path)

sns.set_style("whitegrid")

print("--- Exploratory Data Analysis ---\n")

# 1. Histograms for numeric columns
numeric_cols = ["Age", "YearsAtCompany", "MonthlySalary", "SatisfactionScore", "DistanceFromHome"]

fig, axes = plt.subplots(2, 3, figsize=(15, 9))
axes = axes.flatten()

for i, col in enumerate(numeric_cols):
    axes[i].hist(df[col].dropna(), bins=30, color="steelblue", edgecolor="black", alpha=0.7)
    axes[i].set_title(col)
    axes[i].set_xlabel(col)
    axes[i].set_ylabel("Count")
    # adding mean and median lines
    axes[i].axvline(df[col].mean(), color="red", linestyle="--", label=f"Mean: {df[col].mean():.1f}")
    axes[i].axvline(df[col].median(), color="green", linestyle="-.", label=f"Median: {df[col].median():.1f}")
    axes[i].legend(fontsize=8)

axes[-1].set_visible(False)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "01_numeric_distributions.png"), dpi=150)
plt.close()
print("Saved: 01_numeric_distributions.png")

# 2. Bar charts for categorical columns
cat_cols = ["Gender", "Department", "EducationLevel", "OverTime", "Attrition"]
fig, axes = plt.subplots(2, 3, figsize=(15, 9))
axes = axes.flatten()

for i, col in enumerate(cat_cols):
    counts = df[col].value_counts()
    axes[i].bar(counts.index, counts.values, color=sns.color_palette("muted"), edgecolor="black")
    axes[i].set_title(col)
    axes[i].set_ylabel("Count")
    axes[i].tick_params(axis="x", rotation=45)

axes[-1].set_visible(False)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "02_categorical_distributions.png"), dpi=150)
plt.close()
print("Saved: 02_categorical_distributions.png")

# 3. Correlation heatmap
# need to encode categorical columns first for correlation
df_corr = df.copy()
le = LabelEncoder()
for col in ["Gender", "OverTime", "Attrition"]:
    df_corr[col] = le.fit_transform(df_corr[col])
df_corr["EducationLevel"] = df_corr["EducationLevel"].map(
    {"High School": 0, "Bachelor": 1, "Master": 2, "PhD": 3}
)
df_corr = df_corr.drop(columns=["EmployeeID", "Department"], errors="ignore")

fig, ax = plt.subplots(figsize=(10, 8))
mask = np.triu(np.ones_like(df_corr.corr(), dtype=bool))
sns.heatmap(df_corr.corr(), mask=mask, annot=True, fmt=".2f", cmap="RdBu_r",
            center=0, linewidths=0.5, ax=ax)
ax.set_title("Correlation Heatmap")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "03_correlation_heatmap.png"), dpi=150)
plt.close()
print("Saved: 03_correlation_heatmap.png")

# 4. Box plots
fig, axes = plt.subplots(1, 5, figsize=(16, 4))
for i, col in enumerate(numeric_cols):
    sns.boxplot(y=df[col], ax=axes[i], color="lightblue")
    axes[i].set_title(col)
plt.suptitle("Box Plots (after cleaning)", fontsize=13)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "04_box_plots.png"), dpi=150, bbox_inches="tight")
plt.close()
print("Saved: 04_box_plots.png")

# 5. Attrition breakdown
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# by department
pd.crosstab(df["Department"], df["Attrition"]).plot(kind="bar", ax=axes[0])
axes[0].set_title("Attrition by Department")
axes[0].tick_params(axis="x", rotation=45)

# by overtime
pd.crosstab(df["OverTime"], df["Attrition"]).plot(kind="bar", ax=axes[1])
axes[1].set_title("Attrition by OverTime")

# salary by attrition
for label in ["No", "Yes"]:
    subset = df[df["Attrition"] == label]["MonthlySalary"]
    axes[2].hist(subset, bins=25, alpha=0.6, label=f"Attrition={label}", edgecolor="black")
axes[2].set_title("Salary by Attrition")
axes[2].legend()

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "05_attrition_analysis.png"), dpi=150)
plt.close()
print("Saved: 05_attrition_analysis.png")

# 6. Pair plot
pair_cols = ["Age", "MonthlySalary", "SatisfactionScore", "YearsAtCompany", "Attrition"]
g = sns.pairplot(df[pair_cols], hue="Attrition", diag_kind="hist", plot_kws={"alpha": 0.5, "s": 20})
plt.savefig(os.path.join(output_dir, "06_pair_plot.png"), dpi=120, bbox_inches="tight")
plt.close()
print("Saved: 06_pair_plot.png")

# some quick stats
print(f"\nKey findings:")
print(f"  Total records: {len(df)}")
print(f"  Attrition rate: {(df['Attrition'] == 'Yes').mean() * 100:.1f}%")
print(f"  Average salary: ${df['MonthlySalary'].mean():,.0f}")
print(f"  Average satisfaction: {df['SatisfactionScore'].mean():.2f}/5")
