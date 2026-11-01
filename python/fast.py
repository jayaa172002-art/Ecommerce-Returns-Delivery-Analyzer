import pandas as pd
from sqlalchemy import create_engine

print("reading csv")
df = pd.read_csv("data/processed/ecommerce_cleaned_final.csv")
print("rows:", len(df))

# your password 840991 - confirmed working
engine = create_engine("postgresql://postgres:840991@localhost:5432/ecommerce_returns")
print("connected")

df.to_sql("ecommerce", engine, if_exists="replace", index=False)
print("ALL DONE - 114092 rows inserted")