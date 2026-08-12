import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# STAGE 2: EXPLORATORY DATA ANALYSIS
# ==========================================

# Load dataset
df = pd.read_csv("employee_data.xls.csv")

print("Dataset loaded successfully!")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])


# ==========================================
# 1. ATTRITION DISTRIBUTION
# ==========================================

print("\n========== ATTRITION ==========")
print(df["Attrition"].value_counts())

plt.figure(figsize=(7, 5))
sns.countplot(data=df, x="Attrition")
plt.title("Employee Attrition Distribution")
plt.xlabel("Attrition (0 = Stayed, 1 = Left)")
plt.ylabel("Number of Employees")
plt.show()


# ==========================================
# 2. ATTRITION BY DEPARTMENT
# ==========================================

plt.figure(figsize=(8, 5))
sns.countplot(data=df, x="Department", hue="Attrition")
plt.title("Attrition by Department")
plt.xlabel("Department")
plt.ylabel("Number of Employees")
plt.xticks(rotation=15)
plt.show()


# ==========================================
# 3. ATTRITION BY JOB ROLE
# ==========================================

plt.figure(figsize=(10, 6))
sns.countplot(data=df, y="JobRole", hue="Attrition")
plt.title("Attrition by Job Role")
plt.xlabel("Number of Employees")
plt.ylabel("Job Role")
plt.show()


# ==========================================
# 4. YEARS SINCE LAST PROMOTION
# ==========================================

plt.figure(figsize=(9, 5))
sns.histplot(
    data=df,
    x="YearsSinceLastPromotion",
    hue="Attrition",
    multiple="stack",
    bins=15
)

plt.title("Years Since Last Promotion vs Attrition")
plt.xlabel("Years Since Last Promotion")
plt.ylabel("Number of Employees")
plt.show()


# ==========================================
# 5. YEARS IN CURRENT ROLE
# ==========================================

plt.figure(figsize=(9, 5))
sns.boxplot(
    data=df,
    x="Attrition",
    y="YearsInCurrentRole"
)

plt.title("Years in Current Role vs Attrition")
plt.xlabel("Attrition (0 = Stayed, 1 = Left)")
plt.ylabel("Years in Current Role")
plt.show()


# ==========================================
# 6. YEARS AT COMPANY
# ==========================================

plt.figure(figsize=(9, 5))
sns.boxplot(
    data=df,
    x="Attrition",
    y="YearsAtCompany"
)

plt.title("Years at Company vs Attrition")
plt.xlabel("Attrition (0 = Stayed, 1 = Left)")
plt.ylabel("Years at Company")
plt.show()


# ==========================================
# 7. TRAINING VS ATTRITION
# ==========================================

plt.figure(figsize=(9, 5))
sns.countplot(
    data=df,
    x="TrainingTimesLastYear",
    hue="Attrition"
)

plt.title("Training Frequency vs Attrition")
plt.xlabel("Training Times Last Year")
plt.ylabel("Number of Employees")
plt.show()


# ==========================================
# 8. OVERTIME VS ATTRITION
# ==========================================

plt.figure(figsize=(7, 5))
sns.countplot(
    data=df,
    x="OverTime",
    hue="Attrition"
)

plt.title("Overtime vs Attrition")
plt.xlabel("Overtime")
plt.ylabel("Number of Employees")
plt.show()


# ==========================================
# 9. JOB SATISFACTION VS ATTRITION
# ==========================================

plt.figure(figsize=(8, 5))
sns.countplot(
    data=df,
    x="JobSatisfaction",
    hue="Attrition"
)

plt.title("Job Satisfaction vs Attrition")
plt.xlabel("Job Satisfaction (1 = Low, 4 = High)")
plt.ylabel("Number of Employees")
plt.show()


# ==========================================
# 10. PROMOTION STAGNATION
# ==========================================

stagnation = df[
    (df["YearsSinceLastPromotion"] >= 3) &
    (df["YearsInCurrentRole"] >= 3)
]

print("\n========== PROMOTION STAGNATION ==========")
print("Employees with potential stagnation:", len(stagnation))

print("\nAttrition among potential stagnation employees:")
print(stagnation["Attrition"].value_counts())


# ==========================================
# 11. CAREER FEATURES SUMMARY
# ==========================================

career_features = [
    "YearsAtCompany",
    "YearsInCurrentRole",
    "YearsSinceLastPromotion",
    "YearsWithCurrManager",
    "TrainingTimesLastYear"
]

print("\n========== CAREER FEATURE SUMMARY ==========")
print(df[career_features].describe())


print("\n==========================================")
print("EDA COMPLETED SUCCESSFULLY!")
print("==========================================")