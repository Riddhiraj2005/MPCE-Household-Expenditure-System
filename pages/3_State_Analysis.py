import streamlit as st
import plotly.express as px
from src.data_loader import load_data

st.set_page_config(
    page_title="State Analysis",
    page_icon="🗺️",
    layout="wide"
)

st.title("State-wise MPCE Analysis")

df = load_data()

selected_state = st.selectbox(
    "Select State",
    sorted(df["state"].unique())
)

state_df = df[df["state"] == selected_state]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Average MPCE", f"₹{state_df['mpce'].mean():.2f}")

with col2:
    st.metric("Average Household Size", f"{state_df['household_size'].mean():.2f}")

with col3:
    st.metric("Total Households", len(state_df))

fig = px.histogram(
    state_df,
    x="mpce",
    nbins=20,
    title=f"MPCE Distribution in {selected_state}"
)

st.plotly_chart(fig, use_container_width=True)

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

expense_data = state_df[expense_cols].mean().reset_index()
expense_data.columns = ["Expense Category", "Average Amount"]

fig2 = px.bar(
    expense_data,
    x="Expense Category",
    y="Average Amount",
    title=f"Average Expense Category Distribution in {selected_state}",
    text_auto=True
)

st.plotly_chart(fig2, use_container_width=True)

st.subheader("State Household Records")
st.dataframe(state_df)