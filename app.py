import streamlit as st
import pandas as pd

from src.risk_model import calculate_risk
from src.concentration import calculate_hhi

st.title("SupplyLens")

def label_risk(score):
    if score >= 60:
        return "High"
    elif score >= 40:
        return "Medium"
    else:
        return "Low"

uploaded_file = st.file_uploader(
    "Upload Supplier CSV",
    type="csv"
)

if uploaded_file:
    # Load data
    df = pd.read_csv(uploaded_file)

    # Calculate supplier risk
    df["RiskScore"] = df.apply(
        calculate_risk,
        axis=1
    )

    df["RiskLevel"] = df["RiskScore"].apply(label_risk)

    # Display table
    st.subheader("Supplier Risk Scores")
    st.dataframe(df)

    # Spend chart
    st.subheader("Spend by Supplier")
    st.bar_chart(
        df.set_index("Supplier")["Spend"]
    )

    # HHI calculation
    hhi = calculate_hhi(df)

    st.subheader("Supplier Concentration")
    st.metric(
        label="HHI",
        value=hhi
    )

    if hhi > 0.25:
        st.warning("High supplier concentration risk")
    elif hhi > 0.15:
        st.info("Moderate supplier concentration")
    else:
        st.success("Low concentration risk")

else:
    st.info("Upload a supplier CSV to begin.")