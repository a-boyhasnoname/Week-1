"""
Generate the Week 1 Report as a .docx file
"""

from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
REPORT_PATH = os.path.join(BASE_DIR, "report", "Week1_Report.docx")

doc = Document()

# ─── Styles ───
style = doc.styles["Normal"]
font = style.font
font.name = "Calibri"
font.size = Pt(11)

# ═══════════════════════════════════════════════════════════════════════
# TITLE PAGE
# ═══════════════════════════════════════════════════════════════════════
for _ in range(6):
    doc.add_paragraph()

title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title.add_run("Week 1 Report")
run.bold = True
run.font.size = Pt(28)
run.font.color.rgb = RGBColor(0x2C, 0x3E, 0x50)

subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = subtitle.add_run("Python for Machine Learning & Data Preprocessing")
run.font.size = Pt(16)
run.font.color.rgb = RGBColor(0x7F, 0x8C, 0x8D)

doc.add_paragraph()

info = doc.add_paragraph()
info.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = info.add_run("Internship Task Submission\nNovember 2026")
run.font.size = Pt(12)

doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════
# TABLE OF CONTENTS
# ═══════════════════════════════════════════════════════════════════════
doc.add_heading("Table of Contents", level=1)
toc_items = [
    "1. Introduction",
    "2. Objective",
    "3. Dataset Description",
    "4. Methodology",
    "   4.1 Data Loading & Inspection",
    "   4.2 Data Cleaning",
    "   4.3 Feature Engineering",
    "   4.4 Normalization & Scaling",
    "   4.5 Exploratory Data Analysis",
    "5. Complete Preprocessing Pipeline",
    "6. Results & Key Findings",
    "7. Tools & Technologies Used",
    "8. Conclusion",
]
for item in toc_items:
    doc.add_paragraph(item, style="List Bullet")
doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════
# 1. INTRODUCTION
# ═══════════════════════════════════════════════════════════════════════
doc.add_heading("1. Introduction", level=1)
doc.add_paragraph(
    "This report documents the work completed during Week 1 of the internship program, "
    "focusing on Python fundamentals for Machine Learning and Data Preprocessing. "
    "The primary goal was to build a solid foundation in data manipulation, cleaning, "
    "and preparation techniques that are essential prerequisites for any machine learning project. "
    "Data preprocessing is arguably the most critical step in the ML pipeline, as the quality "
    "of input data directly impacts model performance. Real-world datasets are inherently messy — "
    "they contain missing values, duplicate records, inconsistent formatting, outliers, and "
    "features at different scales. This report walks through a systematic approach to handling "
    "each of these challenges using Python's powerful data science ecosystem."
)

# ═══════════════════════════════════════════════════════════════════════
# 2. OBJECTIVE
# ═══════════════════════════════════════════════════════════════════════
doc.add_heading("2. Objective", level=1)
doc.add_paragraph(
    "The objectives for this week were threefold:"
)
objectives = [
    "Understand the fundamentals of Machine Learning using Python, including the typical ML workflow and the role of data preprocessing within it.",
    "Learn data loading, cleaning, handling missing values, feature selection, encoding categorical variables, normalization, and exploratory data analysis using Pandas and NumPy.",
    "Clean and preprocess a sample dataset and document each preprocessing step thoroughly.",
]
for obj in objectives:
    doc.add_paragraph(obj, style="List Number")

# ═══════════════════════════════════════════════════════════════════════
# 3. DATASET DESCRIPTION
# ═══════════════════════════════════════════════════════════════════════
doc.add_heading("3. Dataset Description", level=1)
doc.add_paragraph(
    "For this project, a synthetic Employee Attrition dataset was created to simulate "
    "real-world data quality issues. The dataset contains 515 records (including 15 intentional "
    "duplicates) with 12 columns representing various employee attributes. The dataset was "
    "designed with the following intentional data quality issues:"
)

issues = [
    "Missing values (~5%) in numeric columns (Age, YearsAtCompany, MonthlySalary, SatisfactionScore, DistanceFromHome)",
    "Missing values (~11%) in categorical columns (Department, EducationLevel)",
    "Duplicate rows (15 records)",
    "Inconsistent categorical values (e.g., 'Male', 'male', 'M' all representing the same category)",
    "Outliers in MonthlySalary (values like $150, $200, $25,000, $50,000)",
]
for issue in issues:
    doc.add_paragraph(issue, style="List Bullet")

