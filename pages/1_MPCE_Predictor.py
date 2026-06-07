import streamlit as st
from src.predict import predict_mpce

st.set_page_config(page_title="MPCE Predictor", page_icon="🧮", layout="wide")

st.title("AI-Based MPCE Predictor")
st.write("Enter household expenditure details to predict Monthly Per Capita Expenditure using a trained ML model.")

sector = st.selectbox("Sector", ["Rural", "Urban"])
state = st.selectbox(
    "State",
    ["Rajasthan", "Maharashtra", "Bihar", "Karnataka", "Uttar Pradesh", "Gujarat", "Tamil Nadu"]
)

household_size = st.number_input("Household Size", min_value=1, max_value=20, value=4)

food = st.number_input("Food Expenditure", min_value=0, value=5000)
education = st.number_input("Education Expenditure", min_value=0, value=1000)
medical = st.number_input("Medical Expenditure", min_value=0, value=1000)
transport = st.number_input("Transport Expenditure", min_value=0, value=1000)
rent = st.number_input("Rent", min_value=0, value=2000)
fuel = st.number_input("Fuel and Light", min_value=0, value=800)
clothing = st.number_input("Clothing", min_value=0, value=500)
durable = st.number_input("Durable Goods", min_value=0, value=1000)

total_expense = food + education + medical + transport + rent + fuel + clothing + durable

input_data = {
    "household_size": household_size,
    "food_expenditure": food,
    "education_expenditure": education,
    "medical_expenditure": medical,
    "transport_expenditure": transport,
    "rent": rent,
    "fuel_light": fuel,
    "clothing": clothing,
    "durable_goods": durable,
    "total_monthly_expenditure": total_expense
}

if st.button("Predict MPCE using ML Model"):
    predicted_mpce = predict_mpce(input_data)
    formula_mpce = total_expense / household_size

    col1, col2 = st.columns(2)

    with col1:
        st.success(f"ML Predicted MPCE: ₹{predicted_mpce:.2f}")

    with col2:
        st.info(f"Formula MPCE: ₹{formula_mpce:.2f}")

    if predicted_mpce < 3000:
        st.warning("Predicted Category: Low Expenditure")
    elif predicted_mpce < 7000:
        st.info("Predicted Category: Middle Expenditure")
    else:
        st.success("Predicted Category: High Expenditure")