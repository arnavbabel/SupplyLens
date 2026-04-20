import streamlit as st
import pandas as pd

from src.risk_model import calculate_risk
from src.sustainability import calculate_sustainability
from src.concentration import add_supplier_share, label_supplier_share, calculate_category_hhi
from src.recommendations import generate_recommendations

st.title("SupplyLens")

def label_risk(score):
    if score <= 20:
        return "Very Low"
    elif score <= 40:
        return "Low/Moderate"
    elif score <= 70:
        return "Moderate/High"
    else:
        return "High/Critical"


uploaded_file = st.file_uploader("Upload Supplier CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Supplier-level calculations
    df["Risk Score"] = df.apply(calculate_risk, axis=1)
    df["Risk Level"] = df["Risk Score"].apply(label_risk)

    df["Sustainability Score"] = df.apply(calculate_sustainability, axis=1)

    df = add_supplier_share(df)
    df["Supplier Share Risk"] = df["Supplier Share %"].apply(label_supplier_share)

    # Category-level concentration
    hhi_df = calculate_category_hhi(df)
    hhi_lookup = dict(zip(hhi_df["Category"], hhi_df["HHI"]))

    # Recommendations
    df["Recommendation"] = df.apply(
        lambda row: generate_recommendations(row, hhi_lookup),
        axis=1
    )

    # Dashboard
    st.subheader("Supplier Overview")
    st.dataframe(df)

    st.subheader("Category Concentration (HHI)")
    st.dataframe(hhi_df)

    st.subheader("Top Risk Suppliers")
    st.dataframe(
        df.sort_values("Risk Score", ascending=False)[
            ["Supplier Name", "Category", "Annual Spend", "Risk Score", "Risk Level", "Recommendation"]
        ].head(10)
    )

    st.subheader("Spend by Supplier")
    st.bar_chart(df.set_index("Supplier Name")["Annual Spend"])

else:
    st.info("Upload a supplier CSV to begin.")