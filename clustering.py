import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import linkage, fcluster


# ============================================================
# STAGE 4: CAREER PATH CLUSTERING
# ============================================================

print("==========================================")
print("CAREER PATH CLUSTERING")
print("==========================================")


# ============================================================
# 1. LOAD DATA
# ============================================================

df = pd.read_csv("employee_career_features.csv")

print()
print("Dataset loaded successfully!")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])


# ============================================================
# 2. SELECT CAREER FEATURES
# ============================================================

career_features = [
    "JobLevel",
    "TotalWorkingYears",
    "YearsAtCompany",
    "YearsInCurrentRole",
    "YearsSinceLastPromotion",
    "YearsWithCurrManager",
    "TrainingTimesLastYear",
    "Promotion_Gap_Ratio",
    "Role_Stagnation_Index",
    "Training_Intensity_Score",
    "Manager_Stability_Indicator"
]

X = df[career_features].copy()


# ============================================================
# 3. HANDLE MISSING VALUES
# ============================================================

X = X.replace([np.inf, -np.inf], np.nan)
X = X.fillna(0)


# ============================================================
# 4. STANDARDIZE FEATURES
# ============================================================

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

print()
print("Career features normalized successfully.")


# ============================================================
# 5. TEST DIFFERENT K VALUES
# ============================================================

print()
print("========== TESTING CLUSTER NUMBERS ==========")

scores = {}

for k in range(2, 7):

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    labels = model.fit_predict(X_scaled)

    score = silhouette_score(
        X_scaled,
        labels
    )

    scores[k] = score

    print(
        f"K = {k} | "
        f"Silhouette Score = {score:.4f}"
    )


# ============================================================
# 6. SELECT BEST K
# ============================================================

best_k = max(
    scores,
    key=scores.get
)

print()
print("==========================================")
print("BEST K:", best_k)
print(
    "BEST SILHOUETTE SCORE:",
    round(scores[best_k], 4)
)
print("==========================================")


# ============================================================
# 7. FINAL K-MEANS
# ============================================================

kmeans = KMeans(
    n_clusters=best_k,
    random_state=42,
    n_init=10
)

df["Career_Cluster"] = kmeans.fit_predict(
    X_scaled
)


# ============================================================
# 8. CLUSTER DISTRIBUTION
# ============================================================

print()
print("========== CLUSTER DISTRIBUTION ==========")

print(
    df["Career_Cluster"]
    .value_counts()
    .sort_index()
)


# ============================================================
# 9. CLUSTER PROFILE
# ============================================================

profile_features = [
    "JobLevel",
    "TotalWorkingYears",
    "YearsAtCompany",
    "YearsInCurrentRole",
    "YearsSinceLastPromotion",
    "YearsWithCurrManager",
    "TrainingTimesLastYear",
    "Promotion_Gap_Ratio",
    "Role_Stagnation_Index",
    "Training_Intensity_Score",
    "Manager_Stability_Indicator",
    "Retention_Opportunity_Index"
]

cluster_profile = (
    df.groupby("Career_Cluster")[profile_features]
    .mean()
    .round(2)
)

print()
print("========== CLUSTER PROFILE ==========")
print(cluster_profile)


# ============================================================
# 10. HIERARCHICAL CLUSTERING
# ============================================================

hierarchical = linkage(
    X_scaled,
    method="ward"
)

hierarchical_labels = fcluster(
    hierarchical,
    t=best_k,
    criterion="maxclust"
)

hierarchical_score = silhouette_score(
    X_scaled,
    hierarchical_labels
)

print()
print("========== HIERARCHICAL CLUSTERING ==========")

print(
    "Hierarchical Silhouette Score:",
    round(hierarchical_score, 4)
)


# ============================================================
# 11. CAREER CLUSTER LABELS
# ============================================================

print()
print("========== ASSIGNING CAREER LABELS ==========")

# Based on the actual profiles obtained from your dataset:
#
# Cluster 0:
# ~0.95 years at company
# ~0.12 years in current role
# ~0.10 years since promotion
# = Early-career employees
#
# Cluster 1:
# ~5.26 years at company
# ~3.40 years in current role
# ~1.02 years since promotion
# = Developing professionals
#
# Cluster 2:
# ~14.71 years at company
# ~8.61 years in current role
# ~6.19 years since promotion
# = Experienced professionals

cluster_labels = {
    0: "Early-Career Explorer",
    1: "Developing Professional",
    2: "Experienced Professional"
}

df["Career_Cluster_Label"] = (
    df["Career_Cluster"].map(cluster_labels)
)


# ============================================================
# 12. SHOW FINAL LABELS
# ============================================================

print()
print("========== CAREER CLUSTER LABELS ==========")

print(
    df[
        [
            "Career_Cluster",
            "Career_Cluster_Label"
        ]
    ]
    .drop_duplicates()
    .sort_values("Career_Cluster")
)


print()
print("========== LABEL DISTRIBUTION ==========")

print(
    df["Career_Cluster_Label"]
    .value_counts()
)


# ============================================================
# 13. SAVE DATASET
# ============================================================

output_file = "employee_career_clusters.csv"

df.to_csv(
    output_file,
    index=False
)


# ============================================================
# 14. COMPLETE
# ============================================================

print()
print("==========================================")
print("CLUSTERING COMPLETED SUCCESSFULLY!")
print("==========================================")

print()
print("Final dataset saved as:")
print(output_file)