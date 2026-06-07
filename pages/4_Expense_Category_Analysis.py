import streamlit as st
import plotly.express as px
from src.data_loader import load_data

st.set_page_config(
    page_title="Expense Category Analysis",
    page_icon="💰",
    layout="wide"
)

st.title("Expense Category Analysis")
st.write("Analyze household spending across different expenditure categories.")

df = load_data()

expense_cols = [
    "food_expenditure",
    "education_expenditure",
    "medical_expenditure",
    "transport_expenditure",
    "rent",
    "fuel_light",
    "clothing",
    "durable_goods"
]

category_data = df[expense_cols].mean().reset_index()
category_data.columns = ["Expense Category", "Average Amount"]

col1, col2 = st.columns(2)

with col1:
    highest_category = category_data.loc[category_data["Average Amount"].idxmax()]
    st.metric(
        "Highest Avg Expense",
        highest_category["Expense Category"],
        f"₹{highest_category['Average Amount']:.2f}"
    )

with col2:
    lowest_category = category_data.loc[category_data["Average Amount"].idxmin()]
    st.metric(
        "Lowest Avg Expense",
        lowest_category["Expense Category"],
        f"₹{lowest_category['Average Amount']:.2f}"
    )

st.subheader("Average Spending by Category")

fig1 = px.bar(
    category_data,
    x="Expense Category",
    y="Average Amount",
    text_auto=True,
    title="Average Household Spending Across Categories"
)

st.plotly_chart(fig1, use_container_width=True)

st.subheader("Expense Share Distribution")

fig2 = px.pie(
    category_data,
    names="Expense Category",
    values="Average Amount",
    title="Average Expense Category Share"
)

st.plotly_chart(fig2, use_container_width=True)

st.subheader("Sector-wise Category Comparison")

sector_category = df.groupby("sector_rural_urban")[expense_cols].mean().reset_index()

sector_melted = sector_category.melt(
    id_vars="sector_rural_urban",
    value_vars=expense_cols,
    var_name="Expense Category",
    value_name="Average Amount"
)

fig3 = px.bar(
    sector_melted,
    x="Expense Category",
    y="Average Amount",
    color="sector_rural_urban",
    barmode="group",
    title="Rural vs Urban Category-wise Expenditure",
    text_auto=True
)

st.plotly_chart(fig3, use_container_width=True)

st.subheader("Category Data Table")
st.dataframe(category_data)