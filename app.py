import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Career Progression & Employee Retention",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main {
    background-color: #f8fafc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1 {
    color: #0f172a;
    font-weight: 700;
}

h2 {
    color: #0f172a;
    font-weight: 650;
}

h3 {
    color: #1e293b;
}

[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #e2e8f0;
    padding: 18px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.insight-box {
    background-color: white;
    border-left: 5px solid #2563eb;
    padding: 15px;
    margin-bottom: 12px;
    border-radius: 8px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}

.warning-box {
    background-color: #fff7ed;
    border-left: 5px solid #f97316;
    padding: 15px;
    margin-bottom: 12px;
    border-radius: 8px;
}

.success-box {
    background-color: #f0fdf4;
    border-left: 5px solid #16a34a;
    padding: 15px;
    margin-bottom: 12px;
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    file_name = "employee_career_clusters.csv"

    df = pd.read_csv(file_name)

    return df


try:
    df = load_data()

except FileNotFoundError:

    st.error(
        "employee_career_clusters.csv was not found. "
        "Make sure it is inside the same folder as app.py."
    )

    st.stop()


# ============================================================
# PAGE TITLE
# ============================================================

st.title("📊 Career Progression & Employee Retention Dashboard")

st.markdown(
    "### Data-driven insights for career development and employee retention"
)

st.divider()


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.title("🔎 Filters")

# Department
departments = ["All"] + sorted(
    df["Department"].dropna().unique().tolist()
)

selected_department = st.sidebar.selectbox(
    "Department",
    departments
)

# Job Role
job_roles = ["All"] + sorted(
    df["JobRole"].dropna().unique().tolist()
)

selected_job_role = st.sidebar.selectbox(
    "Job Role",
    job_roles
)

# Overtime
overtime_options = ["All"] + sorted(
    df["OverTime"].dropna().unique().tolist()
)

selected_overtime = st.sidebar.selectbox(
    "Overtime",
    overtime_options
)

# Career Stage
career_stages = ["All"] + sorted(
    df["Career_Cluster_Label"].dropna().unique().tolist()
)

selected_career_stage = st.sidebar.selectbox(
    "Career Stage",
    career_stages
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()

if selected_department != "All":
    filtered_df = filtered_df[
        filtered_df["Department"] == selected_department
    ]

if selected_job_role != "All":
    filtered_df = filtered_df[
        filtered_df["JobRole"] == selected_job_role
    ]

if selected_overtime != "All":
    filtered_df = filtered_df[
        filtered_df["OverTime"] == selected_overtime
    ]

if selected_career_stage != "All":
    filtered_df = filtered_df[
        filtered_df["Career_Cluster_Label"] == selected_career_stage
    ]


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_employees = len(filtered_df)

if total_employees > 0:

    attrition_count = filtered_df["Attrition"].sum()

    attrition_rate = (
        attrition_count / total_employees
    ) * 100

    stagnation_count = filtered_df[
        filtered_df["Career_Stagnation_Flag"] == 1
    ].shape[0]

    high_retention = filtered_df[
        filtered_df["Retention_Opportunity_Level"] == "High"
    ].shape[0]

else:

    attrition_count = 0
    attrition_rate = 0
    stagnation_count = 0
    high_retention = 0


# ============================================================
# KPI SECTION
# ============================================================

st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Employees",
        f"{total_employees:,}"
    )

with col2:
    st.metric(
        "Attrition Rate",
        f"{attrition_rate:.2f}%"
    )

with col3:
    st.metric(
        "Career Stagnation",
        f"{stagnation_count:,}"
    )

with col4:
    st.metric(
        "High Retention Opportunity",
        f"{high_retention:,}"
    )


st.divider()


# ============================================================
# ATTRITION OVERVIEW
# ============================================================

st.header("📉 Attrition Overview")

col1, col2 = st.columns(2)


# ---------------- ATTRITION DONUT ----------------

with col1:

    attrition_data = pd.DataFrame({
        "Status": ["Stayed", "Left"],
        "Employees": [
            total_employees - attrition_count,
            attrition_count
        ]
    })

    fig_attrition = px.pie(
        attrition_data,
        names="Status",
        values="Employees",
        hole=0.55,
        title="Employee Attrition Distribution"
    )

    fig_attrition.update_traces(
        textinfo="percent+label"
    )

    st.plotly_chart(
        fig_attrition,
        use_container_width=True
    )


# ---------------- OVERTIME ----------------

with col2:

    overtime_table = (
        filtered_df
        .groupby("OverTime")
        .agg(
            count=("Attrition", "count"),
            attrition=("Attrition", "sum")
        )
        .reset_index()
    )

    overtime_table["Attrition Rate"] = (
        overtime_table["attrition"]
        / overtime_table["count"]
    ) * 100

    fig_overtime = px.bar(
        overtime_table,
        x="OverTime",
        y="Attrition Rate",
        text="Attrition Rate",
        title="Attrition Rate by Overtime"
    )

    fig_overtime.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    st.plotly_chart(
        fig_overtime,
        use_container_width=True
    )


# ============================================================
# CAREER PROGRESSION
# ============================================================

st.header("🚀 Career Progression Analysis")

col1, col2 = st.columns(2)


# ---------------- CAREER STAGE ----------------

with col1:

    career_stage_data = (
        filtered_df["Career_Cluster_Label"]
        .value_counts()
        .reset_index()
    )

    career_stage_data.columns = [
        "Career Stage",
        "Employees"
    ]

    fig_career = px.bar(
        career_stage_data,
        x="Career Stage",
        y="Employees",
        text="Employees",
        title="Employees by Career Stage"
    )

    fig_career.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig_career,
        use_container_width=True
    )


# ---------------- STAGNATION ----------------

with col2:

    stagnation_data = pd.DataFrame({
        "Status": [
            "No Stagnation",
            "Potential Stagnation"
        ],
        "Employees": [
            total_employees - stagnation_count,
            stagnation_count
        ]
    })

    fig_stagnation = px.pie(
        stagnation_data,
        names="Status",
        values="Employees",
        hole=0.55,
        title="Career Stagnation Status"
    )

    fig_stagnation.update_traces(
        textinfo="percent+label"
    )

    st.plotly_chart(
        fig_stagnation,
        use_container_width=True
    )


# ============================================================
# DEPARTMENT ANALYSIS
# ============================================================

st.header("🏢 Department Analysis")

department_data = (
    filtered_df
    .groupby("Department")
    .agg(
        Employees=("Attrition", "count"),
        Attrition=("Attrition", "sum")
    )
    .reset_index()
)

department_data["Attrition Rate"] = (
    department_data["Attrition"]
    / department_data["Employees"]
) * 100


fig_department = px.bar(
    department_data,
    x="Department",
    y="Attrition Rate",
    text="Attrition Rate",
    title="Attrition Rate by Department"
)

fig_department.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

st.plotly_chart(
    fig_department,
    use_container_width=True
)


# ============================================================
# JOB ROLE ANALYSIS
# ============================================================

st.header("💼 Job Role Analysis")

job_role_data = (
    filtered_df
    .groupby("JobRole")
    .agg(
        Employees=("Attrition", "count"),
        Attrition=("Attrition", "sum")
    )
    .reset_index()
)

job_role_data["Attrition Rate"] = (
    job_role_data["Attrition"]
    / job_role_data["Employees"]
) * 100

job_role_data = job_role_data.sort_values(
    "Attrition Rate",
    ascending=False
)


fig_job_role = px.bar(
    job_role_data,
    x="Attrition Rate",
    y="JobRole",
    orientation="h",
    text="Attrition Rate",
    title="Attrition Rate by Job Role"
)

fig_job_role.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

st.plotly_chart(
    fig_job_role,
    use_container_width=True
)


# ============================================================
# JOB SATISFACTION
# ============================================================

st.header("😊 Job Satisfaction vs Attrition")

satisfaction_data = (
    filtered_df
    .groupby("JobSatisfaction")
    .agg(
        Employees=("Attrition", "count"),
        Attrition=("Attrition", "sum")
    )
    .reset_index()
)

satisfaction_data["Attrition Rate"] = (
    satisfaction_data["Attrition"]
    / satisfaction_data["Employees"]
) * 100

fig_satisfaction = px.bar(
    satisfaction_data,
    x="JobSatisfaction",
    y="Attrition Rate",
    text="Attrition Rate",
    title="Attrition Rate by Job Satisfaction Level"
)

fig_satisfaction.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

st.plotly_chart(
    fig_satisfaction,
    use_container_width=True
)


# ============================================================
# RETENTION OPPORTUNITY
# ============================================================

st.header("🛡️ Retention Opportunity")

retention_data = (
    filtered_df["Retention_Opportunity_Level"]
    .value_counts()
    .reset_index()
)

retention_data.columns = [
    "Retention Level",
    "Employees"
]

fig_retention = px.pie(
    retention_data,
    names="Retention Level",
    values="Employees",
    hole=0.5,
    title="Retention Opportunity Distribution"
)

fig_retention.update_traces(
    textinfo="percent+label"
)

st.plotly_chart(
    fig_retention,
    use_container_width=True
)


# ============================================================
# AUTOMATIC INSIGHTS
# ============================================================

st.header("💡 Key Insights & Recommendations")

if total_employees > 0:

    # Overtime insight
    overtime_rates = (
        filtered_df
        .groupby("OverTime")["Attrition"]
        .mean()
        * 100
    )

    if "Yes" in overtime_rates.index and "No" in overtime_rates.index:

        overtime_difference = (
            overtime_rates["Yes"]
            - overtime_rates["No"]
        )

        st.markdown(
            f"""
            <div class="warning-box">
            <b>⚠️ Overtime Risk:</b><br>
            Employees working overtime have an attrition rate of
            <b>{overtime_rates["Yes"]:.2f}%</b>, compared with
            <b>{overtime_rates["No"]:.2f}%</b> for employees without overtime.
            This represents a difference of approximately
            <b>{overtime_difference:.2f} percentage points</b>.
            </div>
            """,
            unsafe_allow_html=True
        )

    # Job role insight
    if len(job_role_data) > 0:

        highest_role = job_role_data.iloc[0]

        st.markdown(
            f"""
            <div class="insight-box">
            <b>💼 Highest-Risk Job Role:</b><br>
            <b>{highest_role["JobRole"]}</b> has the highest observed
            attrition rate at <b>{highest_role["Attrition Rate"]:.2f}%</b>.
            </div>
            """,
            unsafe_allow_html=True
        )

    # Department insight
    if len(department_data) > 0:

        highest_department = department_data.loc[
            department_data["Attrition Rate"].idxmax()
        ]

        st.markdown(
            f"""
            <div class="insight-box">
            <b>🏢 Department Risk:</b><br>
            <b>{highest_department["Department"]}</b> has the highest
            attrition rate at
            <b>{highest_department["Attrition Rate"]:.2f}%</b>.
            </div>
            """,
            unsafe_allow_html=True
        )

    # Stagnation insight
    stagnation_percentage = (
        stagnation_count / total_employees
    ) * 100

    st.markdown(
        f"""
        <div class="warning-box">
        <b>🚨 Career Stagnation:</b><br>
        <b>{stagnation_count:,}</b> employees
        ({stagnation_percentage:.2f}% of the filtered workforce)
        are identified as having potential career stagnation.
        </div>
        """,
        unsafe_allow_html=True
    )

    # Retention insight
    retention_percentage = (
        high_retention / total_employees
    ) * 100

    st.markdown(
        f"""
        <div class="success-box">
        <b>🛡️ Retention Opportunity:</b><br>
        <b>{high_retention:,}</b> employees
        ({retention_percentage:.2f}% of the filtered workforce)
        have a high retention opportunity score.
        These employees can be prioritized for career development,
        recognition and growth programs.
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# HIGH PRIORITY EMPLOYEES
# ============================================================

st.header("🚨 High-Priority Retention Employees")

priority_df = filtered_df[
    filtered_df["Retention_Opportunity_Level"] == "High"
].copy()

priority_columns = [
    "Employee_ID",
    "Age",
    "Department",
    "JobRole",
    "JobLevel",
    "YearsAtCompany",
    "YearsInCurrentRole",
    "YearsSinceLastPromotion",
    "OverTime",
    "JobSatisfaction",
    "Career_Cluster_Label",
    "Retention_Opportunity_Index"
]

available_columns = [
    col for col in priority_columns
    if col in priority_df.columns
]

priority_df = priority_df[available_columns]

priority_df = priority_df.sort_values(
    "Retention_Opportunity_Index",
    ascending=False
)

st.dataframe(
    priority_df.head(20),
    use_container_width=True,
    hide_index=True
)


# ============================================================
# DOWNLOAD DATA
# ============================================================

st.header("📥 Download Data")

download_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Employee Data",
    data=download_data,
    file_name="filtered_employee_career_data.csv",
    mime="text/csv"
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center">

    <h3>🎯 Career Progression & Employee Retention Analytics</h3>

    <p>
    Built using Python • Pandas • Scikit-learn • Plotly • Streamlit
    </p>

    <p>
    <b>Project Focus:</b>
    Career Development, Employee Retention & Data-Driven HR Analytics
    </p>

    </div>
    """,
    unsafe_allow_html=True
)