doc.add_paragraph()
doc.add_paragraph("Dataset Columns:", style="Intense Quote")

# Column description table
table = doc.add_table(rows=13, cols=3)
table.style = "Medium Shading 1 Accent 1"
headers = ["Column Name", "Data Type", "Description"]
for i, h in enumerate(headers):
    table.rows[0].cells[i].text = h

columns_info = [
    ("EmployeeID", "Integer", "Unique employee identifier"),
    ("Age", "Float", "Employee age (22-61)"),
    ("Gender", "String", "Male/Female (with inconsistent variations)"),
    ("Department", "String", "Work department (Sales, Engineering, HR, etc.)"),
    ("EducationLevel", "String", "Highest education (High School to PhD)"),
    ("YearsAtCompany", "Float", "Tenure in years"),
    ("MonthlySalary", "Float", "Monthly salary with outliers"),
    ("SatisfactionScore", "Float", "Job satisfaction (1-5 scale)"),
    ("PerformanceRating", "Integer", "Performance rating (1-5)"),
    ("DistanceFromHome", "Float", "Distance from home in km"),
    ("OverTime", "String", "Whether employee works overtime"),
    ("Attrition", "String", "Whether employee left (Yes/No) — target variable"),
]
for i, (name, dtype, desc) in enumerate(columns_info):
    table.rows[i + 1].cells[0].text = name
    table.rows[i + 1].cells[1].text = dtype
    table.rows[i + 1].cells[2].text = desc

# ═══════════════════════════════════════════════════════════════════════
# 4. METHODOLOGY
# ═══════════════════════════════════════════════════════════════════════
doc.add_heading("4. Methodology", level=1)
doc.add_paragraph(
    "The preprocessing was carried out in a systematic, step-by-step manner. "
    "Each step is implemented as an independent Python script, and a final pipeline "
    "script combines all steps into a single reusable workflow."
)

# 4.1 Data Loading & Inspection
doc.add_heading("4.1 Data Loading & Inspection", level=2)
doc.add_paragraph(
    "The first step involved loading the CSV file using pandas.read_csv() and performing "
    "an initial inspection of the dataset. This included examining the shape (515 rows × 12 columns), "
    "data types, and generating statistical summaries using df.describe(). "
    "The inspection revealed 244 total missing values across 7 columns, 15 duplicate rows, "
    "6 different representations of gender, and extreme salary values ranging from $150 to $50,000. "
    "Key functions used: pd.read_csv(), df.info(), df.describe(), df.isnull().sum(), "
    "df.duplicated().sum(), df.nunique()."
)

# 4.2 Data Cleaning
doc.add_heading("4.2 Data Cleaning", level=2)
doc.add_paragraph(
    "Data cleaning was performed in four sub-steps:"
)

doc.add_heading("Removing Duplicates", level=3)
doc.add_paragraph(
    "Used df.drop_duplicates() to remove 15 duplicate rows, reducing the dataset from "
    "515 to 500 records."
)

doc.add_heading("Standardizing Categorical Values", level=3)
doc.add_paragraph(
    "Inconsistent categorical values were standardized using the .replace() method and "
    "string operations. For example, Gender values ('Male', 'male', 'M', 'Female', 'female', 'F') "
    "were mapped to just 'Male' and 'Female'. Similar standardization was applied to Department "
    "and OverTime columns using .str.title() and explicit mappings."
)

doc.add_heading("Handling Missing Values", level=3)
doc.add_paragraph(
    "Two imputation strategies were employed based on column type:\n"
    "• Numeric columns (Age, YearsAtCompany, MonthlySalary, SatisfactionScore, DistanceFromHome): "
    "Imputed using the median, which is robust to outliers. For example, Age nulls were filled "
    "with median value 44.0, and MonthlySalary nulls with 5515.03.\n"
    "• Categorical columns (Department, EducationLevel): Imputed using the mode (most frequent value). "
    "Department nulls were filled with 'Engineering' and EducationLevel with 'Bachelor'."
)

doc.add_heading("Outlier Detection & Treatment", level=3)
doc.add_paragraph(
    "Outliers were detected using the Interquartile Range (IQR) method. For each numeric column, "
    "the IQR was calculated as Q3 - Q1, and values outside [Q1 - 1.5×IQR, Q3 + 1.5×IQR] were "
    "identified as outliers. Rather than removing outliers (which would lose data), Winsorization "
    "was applied — capping extreme values at the computed boundaries. For MonthlySalary, 13 outliers "
    "were capped to the range [$1,492.70, $9,761.20]."
)

