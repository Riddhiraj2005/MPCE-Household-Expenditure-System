import streamlit as st
import pandas as pd
import joblib
import shap
import plotly.express as px

from src.data_loader import load_data

st.set_page_config(
    page_title="SHAP Explainability",
    page_icon="🔍",
    layout="wide"
)

st.title("SHAP Explainability for MPCE Prediction")
st.write("Explain individual MPCE predictions using SHAP values.")

df = load_data()

features = [
    "household_size",
    "food_expenditure",
    "education_expenditure",
    "medical_expenditure",
    "transport_expenditure",
    "rent",
    "fuel_light",
    "clothing",
    "durable_goods",
    "total_monthly_expenditure"
]

model = joblib.load("models/mpce_model.pkl")

st.subheader("Select Household Record")

selected_id = st.selectbox(
    "Choose Household ID",
    df["household_id"].unique()
)

selected_row = df[df["household_id"] == selected_id]

X = df[features]
selected_X = selected_row[features]

prediction = model.predict(selected_X)[0]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Household ID", selected_id)

with col2:
    st.metric("Predicted MPCE", f"₹{prediction:.2f}")

with col3:
    st.metric("Actual MPCE", f"₹{selected_row['mpce'].values[0]:.2f}")

st.subheader("Selected Household Details")
st.dataframe(selected_row)

st.subheader("SHAP Feature Contribution")

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(selected_X)

shap_df = pd.DataFrame({
    "Feature": features,
    "SHAP Value": shap_values[0]
})

shap_df["Impact"] = shap_df["SHAP Value"].apply(
    lambda x: "Increases MPCE" if x > 0 else "Decreases MPCE"
)

shap_df["Absolute Impact"] = shap_df["SHAP Value"].abs()

shap_df = shap_df.sort_values(
    by="Absolute Impact",
    ascending=False
)

fig = px.bar(
    shap_df,
    x="SHAP Value",
    y="Feature",
    color="Impact",
    orientation="h",
    title="Feature Contribution for Selected Household",
    text_auto=True
)

fig.update_layout(yaxis={"categoryorder": "total ascending"})

st.plotly_chart(fig, use_container_width=True)

st.subheader("Explanation")

for _, row in shap_df.iterrows():
    feature = row["Feature"].replace("_", " ").title()
    value = row["SHAP Value"]

    if value > 0:
        st.success(f"{feature} increased the predicted MPCE by approximately ₹{value:.2f}.")
    else:
        st.warning(f"{feature} decreased the predicted MPCE by approximately ₹{abs(value):.2f}.")

st.subheader("SHAP Values Table")
st.dataframe(shap_df)