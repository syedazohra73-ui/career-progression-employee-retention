import pandas as pd
import numpy as np

# ==========================================
# STAGE 1: LOAD AND INSPECT DATASET
# Career Progression & Promotion Gap Analysis
# ==========================================

# 1. Load dataset
df = pd.read_csv("employee_data.xls.csv")

print("\n========== DATASET LOADED ==========")
print("Number of rows:", df.shape[0])
print("Number of columns:", df.shape[1])


# 2. Display first 5 rows
print("\n========== FIRST 5 ROWS ==========")
print(df.head())


# 3. Display column names
print("\n========== COLUMN NAMES ==========")
print(df.columns.tolist())


# 4. Dataset information
print("\n========== DATA TYPES & INFORMATION ==========")
df.info()


# 5. Check missing values
print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())


# 6. Check duplicate rows
print("\n========== DUPLICATES ==========")
print("Duplicate rows:", df.duplicated().sum())


# 7. Statistical summary
print("\n========== STATISTICAL SUMMARY ==========")
print(df.describe())


# 8. Remove duplicate rows
df = df.drop_duplicates()

print("\n========== AFTER CLEANING ==========")
print("Rows after removing duplicates:", len(df))


# 9. Identify categorical columns
print("\n========== CATEGORICAL COLUMNS ==========")

categorical_columns = df.select_dtypes(
    include=["object"]
).columns

print(categorical_columns.tolist())


# 10. Display unique values
print("\n========== UNIQUE VALUES ==========")

for column in categorical_columns:
    print(f"\n{column}:")
    print(df[column].unique())


# 11. Save cleaned dataset
df.to_csv("employee_data_cleaned.csv", index=False)

print("\n========================================")
print("CLEANED DATASET SAVED SUCCESSFULLY!")
print("File: employee_data_cleaned.csv")
print("========================================")