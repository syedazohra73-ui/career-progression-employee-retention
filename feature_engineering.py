import pandas as pd
import numpy as np

# ==========================================
# STAGE 3: FEATURE ENGINEERING
# ==========================================

# Load the original dataset
df = pd.read_csv("employee_data.xls.csv")

print("========== DATASET LOADED ==========")
print("Rows:", len(df))
print("Columns:", len(df.columns))


# ==========================================
# 1. CREATE EMPLOYEE ID
# ==========================================

df["Employee_ID"] = [
    f"EMP{i:04d}" for i in range(1, len(df) + 1)
]


# ==========================================
# 2. PROMOTION GAP RATIO
# ==========================================

# Avoid division by zero for employees
# who have just joined the company.

df["Promotion_Gap_Ratio"] = np.where(
    df["YearsAtCompany"] > 0,
    df["YearsSinceLastPromotion"] / df["YearsAtCompany"],
    0
)


# ==========================================
# 3. ROLE STAGNATION INDEX
# ==========================================

df["Role_Stagnation_Index"] = np.where(
    df["YearsAtCompany"] > 0,
    df["YearsInCurrentRole"] / df["YearsAtCompany"],
    0
)


# ==========================================
# 4. TRAINING INTENSITY SCORE
# ==========================================

df["Training_Intensity_Score"] = np.where(
    df["YearsAtCompany"] > 0,
    df["TrainingTimesLastYear"] / df["YearsAtCompany"],
    df["TrainingTimesLastYear"]
)


# ==========================================
# 5. MANAGER STABILITY INDICATOR
# ==========================================

df["Manager_Stability_Indicator"] = np.where(
    df["YearsAtCompany"] > 0,
    df["YearsWithCurrManager"] / df["YearsAtCompany"],
    0
)


# ==========================================
# 6. PROMOTION GAP SCORE
# ==========================================

def promotion_gap_score(row):

    promotion_gap = row["YearsSinceLastPromotion"]
    role_years = row["YearsInCurrentRole"]

    if promotion_gap >= 5 or role_years >= 7:
        return "High"

    elif promotion_gap >= 3 or role_years >= 4:
        return "Medium"

    else:
        return "Low"


df["Promotion_Gap_Score"] = df.apply(
    promotion_gap_score,
    axis=1
)


# ==========================================
# 7. TRAINING NEED INDICATOR
# ==========================================

def training_need(row):

    training = row["TrainingTimesLastYear"]
    role_years = row["YearsInCurrentRole"]

    if training <= 1 and role_years >= 3:
        return "High"

    elif training <= 2:
        return "Medium"

    else:
        return "Low"


df["Training_Need_Indicator"] = df.apply(
    training_need,
    axis=1
)


# ==========================================
# 8. CAREER STAGNATION FLAG
# ==========================================

df["Career_Stagnation_Flag"] = np.where(
    (
        (df["YearsSinceLastPromotion"] >= 3)
        &
        (df["YearsInCurrentRole"] >= 3)
    ),
    1,
    0
)


# ==========================================
# 9. RETENTION OPPORTUNITY INDEX
# ==========================================

# Higher score = stronger opportunity
# for proactive career intervention.

df["Retention_Opportunity_Index"] = (
    df["Promotion_Gap_Ratio"] * 40
    +
    df["Role_Stagnation_Index"] * 30
    +
    df["Manager_Stability_Indicator"] * 15
    +
    (4 - df["JobSatisfaction"]) * 5
    +
    (3 - df["TrainingTimesLastYear"]).clip(lower=0) * 10
)


# Keep the score within a reasonable range
df["Retention_Opportunity_Index"] = (
    df["Retention_Opportunity_Index"]
    .clip(lower=0, upper=100)
)


# ==========================================
# 10. RETENTION OPPORTUNITY LEVEL
# ==========================================

def opportunity_level(score):

    if score >= 60:
        return "High"

    elif score >= 30:
        return "Medium"

    else:
        return "Low"


df["Retention_Opportunity_Level"] = (
    df["Retention_Opportunity_Index"]
    .apply(opportunity_level)
)


# ==========================================
# 11. DISPLAY NEW FEATURES
# ==========================================

new_features = [
    "Employee_ID",
    "Promotion_Gap_Ratio",
    "Role_Stagnation_Index",
    "Training_Intensity_Score",
    "Manager_Stability_Indicator",
    "Promotion_Gap_Score",
    "Training_Need_Indicator",
    "Career_Stagnation_Flag",
    "Retention_Opportunity_Index",
    "Retention_Opportunity_Level"
]

print("\n========== NEW FEATURES ==========")
print(df[new_features].head(10))


# ==========================================
# 12. FEATURE SUMMARY
# ==========================================

print("\n========== PROMOTION GAP SCORE ==========")
print(df["Promotion_Gap_Score"].value_counts())


print("\n========== TRAINING NEED ==========")
print(df["Training_Need_Indicator"].value_counts())


print("\n========== CAREER STAGNATION ==========")
print(df["Career_Stagnation_Flag"].value_counts())


print("\n========== RETENTION OPPORTUNITY ==========")
print(df["Retention_Opportunity_Level"].value_counts())


# ==========================================
# 13. SAVE ENGINEERED DATASET
# ==========================================

df.to_csv(
    "employee_career_features.csv",
    index=False
)

print("\n==========================================")
print("FEATURE ENGINEERING COMPLETED SUCCESSFULLY!")
print("==========================================")

print("\nNew dataset saved as:")
print("employee_career_features.csv")