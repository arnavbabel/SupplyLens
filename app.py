import streamlit as st
import pandas as pd

from src.risk_model import calculate_risk
from src.concentration import calculate_hhi
from src.sustainability import sustainability_score

st.title("SupplyLens")

# Helper functions
def label_risk(score):
    if score >= 60:
        return "High"
    elif score >= 40:
        return "Medium"
    else:
        return "Low"


# File upload
uploaded_file = st.file_uploader(
    "Upload Supplier CSV",
    type="csv"
)

if uploaded_file:
    # Load data
    df = pd.read_csv(uploaded_file)

    # Feature engineering
    df["RiskScore"] = df.apply(calculate_risk, axis=1)
    df["RiskLevel"] = df["RiskScore"].apply(label_risk)

    df["SustainabilityScore"] = df.apply(sustainability_score, axis=1)

    # Portfolio metrics
    hhi = calculate_hhi(df)
    avg_sustainability = df["SustainabilityScore"].mean()

    # Key insights section
    st.subheader("Key Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(label="HHI (Concentration)", value=round(hhi, 4))

        if hhi > 0.25:
            st.warning("High supplier concentration risk")
        elif hhi > 0.15:
            st.info("Moderate supplier concentration risk")
        else:
            st.success("Low concentration risk")

    with col2:
        st.metric(
            label="Avg Sustainability Score",
            value=round(avg_sustainability, 1)
        )

        if avg_sustainability < 60:
            st.warning("Low overall sustainability performance")
        else:
            st.success("Healthy sustainability profile")

    # Main table
    st.subheader("Supplier Risk Table")
    st.dataframe(df)

    # Spend visualization
    st.subheader("Spend by Supplier")
    st.bar_chart(df.set_index("Supplier")["Spend"])

    # Top risk suppliers
    st.subheader("Top Risk Suppliers")
    st.dataframe(
        df.sort_values("RiskScore", ascending=False).head(5)
    )

else:
    st.info("Upload a supplier CSV to begin analysis.")