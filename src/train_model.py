import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

df = pd.read_csv("dataset/cleaned_data.csv")

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

target = "mpce"

X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

models = {
    "Linear Regression": LinearRegression(),
    "Decision Tree": DecisionTreeRegressor(random_state=42),
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
    "Gradient Boosting": GradientBoostingRegressor(random_state=42)
}

results = []

best_model = None
best_r2 = -999
best_model_name = ""

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    results.append({
        "Model": name,
        "MAE": round(mae, 2),
        "RMSE": round(rmse, 2),
        "R2 Score": round(r2, 4)
    })

    if r2 > best_r2:
        best_r2 = r2
        best_model = model
        best_model_name = name

results_df = pd.DataFrame(results)

results_df.to_csv("models/model_comparison.csv", index=False)
joblib.dump(best_model, "models/mpce_model.pkl")

print("Model training completed")
print(results_df)
print(f"Best Model: {best_model_name}")
print("Best model saved as models/mpce_model.pkl")
print("Model comparison saved as models/model_comparison.csv")
# Save feature importance if model supports it
if hasattr(best_model, "feature_importances_"):
    importance_df = pd.DataFrame({
        "Feature": features,
        "Importance": best_model.feature_importances_
    }).sort_values(by="Importance", ascending=False)

    importance_df.to_csv("models/feature_importance.csv", index=False)
    print("Feature importance saved as models/feature_importance.csv")