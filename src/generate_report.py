# Script to generate the Week 1 report

from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
REPORT_PATH = os.path.join(BASE_DIR, "report", "Week1_Report.docx")

doc = Document()

style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(11)

# --- Title ---
doc.add_heading("Week 1 Report: Python for Machine Learning & Data Preprocessing", level=0)
doc.add_paragraph("Internship Weekly Task Submission")
doc.add_paragraph("")

# --- Introduction ---
doc.add_heading("1. Introduction", level=1)
doc.add_paragraph(
    "This report covers the work I did for Week 1 of my internship. The task was about "
    "learning Python basics for Machine Learning, specifically focusing on data preprocessing. "
    "Data preprocessing is really important because real-world data is always messy - it has "
    "missing values, duplicates, inconsistent formatting, etc. If we don't clean the data "
    "properly, any ML model we build on top of it won't perform well. So this week I focused "
    "on learning how to clean and prepare data using Python libraries like Pandas and NumPy."
)

# --- Objective ---
doc.add_heading("2. Objectives", level=1)
doc.add_paragraph("The main objectives for this week were:")
doc.add_paragraph("1. Understand the fundamentals of Machine Learning using Python", style="List Number")
doc.add_paragraph("2. Learn data loading, cleaning, handling missing values, feature selection, "
                   "encoding categorical variables, normalization, and EDA using Pandas and NumPy", style="List Number")
doc.add_paragraph("3. Clean and preprocess a sample dataset and document each step", style="List Number")

# --- Dataset ---
doc.add_heading("3. About the Dataset", level=1)
doc.add_paragraph(
    "I created a synthetic Employee Attrition dataset for this project. It has 515 records "
    "with 12 columns like Age, Gender, Department, Salary, etc. I intentionally added some "
    "data quality issues to make it realistic - things like missing values in several columns, "
    "15 duplicate rows, inconsistent text values (like 'Male', 'male', and 'M' all meaning the "
    "same thing), and some extreme salary values as outliers."
)

doc.add_paragraph("The columns in the dataset are:")
columns_desc = [
    "EmployeeID - unique identifier for each employee",
    "Age - employee's age (22-61)",
    "Gender - Male or Female (had inconsistent variations)",
    "Department - which department they work in",
    "EducationLevel - highest education from High School to PhD",
    "YearsAtCompany - how long they've been working there",
    "MonthlySalary - their monthly pay (had some outliers)",
    "SatisfactionScore - job satisfaction from 1 to 5",
    "PerformanceRating - performance score 1-5",
    "DistanceFromHome - distance from home in km",
    "OverTime - whether they work overtime",
    "Attrition - whether they left the company (target variable)",
]
for c in columns_desc:
    doc.add_paragraph(c, style="List Bullet")

# --- What I Did ---
doc.add_heading("4. Steps I Followed", level=1)

doc.add_heading("Step 1: Data Loading and Inspection", level=2)
doc.add_paragraph(
    "First I loaded the CSV file using pandas read_csv() and looked at the basic info. "
    "I checked the shape (515 rows, 12 columns), data types, and ran describe() to see "
    "statistics. I found 244 total missing values, 15 duplicate rows, and inconsistent "
    "categorical values. The salary column had some really extreme values (like $150 and $50,000) "
    "which were clearly outliers."
)

doc.add_heading("Step 2: Data Cleaning", level=2)
doc.add_paragraph(
    "This was the biggest step. I did four things here:"
)
doc.add_paragraph(
    "Removing duplicates: Used drop_duplicates() to remove 15 duplicate rows. "
    "This brought the dataset down from 515 to 500 rows."
)
doc.add_paragraph(
    "Fixing categorical values: Used replace() to standardize Gender (mapped 'male', 'M' etc "
    "to 'Male'/'Female'), used str.title() for Department, and fixed OverTime similarly."
)
doc.add_paragraph(
    "Handling missing values: For numeric columns I used the median to fill missing values "
    "because median is less affected by outliers than mean. For categorical columns I used "
    "the mode (most frequent value). For example, Age nulls were filled with 44 and "
    "Department nulls with 'Engineering'."
)
doc.add_paragraph(
    "Handling outliers: I used the IQR (Interquartile Range) method to find outliers. "
    "Instead of deleting them, I capped them at the boundaries (this is called Winsorization). "
    "For MonthlySalary, 13 outliers were capped to the range [$1,493 - $9,761]."
)

