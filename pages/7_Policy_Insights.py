import streamlit as st
from src.data_loader import load_data

st.set_page_config(
    page_title="Policy Insights",
    page_icon="📌",
    layout="wide"
)

st.title("Policy Insight Generator")
st.write("Automatically generate simple insights from household expenditure data.")

df = load_data()

avg_mpce = df["mpce"].mean()
avg_total = df["total_monthly_expenditure"].mean()

avg_rural = df[df["sector_rural_urban"] == "Rural"]["mpce"].mean()
avg_urban = df[df["sector_rural_urban"] == "Urban"]["mpce"].mean()

highest_state = df.groupby("state")["mpce"].mean().idxmax()
lowest_state = df.groupby("state")["mpce"].mean().idxmin()

highest_category = df[
    [
        "food_expenditure",
        "education_expenditure",
        "medical_expenditure",
        "transport_expenditure",
        "rent",
        "fuel_light",
        "clothing",
        "durable_goods"
    ]
].mean().idxmax()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Average MPCE", f"₹{avg_mpce:.2f}")

with col2:
    st.metric("Average Rural MPCE", f"₹{avg_rural:.2f}")

with col3:
    st.metric("Average Urban MPCE", f"₹{avg_urban:.2f}")

st.subheader("Generated Policy Insights")

st.success(
    f"Urban households have higher average MPCE of ₹{avg_urban:.2f} "
    f"compared to rural households with ₹{avg_rural:.2f}."
)

st.info(
    f"{highest_state} shows the highest average MPCE among available states, "
    f"while {lowest_state} shows the lowest average MPCE."
)

st.warning(
    f"The highest average spending category is {highest_category.replace('_', ' ').title()}, "
    f"indicating it is a major component of household consumption."
)

st.subheader("Detailed Insight Report")

report = f"""
### Household Expenditure Insight Report

The dataset contains **{len(df)} household records**.

The overall average Monthly Per Capita Expenditure is **₹{avg_mpce:.2f}**.

The average total monthly household expenditure is **₹{avg_total:.2f}**.

Rural households have an average MPCE of **₹{avg_rural:.2f}**, while urban households have an average MPCE of **₹{avg_urban:.2f}**.

The highest MPCE state in the dataset is **{highest_state}**.

The lowest MPCE state in the dataset is **{lowest_state}**.

The category with the highest average expenditure is **{highest_category.replace('_', ' ').title()}**.

This analysis can help identify rural-urban consumption gaps, household expenditure pressure, and state-wise spending variation.
"""

st.markdown(report)

st.download_button(
    label="Download Insight Report",
    data=report,
    file_name="mpce_policy_insight_report.md",
    mime="text/markdown"
)