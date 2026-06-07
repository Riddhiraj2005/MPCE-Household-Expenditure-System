import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Model Comparison",
    page_icon="🤖",
    layout="wide"
)

st.title("ML Model Comparison")
st.write("Compare different machine learning models used for MPCE prediction.")

results = pd.read_csv("models/model_comparison.csv")

best_model = results.sort_values("R2 Score", ascending=False).iloc[0]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Best Model", best_model["Model"])

with col2:
    st.metric("Best R² Score", best_model["R2 Score"])

with col3:
    st.metric("Lowest MAE", f"₹{results['MAE'].min():.2f}")

st.subheader("Model Performance Table")
st.dataframe(results)

st.subheader("R² Score Comparison")

fig1 = px.bar(
    results,
    x="Model",
    y="R2 Score",
    text_auto=True,
    title="R² Score by Model"
)

st.plotly_chart(fig1, use_container_width=True)

st.subheader("Error Comparison")

fig2 = px.bar(
    results,
    x="Model",
    y=["MAE", "RMSE"],
    barmode="group",
    title="MAE and RMSE Comparison"
)

st.plotly_chart(fig2, use_container_width=True)

st.info(
    "Higher R² score is better. Lower MAE and RMSE values indicate better prediction accuracy."
)