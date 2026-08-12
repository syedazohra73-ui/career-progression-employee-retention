# Career Progression & Employee Retention Analytics

## 📊 Project Overview

This project analyzes employee career progression and retention patterns using data analytics and machine learning.

The main goal is to identify:

- Employee attrition patterns
- Career progression stages
- Potential career stagnation
- Promotion gaps
- Employee retention opportunities
- High-priority employees who may require retention strategies

The project also provides an interactive Streamlit dashboard for exploring the results.

---

## 🎯 Project Objectives

1. Analyze employee attrition.
2. Identify employees experiencing career stagnation.
3. Analyze promotion gaps and career progression.
4. Identify different employee career stages using clustering.
5. Identify employees with high retention opportunities.
6. Analyze attrition based on department, job role and overtime.
7. Provide data-driven recommendations for employee retention.

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Plotly
- Streamlit
- Matplotlib

---

## 🔍 Project Workflow

The project follows these major stages:

### 1. Data Analysis

The employee dataset is loaded and analyzed for:

- Dataset structure
- Missing values
- Duplicate records
- Statistical summaries
- Categorical variables

### 2. Exploratory Data Analysis

Employee attrition and career-related patterns are analyzed.

### 3. Feature Engineering

New career-related features are created, including:

- Promotion Gap Ratio
- Promotion Gap Score
- Training Need Indicator
- Career Stagnation Flag
- Retention Opportunity Index
- Retention Opportunity Level

### 4. Career Clustering

Machine learning clustering is used to identify employee career stages.

The project identifies three career stages:

- Early-Career Explorer
- Developing Professional
- Experienced Professional

### 5. Retention Analysis

Attrition is analyzed across:

- Overtime
- Department
- Job Role
- Job Satisfaction
- Job Level
- Career Stage
- Promotion Gap
- Career Stagnation

### 6. Interactive Dashboard

A Streamlit dashboard provides interactive filters and visualizations for HR analysis.

---

## 📈 Key Findings

### Employee Attrition

Total Employees: 1,470

Overall Attrition Rate: 16.12%

### Career Stagnation

338 employees were identified as having potential career stagnation.

### Retention Opportunity

436 employees were identified as having a high retention opportunity.

### Overtime Risk

Employees working overtime have a significantly higher attrition rate than employees who do not work overtime.

- Overtime: 30.53%
- No Overtime: 10.44%

### Job Role Risk

Sales Representatives have the highest observed attrition rate at approximately 39.76%.

### Department Risk

The Sales department has the highest observed attrition rate at approximately 20.63%.

---

## 📊 Dashboard Features

The dashboard includes:

- Department filter
- Job Role filter
- Overtime filter
- Career Stage filter
- Employee Attrition Distribution
- Attrition by Overtime
- Career Progression Analysis
- Career Stagnation Analysis
- Department Analysis
- Job Role Analysis
- Job Satisfaction Analysis
- Retention Opportunity Analysis
- High-Priority Retention Employees
- Downloadable datasets

---

## 📁 Project Structure

```text
Career_Progression_Project/
│
├── analysis.py
├── eda.py
├── feature_engineering.py
├── clustering.py
├── retention_analysis.py
├── app.py
│
├── employee_career_features.csv
├── employee_career_clusters.csv
├── employee_data_cleaned.csv
│
├── high_priority_retention_employees.csv
├── retention_by_career_cluster.csv
├── retention_by_department.csv
├── retention_by_job_role.csv
├── retention_by_overtime.csv
├── retention_by_promotion_gap.csv
├── retention_by_stagnation.csv
├── retention_opportunity_summary.csv
│
├── requirements.txt
└── README.md