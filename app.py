import streamlit as st
import pandas as pd

from src.risk_model import calculate_risk
from src.sustainability import calculate_sustainability
from src.concentration import add_supplier_share, label_supplier_share, calculate_category_hhi
from src.recommendations import generate_recommendations

st.title("SupplyLens")


# Helper functions
def label_risk(score):
    if score <= 20:
        return "Very Low"
    elif score <= 40:
        return "Low/Moderate"
    elif score <= 70:
        return "Moderate/High"
    else:
        return "High/Critical"


# File Upload
uploaded_file = st.file_uploader("Upload Supplier CSV", type="csv")

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    # Feature Engineering
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

    # Executive Snapshot
    st.subheader("Executive Snapshot")

    avg_risk = df["Risk Score"].mean()
    avg_sustainability = df["Sustainability Score"].mean()
    high_risk_pct = (df["Risk Score"] >= 70).mean() * 100
    avg_hhi = hhi_df["HHI"].mean()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Avg Risk Score", round(avg_risk, 1))
    with col2:
        st.metric("Avg Sustainability", round(avg_sustainability, 1))
    with col3:
        st.metric("% High Risk Suppliers", f"{round(high_risk_pct, 1)}%")
    with col4:
        st.metric("Avg Category HHI", round(avg_hhi, 0))

    # Key Insight
    st.subheader("Key Insight")

    if avg_hhi > 2500:
        st.warning("Supplier base is highly concentrated. Immediate diversification may be required.")
    elif high_risk_pct > 20:
        st.warning("Significant portion of suppliers are high risk.")
    elif avg_sustainability < 60:
        st.warning("Overall sustainability performance is below target.")
    else:
        st.success("Supply base is stable with no major risks detected.")

    # Critical Risks
    st.subheader("Critical Risks")

    high_risk_df = df[df["Risk Score"] >= 70]

    if not high_risk_df.empty:
        st.error(f"{len(high_risk_df)} supplier(s) require immediate attention")

        for _, row in high_risk_df.iterrows():
            st.markdown(f"""
**{row['Supplier Name']}** ({row['Category']})  
- Risk Score: {row['Risk Score']}  
- Action: {row['Recommendation']}
""")
    else:
        st.success("No critical supplier risks identified")

    # Sustainability Watchlist
    st.subheader("Sustainability Watchlist")

    low_sust_df = df[df["Sustainability Score"] < 50]

    if not low_sust_df.empty:
        st.warning("Suppliers requiring sustainability review:")

        for _, row in low_sust_df.iterrows():
            st.markdown(f"""
**{row['Supplier Name']}** ({row['Category']})  
- Sustainability Score: {row['Sustainability Score']}  
- Action: {row['Recommendation']}
""")
    else:
        st.success("No major sustainability risks detected")

    # Category Concentration
    st.subheader("Category Concentration")

    high_concentration = hhi_df[hhi_df["HHI"] > 2500]

    if not high_concentration.empty:
        st.error("High concentration in these categories:")

        for _, row in high_concentration.iterrows():
            category = row["Category"]

            st.markdown(f"""
**{category}**  
- HHI: {row['HHI']} ({row['HHI Level']})
""")

            subset = df[df["Category"] == category]

            if not subset.empty:
                top_supplier = subset.sort_values(
                    "Supplier Share %", ascending=False
                ).iloc[0]

                st.markdown(
                    f"- Top supplier: {top_supplier['Supplier Name']} "
                    f"({round(top_supplier['Supplier Share %'], 1)}%)"
                )
    else:
        st.success("No high concentration risks detected")

    # Supplier Overview
    st.subheader("Supplier Overview")
    st.dataframe(df)

    # Spend Visualization
    st.subheader("Spend by Supplier")
    st.bar_chart(df.set_index("Supplier Name")["Annual Spend"])

else:
    st.info("Upload a supplier CSV to begin analysis.")