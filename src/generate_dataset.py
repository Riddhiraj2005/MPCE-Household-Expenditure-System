import pandas as pd
import numpy as np

np.random.seed(42)

states = [
    "Rajasthan", "Maharashtra", "Bihar", "Karnataka",
    "Uttar Pradesh", "Gujarat", "Tamil Nadu", "Delhi",
    "Kerala", "West Bengal"
]

sectors = ["Rural", "Urban"]

data = []

for i in range(1, 5001):
    state = np.random.choice(states)
    sector = np.random.choice(sectors, p=[0.55, 0.45])

    household_size = np.random.randint(2, 9)

    if sector == "Rural":
        base = np.random.randint(6000, 22000)
        rent = np.random.randint(0, 4000)
    else:
        base = np.random.randint(15000, 60000)
        rent = np.random.randint(3000, 18000)

    food = int(base * np.random.uniform(0.25, 0.45))
    education = int(base * np.random.uniform(0.05, 0.18))
    medical = int(base * np.random.uniform(0.04, 0.15))
    transport = int(base * np.random.uniform(0.05, 0.15))
    fuel = int(base * np.random.uniform(0.04, 0.10))
    clothing = int(base * np.random.uniform(0.02, 0.08))
    durable = int(base * np.random.uniform(0.03, 0.15))

    total = food + education + medical + transport + rent + fuel + clothing + durable
    mpce = round(total / household_size, 2)

    data.append([
        i, state, sector, household_size, food, education,
        medical, transport, rent, fuel, clothing, durable,
        total, mpce
    ])

df = pd.DataFrame(data, columns=[
    "household_id",
    "state",
    "sector_rural_urban",
    "household_size",
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
])

df.to_csv("dataset/cleaned_data.csv", index=False)

print("Dataset generated successfully")
print(df.head())
print("Total records:", len(df))