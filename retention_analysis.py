import pandas as pd
import numpy as np

# ============================================================
# RETENTION ANALYSIS
# ============================================================

print("\n==========================================")
print("        EMPLOYEE RETENTION ANALYSIS")
print("==========================================")

# ------------------------------------------------------------
# 1. LOAD DATASET
# ------------------------------------------------------------

df = pd.read_csv("employee_career_clusters.csv")

print("\nDataset loaded successfully!")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])


# ------------------------------------------------------------
# 2. OVERALL ATTRITION
# ------------------------------------------------------------

print("\n========== OVERALL ATTRITION ==========")

attrition_counts = df["Attrition"].value_counts()

print(attrition_counts)

attrition_rate = df["Attrition"].mean() * 100

print(f"\nOverall Attrition Rate: {attrition_rate:.2f}%")


# ------------------------------------------------------------
# 3. ATTRITION BY CAREER CLUSTER
# ------------------------------------------------------------

print("\n========== ATTRITION BY CAREER CLUSTER ==========")

cluster_attrition = (
    df.groupby("Career_Cluster_Label")["Attrition"]
    .agg(["count", "sum", "mean"])
    .reset_index()
)

cluster_attrition["Attrition_Rate_%"] = (
    cluster_attrition["mean"] * 100
)

cluster_attrition = cluster_attrition.drop(columns=["mean"])

print(cluster_attrition)


# ------------------------------------------------------------
# 4. ATTRITION BY OVERTIME
# ------------------------------------------------------------

print("\n========== ATTRITION BY OVERTIME ==========")

overtime_attrition = (
    df.groupby("OverTime")["Attrition"]
    .agg(["count", "sum", "mean"])
    .reset_index()
)

overtime_attrition["Attrition_Rate_%"] = (
    overtime_attrition["mean"] * 100
)

overtime_attrition = overtime_attrition.drop(columns=["mean"])

print(overtime_attrition)


# ------------------------------------------------------------
# 5. ATTRITION BY JOB ROLE
# ------------------------------------------------------------

print("\n========== ATTRITION BY JOB ROLE ==========")

jobrole_attrition = (
    df.groupby("JobRole")["Attrition"]
    .agg(["count", "sum", "mean"])
    .reset_index()
)

jobrole_attrition["Attrition_Rate_%"] = (
    jobrole_attrition["mean"] * 100
)

jobrole_attrition = jobrole_attrition.drop(columns=["mean"])

jobrole_attrition = jobrole_attrition.sort_values(
    "Attrition_Rate_%",
    ascending=False
)

print(jobrole_attrition)


# ------------------------------------------------------------
# 6. ATTRITION BY DEPARTMENT
# ------------------------------------------------------------

print("\n========== ATTRITION BY DEPARTMENT ==========")

department_attrition = (
    df.groupby("Department")["Attrition"]
    .agg(["count", "sum", "mean"])
    .reset_index()
)

department_attrition["Attrition_Rate_%"] = (
    department_attrition["mean"] * 100
)

department_attrition = department_attrition.drop(columns=["mean"])

print(department_attrition)


# ------------------------------------------------------------
# 7. ATTRITION BY JOB SATISFACTION
# ------------------------------------------------------------

print("\n========== ATTRITION BY JOB SATISFACTION ==========")

satisfaction_attrition = (
    df.groupby("JobSatisfaction")["Attrition"]
    .agg(["count", "sum", "mean"])
    .reset_index()
)

satisfaction_attrition["Attrition_Rate_%"] = (
    satisfaction_attrition["mean"] * 100
)

satisfaction_attrition = satisfaction_attrition.drop(columns=["mean"])

print(satisfaction_attrition)


# ------------------------------------------------------------
# 8. ATTRITION BY JOB LEVEL
# ------------------------------------------------------------

print("\n========== ATTRITION BY JOB LEVEL ==========")

level_attrition = (
    df.groupby("JobLevel")["Attrition"]
    .agg(["count", "sum", "mean"])
    .reset_index()
)

level_attrition["Attrition_Rate_%"] = (
    level_attrition["mean"] * 100
)

level_attrition = level_attrition.drop(columns=["mean"])

