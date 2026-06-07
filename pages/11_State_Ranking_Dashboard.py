import streamlit as st
import plotly.express as px
from src.data_loader import load_data

st.set_page_config(
    page_title="State Ranking Dashboard",
    page_icon="🗺️",
    layout="wide"
)

st.title("State-wise MPCE Ranking Dashboard")
st.write("Compare average Monthly Per Capita Expenditure across states.")

df = load_data()

state_mpce = (
    df.groupby("state")
    .agg(
        avg_mpce=("mpce", "mean"),
        avg_total_expense=("total_monthly_expenditure", "mean"),
        avg_household_size=("household_size", "mean"),
        household_count=("household_id", "count")
    )
    .reset_index()
    .sort_values(by="avg_mpce", ascending=False)
)

highest_state = state_mpce.iloc[0]
lowest_state = state_mpce.iloc[-1]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Highest MPCE State", highest_state["state"])

with col2:
    st.metric("Highest Avg MPCE", f"₹{highest_state['avg_mpce']:.2f}")

with col3:
    st.metric("Lowest MPCE State", lowest_state["state"])

st.subheader("State Ranking by Average MPCE")

fig = px.bar(
    state_mpce,
    x="avg_mpce",
    y="state",
    orientation="h",
    text_auto=True,
    title="Average MPCE by State"
)

fig.update_layout(yaxis={"categoryorder": "total ascending"})

st.plotly_chart(fig, use_container_width=True)

st.subheader("State-wise Summary Table")

st.dataframe(state_mpce)

st.subheader("Automatic Interpretation")

st.success(
    f"{highest_state['state']} has the highest average MPCE of ₹{highest_state['avg_mpce']:.2f}."
)

st.warning(
    f"{lowest_state['state']} has the lowest average MPCE of ₹{lowest_state['avg_mpce']:.2f}."
)

gap = highest_state["avg_mpce"] - lowest_state["avg_mpce"]

st.info(
    f"The MPCE gap between the highest and lowest state is ₹{gap:.2f}, "
    "showing regional expenditure variation."
)