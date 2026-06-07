import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Explainable AI",
    page_icon="🧠",
    layout="wide"
)

st.title("Explainable AI: Feature Importance")
st.write("Understand which household expenditure factors influence MPCE prediction the most.")

importance_df = pd.read_csv("models/feature_importance.csv")

top_feature = importance_df.iloc[0]

col1, col2 = st.columns(2)

with col1:
    st.metric("Most Important Feature", top_feature["Feature"])

with col2:
    st.metric("Importance Score", f"{top_feature['Importance']:.4f}")

st.subheader("Feature Importance Ranking")

fig = px.bar(
    importance_df,
    x="Importance",
    y="Feature",
    orientation="h",
    text_auto=True,
    title="Feature Importance for MPCE Prediction"
)

fig.update_layout(yaxis={"categoryorder": "total ascending"})

st.plotly_chart(fig, use_container_width=True)

st.subheader("Interpretation")

for _, row in importance_df.iterrows():
    feature_name = row["Feature"].replace("_", " ").title()
    importance = row["Importance"]

    if importance > 0.20:
        st.success(f"{feature_name} has a strong influence on MPCE prediction.")
    elif importance > 0.10:
        st.info(f"{feature_name} has a moderate influence on MPCE prediction.")
    else:
        st.write(f"{feature_name} has a lower influence on MPCE prediction.")

st.subheader("Feature Importance Table")
st.dataframe(importance_df)