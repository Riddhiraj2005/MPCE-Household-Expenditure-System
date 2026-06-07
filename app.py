import streamlit as st
import plotly.express as px
from src.data_loader import load_data

st.set_page_config(
    page_title="MPCE Insight360",
    page_icon="📊",
    layout="wide"
)

df = load_data()

st.title("MPCE Insight360")
st.subheader("AI-Powered Household Expenditure Intelligence System")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Households", len(df))

with col2:
    st.metric("Average MPCE", f"₹{df['mpce'].mean():.2f}")

with col3:
    st.metric("Average Household Size", f"{df['household_size'].mean():.2f}")

st.markdown("### Rural vs Urban Average MPCE")

sector_data = df.groupby("sector_rural_urban")["mpce"].mean().reset_index()

fig = px.bar(
    sector_data,
    x="sector_rural_urban",
    y="mpce",
    text_auto=True,
    title="Average MPCE by Sector"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("### Sample Dataset")
st.dataframe(df)