import streamlit as st
import plotly.express as px
from sklearn.ensemble import IsolationForest
from src.data_loader import load_data

st.set_page_config(
    page_title="Anomaly Detection",
    page_icon="🚨",
    layout="wide"
)

st.title("Anomaly Detection in Household Spending")
st.write("Detect unusual household expenditure patterns using Isolation Forest.")

df = load_data()

features = [
    "food_expenditure",
    "education_expenditure",
    "medical_expenditure",
    "transport_expenditure",
    "rent",
    "fuel_light",
    "clothing",
    "durable_goods",
    "total_monthly_expenditure",
    "mpce"
]

contamination = st.slider(
    "Select anomaly sensitivity",
    min_value=0.01,
    max_value=0.30,
    value=0.10,
    step=0.01
)

model = IsolationForest(
    contamination=contamination,
    random_state=42
)

df["anomaly"] = model.fit_predict(df[features])

df["anomaly_status"] = df["anomaly"].map({
    1: "Normal",
    -1: "Anomaly"
})

total_records = len(df)
anomaly_count = len(df[df["anomaly_status"] == "Anomaly"])
normal_count = len(df[df["anomaly_status"] == "Normal"])

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Households", total_records)

with col2:
    st.metric("Normal Households", normal_count)

with col3:
    st.metric("Detected Anomalies", anomaly_count)

st.subheader("Anomaly Distribution")

status_count = df["anomaly_status"].value_counts().reset_index()
status_count.columns = ["Status", "Count"]

fig1 = px.bar(
    status_count,
    x="Status",
    y="Count",
    text_auto=True,
    title="Normal vs Anomalous Households"
)

st.plotly_chart(fig1, use_container_width=True)

st.subheader("MPCE vs Total Monthly Expenditure")

fig2 = px.scatter(
    df,
    x="total_monthly_expenditure",
    y="mpce",
    color="anomaly_status",
    size="household_size",
    hover_data=["household_id", "state", "sector_rural_urban"],
    title="Anomaly Detection: MPCE vs Total Monthly Expenditure"
)

st.plotly_chart(fig2, use_container_width=True)

st.subheader("Detected Anomalous Households")

anomaly_df = df[df["anomaly_status"] == "Anomaly"]

if anomaly_df.empty:
    st.success("No anomalies detected at the selected sensitivity.")
else:
    st.dataframe(
        anomaly_df[
            [
                "household_id",
                "state",
                "sector_rural_urban",
                "household_size",
                "total_monthly_expenditure",
                "mpce",
                "anomaly_status"
            ]
        ]
    )

st.subheader("Full Household Data with Anomaly Status")

st.dataframe(
    df[
        [
            "household_id",
            "state",
            "sector_rural_urban",
            "household_size",
            "total_monthly_expenditure",
            "mpce",
            "anomaly_status"
        ]
    ]
)