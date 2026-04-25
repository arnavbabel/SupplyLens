import streamlit as st
import pandas as pd

from src.risk_model import calculate_risk
from src.sustainability import calculate_sustainability
from src.concentration import add_supplier_share, label_supplier_share, calculate_category_hhi
from src.recommendations import generate_recommendations
from src.cost_model import add_cost_score

st.title("SupplyLens")

# ======================
# SIDEBAR (USER CONTROLS)
# ======================
st.sidebar.header("Decision Priorities")

preset = st.sidebar.selectbox(
    "Choose Priority Profile",
    ["Balanced", "Cost-First", "Risk-First", "Sustainability-First", "Custom"]
)

if preset == "Balanced":
    cost_weight = 33
    risk_weight = 33
    sustainability_weight = 34

elif preset == "Cost-First":
    cost_weight = 50
    risk_weight = 30
    sustainability_weight = 20

elif preset == "Risk-First":
    cost_weight = 20
    risk_weight = 60
    sustainability_weight = 20

elif preset == "Sustainability-First":
    cost_weight = 20
    risk_weight = 20
    sustainability_weight = 60

else:
    cost_weight = st.sidebar.slider("Cost Priority", 0, 100, 33)
    risk_weight = st.sidebar.slider("Risk Priority", 0, 100, 33)
    sustainability_weight = st.sidebar.slider("Sustainability Priority", 0, 100, 34)

total = cost_weight + risk_weight + sustainability_weight

cost_weight = cost_weight / total
risk_weight = risk_weight / total
sustainability_weight = sustainability_weight / total


# ======================
# HELPER FUNCTION
# ======================
def label_risk(score):
    if score <= 20:
        return "Very Low"
    elif score <= 40:
        return "Low/Moderate"
    elif score <= 70:
        return "Moderate/High"
    else:
        return "High/Critical"


# ======================
# FILE UPLOAD
# ======================
uploaded_file = st.file_uploader("Upload Supplier CSV", type="csv")


if uploaded_file:

    # ======================
    # LOAD DATA
    # ======================
    df = pd.read_csv(uploaded_file)

    # ======================
    # FEATURE ENGINEERING
    # ======================
    df["Risk Score"] = df.apply(calculate_risk, axis=1)
    df["Risk Level"] = df["Risk Score"].apply(label_risk)

    df["Sustainability Score"] = df.apply(calculate_sustainability, axis=1)

    df = add_cost_score(df)

    df["Risk Adjusted Score"] = 100 - df["Risk Score"]

    df["Overall Score"] = (
        cost_weight * df["Cost Score"] +
        risk_weight * df["Risk Adjusted Score"] +
        sustainability_weight * df["Sustainability Score"]
    ).round(1)

    df = add_supplier_share(df)
    df["Supplier Share Risk"] = df["Supplier Share %"].apply(label_supplier_share)

    # ======================
    # CATEGORY ANALYSIS
    # ======================
    hhi_df = calculate_category_hhi(df)
    hhi_lookup = dict(zip(hhi_df["Category"], hhi_df["HHI"]))

    df["Recommendation"] = df.apply(
        lambda row: generate_recommendations(row, hhi_lookup),
        axis=1
    )

    # ======================
    # DASHBOARD
    # ======================

    st.subheader("Executive Snapshot")

    avg_risk = df["Risk Score"].mean()
    avg_sustainability = df["Sustainability Score"].mean()
    high_risk_pct = (df["Risk Score"] >= 70).mean() * 100
    avg_hhi = hhi_df["HHI"].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Avg Risk Score", round(avg_risk, 1))
    col2.metric("Avg Sustainability", round(avg_sustainability, 1))
    col3.metric("% High Risk Suppliers", f"{round(high_risk_pct, 1)}%")
    col4.metric("Avg Category HHI", round(avg_hhi, 0))

    # ======================
    # RANKED SUPPLIERS (NEW FEATURE)
    # ======================
    st.subheader("Ranked Suppliers")

    st.dataframe(
        df.sort_values("Overall Score", ascending=False)[
            [
                "Supplier Name",
                "Category",
                "Annual Spend",
                "Cost Score",
                "Risk Score",
                "Sustainability Score",
                "Overall Score"
            ]
        ]
    )

    # ======================
    # SUPPLIER TABLE
    # ======================
    st.subheader("Supplier Overview")
    st.dataframe(df)

    # ======================
    # CHART
    # ======================
    st.subheader("Spend by Supplier")
    st.bar_chart(df.set_index("Supplier Name")["Annual Spend"])


else:
    st.info("Upload a supplier CSV to begin analysis.")