print(level_attrition)


# ------------------------------------------------------------
# 9. RETENTION OPPORTUNITY ANALYSIS
# ------------------------------------------------------------

print("\n========== RETENTION OPPORTUNITY ==========")

retention_summary = (
    df.groupby("Retention_Opportunity_Level")
    .agg(
        Employees=("Employee_ID", "count"),
        Attrition_Count=("Attrition", "sum"),
        Average_Opportunity_Index=(
            "Retention_Opportunity_Index",
            "mean"
        )
    )
    .reset_index()
)

retention_summary["Attrition_Rate_%"] = (
    retention_summary["Attrition_Count"]
    / retention_summary["Employees"]
    * 100
)

print(retention_summary)


# ------------------------------------------------------------
# 10. CAREER STAGNATION & ATTRITION
# ------------------------------------------------------------

print("\n========== CAREER STAGNATION & ATTRITION ==========")

stagnation_analysis = (
    df.groupby("Career_Stagnation_Flag")["Attrition"]
    .agg(["count", "sum", "mean"])
    .reset_index()
)

stagnation_analysis["Attrition_Rate_%"] = (
    stagnation_analysis["mean"] * 100
)

stagnation_analysis = stagnation_analysis.drop(columns=["mean"])

print(stagnation_analysis)


# ------------------------------------------------------------
# 11. PROMOTION GAP & ATTRITION
# ------------------------------------------------------------

print("\n========== PROMOTION GAP & ATTRITION ==========")

promotion_analysis = (
    df.groupby("Promotion_Gap_Score")["Attrition"]
    .agg(["count", "sum", "mean"])
    .reset_index()
)

promotion_analysis["Attrition_Rate_%"] = (
    promotion_analysis["mean"] * 100
)

promotion_analysis = promotion_analysis.drop(columns=["mean"])

print(promotion_analysis)


# ------------------------------------------------------------
# 12. HIGH-PRIORITY RETENTION EMPLOYEES
# ------------------------------------------------------------

print("\n========== HIGH-PRIORITY RETENTION EMPLOYEES ==========")

high_priority = df[
    (df["Retention_Opportunity_Level"] == "High")
    & (df["Attrition"] == 0)
].copy()

print("Employees currently retained but requiring attention:",
      len(high_priority))

print(
    high_priority[
        [
            "Employee_ID",
            "Age",
            "JobRole",
            "JobLevel",
            "YearsAtCompany",
            "YearsInCurrentRole",
            "YearsSinceLastPromotion",
            "OverTime",
            "JobSatisfaction",
            "Career_Stagnation_Flag",
            "Retention_Opportunity_Index",
            "Career_Cluster_Label"
        ]
    ].head(10)
)


# ------------------------------------------------------------
# 13. SAVE RETENTION REPORT
# ------------------------------------------------------------

cluster_attrition.to_csv(
    "retention_by_career_cluster.csv",
    index=False
)

overtime_attrition.to_csv(
    "retention_by_overtime.csv",
    index=False
)

jobrole_attrition.to_csv(
    "retention_by_job_role.csv",
    index=False
)

department_attrition.to_csv(
    "retention_by_department.csv",
    index=False
)

retention_summary.to_csv(
    "retention_opportunity_summary.csv",
    index=False
)

stagnation_analysis.to_csv(
    "retention_by_stagnation.csv",
    index=False
)

promotion_analysis.to_csv(
    "retention_by_promotion_gap.csv",
    index=False
)

high_priority.to_csv(
    "high_priority_retention_employees.csv",
    index=False
)


# ------------------------------------------------------------
# 14. FINAL MESSAGE
# ------------------------------------------------------------

print("\n==========================================")
print("RETENTION ANALYSIS COMPLETED SUCCESSFULLY!")
print("==========================================")

print("\nReports created:")
print("1. retention_by_career_cluster.csv")
print("2. retention_by_overtime.csv")
print("3. retention_by_job_role.csv")
print("4. retention_by_department.csv")
print("5. retention_opportunity_summary.csv")
print("6. retention_by_stagnation.csv")
print("7. retention_by_promotion_gap.csv")
print("8. high_priority_retention_employees.csv")