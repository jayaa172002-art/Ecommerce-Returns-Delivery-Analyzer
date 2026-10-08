import pandas as pd
from sqlalchemy import create_engine

PASSWORD = "840991"

engine = create_engine(f'postgresql://postgres:{PASSWORD}@localhost:5432/ecommerce_analyzer')

print("Readng ecommerce file...")
df = pd.read_csv("cleaned_ecommerce_orders.csv")
print(f"Found {len(df)} rows")

df.to_sql('ecom_orders', engine, if_exists='replace', index=False)

print("SUCCESS! ecom_orders table loaded in Postgres")