# 4.3 Feature Engineering
doc.add_heading("4.3 Feature Engineering", level=2)

doc.add_heading("Label Encoding", level=3)
doc.add_paragraph(
    "Label encoding was applied to ordinal and binary categorical variables:\n"
    "• EducationLevel: Mapped to ordinal integers (High School=0, Bachelor=1, Master=2, PhD=3) "
    "to preserve the natural ordering.\n"
    "• Attrition, OverTime, Gender: Encoded as binary 0/1 using sklearn's LabelEncoder."
)

doc.add_heading("One-Hot Encoding", level=3)
doc.add_paragraph(
    "One-hot encoding (pd.get_dummies()) was applied to the Department column since it is a "
    "nominal variable with no inherent order. This created 5 binary columns (Dept_Engineering, "
    "Dept_Finance, Dept_Hr, Dept_Marketing, Dept_Sales), each indicating membership in that department."
)

doc.add_heading("Feature Selection via Correlation Analysis", level=3)
doc.add_paragraph(
    "A correlation analysis was performed to identify features most strongly associated with "
    "the target variable (Attrition). The analysis also checked for multicollinearity — highly "
    "correlated feature pairs (|r| > 0.7) — which could cause issues in certain ML algorithms. "
    "No highly correlated pairs were found, indicating that the feature set is well-suited for modeling."
)

# 4.4 Normalization
doc.add_heading("4.4 Normalization & Scaling", level=2)
doc.add_paragraph(
    "Two normalization techniques were implemented and compared:\n\n"
    "Min-Max Normalization: Scales features to the [0, 1] range using the formula "
    "X_scaled = (X - X_min) / (X_max - X_min). This is useful when bounded values are needed.\n\n"
    "Standard Scaling (Z-score): Centers features to mean=0 and std=1 using the formula "
    "X_scaled = (X - μ) / σ. This is useful when algorithms assume normally distributed features.\n\n"
    "The Min-Max normalized version was chosen for the final pipeline as it provides intuitive "
    "bounded values suitable for most ML algorithms."
)

# 4.5 EDA
doc.add_heading("4.5 Exploratory Data Analysis (EDA)", level=2)
doc.add_paragraph(
    "Comprehensive EDA was performed to understand data distributions and relationships. "
    "Six types of visualizations were generated:"
)

eda_items = [
    "Histograms of numeric feature distributions with mean/median markers",
    "Bar charts of categorical variable frequencies",
    "Correlation heatmap showing inter-feature relationships",
    "Box plots for outlier visualization (post-cleaning)",
    "Attrition analysis — breakdown by department, overtime status, and salary",
    "Pair plots showing pairwise relationships colored by attrition status",
]
for item in eda_items:
    doc.add_paragraph(item, style="List Number")

# Add EDA images
eda_images = [
    ("01_numeric_distributions.png", "Distribution of Numeric Features"),
    ("02_categorical_distributions.png", "Categorical Variable Frequencies"),
    ("03_correlation_heatmap.png", "Feature Correlation Heatmap"),
    ("04_box_plots.png", "Box Plots of Numeric Features"),
    ("05_attrition_analysis.png", "Attrition Analysis"),
    ("06_pair_plot.png", "Pair Plot of Key Features"),
]
for filename, caption in eda_images:
    img_path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(img_path):
        doc.add_paragraph()
        doc.add_picture(img_path, width=Inches(5.5))
        last_paragraph = doc.paragraphs[-1]
        last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap = doc.add_paragraph(f"Figure: {caption}")
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap.runs[0].italic = True
        cap.runs[0].font.size = Pt(9)

# ═══════════════════════════════════════════════════════════════════════
# 5. COMPLETE PIPELINE
# ═══════════════════════════════════════════════════════════════════════
doc.add_heading("5. Complete Preprocessing Pipeline", level=1)
doc.add_paragraph(
    "All preprocessing steps were combined into a single reusable pipeline (07_full_pipeline.py) "
    "that takes the raw dataset and produces an ML-ready output in one execution. The pipeline "
    "consists of modular functions — load_data(), remove_duplicates(), standardize_categories(), "
    "handle_missing_values(), handle_outliers(), encode_features(), and normalize_features() — "
    "that can be individually modified or extended. The final output is a clean, fully numeric "
    "dataset with 500 rows and 15 features, ready to be fed into any machine learning algorithm."
)

