import streamlit as st
import pandas as pd

from src.risk_model import calculate_risk

st.title("SupplyLens")

uploaded_file = st.file_uploader(
    "Upload Supplier CSV",
    type="csv"
)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    df["RiskScore"] = df.apply(
        calculate_risk,
        axis=1
    )

    st.subheader("Supplier Risk Scores")
    st.dataframe(df)

    st.subheader("Spend by Supplier")

    st.bar_chart(
        df.set_index("Supplier")["Spend"]
    )