# Week 1: Python for Machine Learning & Data Preprocessing

## Objective
1. Understand the fundamentals of Machine Learning using Python
2. Learn data loading, cleaning, handling missing values, feature selection, encoding categorical variables, normalization, and exploratory data analysis using Pandas and NumPy
3. Clean and preprocess a sample dataset and document each preprocessing step

## Dataset
We use a synthetic **Employee Attrition Dataset** (`data/employee_attrition.csv`) that contains common real-world data quality issues:
- Missing values (numeric and categorical)
- Duplicate rows
- Outliers
- Mixed categorical encodings
- Un-normalized numeric features

## Project Structure
```
Week1-Python-ML-DataPreprocessing/
├── README.md
├── requirements.txt
├── data/
│   ├── employee_attrition.csv          # Raw dataset
│   └── employee_attrition_cleaned.csv  # Cleaned & preprocessed dataset
├── src/
│   ├── 01_generate_dataset.py          # Script to generate the sample dataset
│   ├── 02_data_loading_inspection.py   # Step 1: Load & inspect the data
│   ├── 03_data_cleaning.py             # Step 2: Handle missing values, duplicates
│   ├── 04_feature_engineering.py       # Step 3: Encoding, feature selection
│   ├── 05_normalization.py             # Step 4: Normalization & scaling
│   ├── 06_eda.py                       # Step 5: Exploratory Data Analysis
│   └── 07_full_pipeline.py            # Complete end-to-end preprocessing pipeline
├── outputs/
│   └── (generated plots and analysis outputs)
└── report/
    └── Week1_Report.docx               # Final report document
```

## How to Run
```bash
# Install dependencies
pip install -r requirements.txt

# Generate the sample dataset
python src/01_generate_dataset.py

# Run each preprocessing step individually
python src/02_data_loading_inspection.py
python src/03_data_cleaning.py
python src/04_feature_engineering.py
python src/05_normalization.py
python src/06_eda.py

# Or run the complete pipeline
python src/07_full_pipeline.py
```

## Technologies Used
- Python 3.13
- NumPy — numerical operations
- Pandas — data manipulation and analysis
- Matplotlib & Seaborn — data visualization
- Scikit-learn — preprocessing utilities (LabelEncoder, MinMaxScaler, StandardScaler)