# ═══════════════════════════════════════════════════════════════════════
# 6. RESULTS
# ═══════════════════════════════════════════════════════════════════════
doc.add_heading("6. Results & Key Findings", level=1)

results_table = doc.add_table(rows=7, cols=3)
results_table.style = "Medium Shading 1 Accent 1"
results_headers = ["Metric", "Before Preprocessing", "After Preprocessing"]
for i, h in enumerate(results_headers):
    results_table.rows[0].cells[i].text = h

results_data = [
    ("Total Rows", "515", "500"),
    ("Total Columns", "12", "15 (all numeric)"),
    ("Missing Values", "244", "0"),
    ("Duplicate Rows", "15", "0"),
    ("Categorical Inconsistencies", "Multiple", "None"),
    ("Outliers (MonthlySalary)", "13 extreme values", "Capped via IQR"),
]
for i, (metric, before, after) in enumerate(results_data):
    results_table.rows[i + 1].cells[0].text = metric
    results_table.rows[i + 1].cells[1].text = before
    results_table.rows[i + 1].cells[2].text = after

doc.add_paragraph()
doc.add_paragraph("Key Insights from EDA:", style="Intense Quote")
insights = [
    "The overall attrition rate is 27.0%, which is a significant proportion of the workforce.",
    "The average monthly salary is approximately $5,578, with values now bounded between $1,493 and $9,761 after outlier treatment.",
    "Average job satisfaction is 3.04 out of 5, indicating moderate satisfaction levels.",
    "No strong multicollinearity was detected between features, making the dataset suitable for a wide range of ML algorithms.",
    "The dataset has a reasonable balance across departments and demographic features after cleaning.",
]
for insight in insights:
    doc.add_paragraph(insight, style="List Bullet")

# ═══════════════════════════════════════════════════════════════════════
# 7. TOOLS & TECHNOLOGIES
# ═══════════════════════════════════════════════════════════════════════
doc.add_heading("7. Tools & Technologies Used", level=1)

tools_table = doc.add_table(rows=6, cols=2)
tools_table.style = "Medium Shading 1 Accent 1"
tools_table.rows[0].cells[0].text = "Tool / Library"
tools_table.rows[0].cells[1].text = "Purpose"

tools_data = [
    ("Python 3.13", "Primary programming language"),
    ("NumPy", "Numerical computing, array operations, random data generation"),
    ("Pandas", "Data loading, manipulation, cleaning, and analysis"),
    ("Matplotlib & Seaborn", "Data visualization (histograms, heatmaps, box plots, pair plots)"),
    ("Scikit-learn", "Preprocessing utilities (LabelEncoder, MinMaxScaler, StandardScaler)"),
]
for i, (tool, purpose) in enumerate(tools_data):
    tools_table.rows[i + 1].cells[0].text = tool
    tools_table.rows[i + 1].cells[1].text = purpose

# ═══════════════════════════════════════════════════════════════════════
# 8. CONCLUSION
# ═══════════════════════════════════════════════════════════════════════
doc.add_heading("8. Conclusion", level=1)
doc.add_paragraph(
    "This week's task provided hands-on experience with the critical first stage of any "
    "machine learning project: data preprocessing. Through working with a realistically messy "
    "dataset, the following key skills were developed:\n\n"
    "• Data inspection and profiling to identify quality issues before any processing begins.\n"
    "• Multiple strategies for handling missing data (median imputation for numeric, mode for categorical).\n"
    "• Techniques for standardizing inconsistent categorical values.\n"
    "• Outlier detection using the IQR method and treatment via Winsorization.\n"
    "• Feature encoding — both label encoding for ordinal data and one-hot encoding for nominal data.\n"
    "• Normalization techniques (Min-Max and Z-score) and when to apply each.\n"
    "• Comprehensive exploratory data analysis with multiple visualization types.\n"
    "• Building a modular, reusable preprocessing pipeline.\n\n"
    "The final preprocessed dataset is clean, fully numeric, normalized, and ready to be used "
    "as input for machine learning models in subsequent weeks. The modular pipeline architecture "
    "ensures that individual steps can be easily modified or extended as requirements evolve."
)

# ─── Save ───
os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
doc.save(REPORT_PATH)
print(f"✅ Report saved to: {REPORT_PATH}")