doc.add_heading("Step 3: Feature Engineering", level=2)
doc.add_paragraph(
    "I needed to convert text columns to numbers since ML algorithms need numeric input. "
    "I used two approaches:"
)
doc.add_paragraph(
    "Label Encoding - for columns with order or binary values. EducationLevel was mapped "
    "as High School=0, Bachelor=1, Master=2, PhD=3. Gender, OverTime, and Attrition were "
    "encoded as 0/1 using sklearn's LabelEncoder."
)
doc.add_paragraph(
    "One-Hot Encoding - for Department since it doesn't have any natural order. "
    "This created 5 new binary columns (Dept_Engineering, Dept_Finance, etc.)."
)
doc.add_paragraph(
    "I also did a correlation analysis to check which features are most related to "
    "Attrition and to check for multicollinearity. No highly correlated pairs were found."
)

doc.add_heading("Step 4: Normalization", level=2)
doc.add_paragraph(
    "Different features had very different ranges (Age: 22-61, Salary: 1493-9761). This can "
    "cause problems for some ML algorithms. I tried two scaling methods:"
)
doc.add_paragraph(
    "Min-Max Scaling: scales everything to [0, 1] range. Formula: (x - min) / (max - min)"
)
doc.add_paragraph(
    "Standard Scaling: makes mean = 0 and std = 1. Formula: (x - mean) / std"
)
doc.add_paragraph(
    "I went with Min-Max scaling for the final pipeline since it gives nice bounded values."
)

doc.add_heading("Step 5: Exploratory Data Analysis", level=2)
doc.add_paragraph(
    "I created several visualizations to better understand the data:"
)
viz_list = [
    "Histograms showing distribution of numeric features with mean/median lines",
    "Bar charts for categorical variable frequencies",
    "Correlation heatmap showing relationships between features",
    "Box plots to see the spread and any remaining outliers",
    "Attrition analysis - breakdown by department, overtime, and salary",
    "Pair plot showing relationships between key features colored by attrition",
]
for v in viz_list:
    doc.add_paragraph(v, style="List Bullet")

# add the charts
charts = [
    ("01_numeric_distributions.png", "Numeric Feature Distributions"),
    ("02_categorical_distributions.png", "Categorical Distributions"),
    ("03_correlation_heatmap.png", "Correlation Heatmap"),
    ("04_box_plots.png", "Box Plots"),
    ("05_attrition_analysis.png", "Attrition Analysis"),
    ("06_pair_plot.png", "Pair Plot"),
]
for filename, title in charts:
    img_path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(img_path):
        doc.add_paragraph("")
        doc.add_picture(img_path, width=Inches(5.0))
        p = doc.add_paragraph(title)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.runs[0].italic = True
        p.runs[0].font.size = Pt(9)

# --- Results ---
doc.add_heading("5. Results", level=1)
doc.add_paragraph(
    "After all the preprocessing, here's what changed:"
)
doc.add_paragraph("Rows went from 515 to 500 (removed duplicates)")
doc.add_paragraph("Columns went from 12 (mixed types) to 15 (all numeric)")
doc.add_paragraph("Missing values went from 244 to 0")
doc.add_paragraph("No more duplicate rows")
doc.add_paragraph("Outliers in salary were capped")
doc.add_paragraph("All features are now normalized to [0, 1] range")

doc.add_paragraph("")
doc.add_paragraph("Some interesting findings from the EDA:")
doc.add_paragraph("The attrition rate is about 27%", style="List Bullet")
doc.add_paragraph("Average monthly salary is around $5,578", style="List Bullet")
doc.add_paragraph("Average satisfaction score is 3.04 out of 5", style="List Bullet")
doc.add_paragraph("No strong correlation between any single feature and attrition", style="List Bullet")

# --- Tools ---
doc.add_heading("6. Tools and Libraries Used", level=1)
doc.add_paragraph("Python 3.13 - main programming language", style="List Bullet")
doc.add_paragraph("NumPy - for numerical operations and generating random data", style="List Bullet")
doc.add_paragraph("Pandas - for loading, manipulating, and cleaning the data", style="List Bullet")
doc.add_paragraph("Matplotlib and Seaborn - for creating charts and plots", style="List Bullet")
doc.add_paragraph("Scikit-learn - for LabelEncoder, MinMaxScaler, StandardScaler", style="List Bullet")

# --- Conclusion ---
doc.add_heading("7. Conclusion", level=1)
doc.add_paragraph(
    "This week I learned how important data preprocessing is before doing any machine learning. "
    "Real data is never clean and there are many steps involved in preparing it - from handling "
    "missing values and duplicates to encoding categories and normalizing features. I also learned "
    "that there are different strategies for each problem (like using median vs mean for imputation, "
    "or choosing between label encoding and one-hot encoding depending on the type of variable). "
    "The final dataset is now clean, fully numeric, and normalized, which means it's ready to be "
    "used as input for ML models in the upcoming weeks."
)

# save
os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
doc.save(REPORT_PATH)
print(f"Report saved to: {REPORT_PATH}")
