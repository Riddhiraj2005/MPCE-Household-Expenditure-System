import joblib
import pandas as pd
import streamlit as st

@st.cache_resource
def load_model():
    model = joblib.load("models/mpce_model.pkl")
    return model

def predict_mpce(input_data):
    model = load_model()
    input_df = pd.DataFrame([input_data])
    prediction = model.predict(input_df)[0]
    return prediction