import streamlit as st
import plotly.express as px
from src.data_loader import load_data

st.set_page_config(
    page_title="Rural vs Urban Dashboard",
    page_icon="🏘️",
    layout="wide"
)

st.title("Rural vs Urban MPCE Dashboard")

df = load_data()

sector_summary = df.groupby("sector_rural_urban").agg(
    avg_mpce=("mpce", "mean"),
    avg_total_expense=("total_monthly_expenditure", "mean"),
    avg_household_size=("household_size", "mean"),
    household_count=("household_id", "count")
).reset_index()

col1, col2 = st.columns(2)

with col1:
    rural_mpce = sector_summary[sector_summary["sector_rural_urban"] == "Rural"]["avg_mpce"].values[0]
    st.metric("Average Rural MPCE", f"₹{rural_mpce:.2f}")

with col2:
    urban_mpce = sector_summary[sector_summary["sector_rural_urban"] == "Urban"]["avg_mpce"].values[0]
    st.metric("Average Urban MPCE", f"₹{urban_mpce:.2f}")

fig1 = px.bar(
    sector_summary,
    x="sector_rural_urban",
    y="avg_mpce",
    text_auto=True,
    title="Average MPCE: Rural vs Urban"
)

st.plotly_chart(fig1, use_container_width=True)

fig2 = px.bar(
    sector_summary,
    x="sector_rural_urban",
    y="avg_total_expense",
    text_auto=True,
    title="Average Total Monthly Expenditure: Rural vs Urban"
)

st.plotly_chart(fig2, use_container_width=True)

st.subheader("Sector Summary Table")
st.dataframe(sector_summary)