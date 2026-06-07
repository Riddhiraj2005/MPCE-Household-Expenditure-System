import streamlit as st
import plotly.express as px
from src.data_loader import load_data

st.set_page_config(
    page_title="Household Segmentation",
    page_icon="👨‍👩‍👧‍👦",
    layout="wide"
)

st.title("Household Segmentation")
st.write("Classify households into Low, Middle, and High expenditure groups.")

df = load_data()

def classify_group(mpce):
    if mpce < 3000:
        return "Low Expenditure"
    elif mpce < 7000:
        return "Middle Expenditure"
    else:
        return "High Expenditure"

df["expenditure_group"] = df["mpce"].apply(classify_group)

group_summary = df["expenditure_group"].value_counts().reset_index()
group_summary.columns = ["Expenditure Group", "Household Count"]

col1, col2, col3 = st.columns(3)

with col1:
    low_count = len(df[df["expenditure_group"] == "Low Expenditure"])
    st.metric("Low Expenditure", low_count)

with col2:
    middle_count = len(df[df["expenditure_group"] == "Middle Expenditure"])
    st.metric("Middle Expenditure", middle_count)

with col3:
    high_count = len(df[df["expenditure_group"] == "High Expenditure"])
    st.metric("High Expenditure", high_count)

st.subheader("Household Group Distribution")

fig1 = px.bar(
    group_summary,
    x="Expenditure Group",
    y="Household Count",
    text_auto=True,
    title="Households by Expenditure Group"
)

st.plotly_chart(fig1, use_container_width=True)

st.subheader("MPCE vs Household Size")

fig2 = px.scatter(
    df,
    x="household_size",
    y="mpce",
    color="expenditure_group",
    size="total_monthly_expenditure",
    hover_data=["state", "sector_rural_urban"],
    title="Household Size vs MPCE"
)

st.plotly_chart(fig2, use_container_width=True)

st.subheader("Sector-wise Segmentation")

sector_group = df.groupby(
    ["sector_rural_urban", "expenditure_group"]
).size().reset_index(name="count")

fig3 = px.bar(
    sector_group,
    x="sector_rural_urban",
    y="count",
    color="expenditure_group",
    barmode="group",
    text_auto=True,
    title="Rural vs Urban Household Segments"
)

st.plotly_chart(fig3, use_container_width=True)

st.subheader("Segmented Household Data")

st.dataframe(
    df[
        [
            "household_id",
            "state",
            "sector_rural_urban",
            "household_size",
            "total_monthly_expenditure",
            "mpce",
            "expenditure_group"
        ]
    ]
)