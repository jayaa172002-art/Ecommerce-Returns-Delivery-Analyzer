import pandas as pd
import numpy as np

print("Loading Olist files...")
orders = pd.read_csv("olist_orders_dataset.csv")
items = pd.read_csv("olist_order_items_dataset.csv")
products = pd.read_csv("olist_products_dataset.csv")
customers = pd.read_csv("olist_customers_dataset.csv")

# Merge all
df = orders.merge(items, on='order_id', how='left')
df = df.merge(products[['product_id', 'product_category_name']], on='product_id', how='left')
df = df.merge(customers[['customer_id', 'customer_state', 'customer_city']], on='customer_id', how='left')

# Clean dates
for col in ['order_purchase_timestamp', 'order_estimated_delivery_date', 'order_delivered_customer_date']:
    df[col] = pd.to_datetime(df[col], errors='coerce')

# Create Business metrics
df['delivery_delay_days'] = (df['order_delivered_customer_date'] - df['order_estimated_delivery_date']).dt.days
df['shipping_days'] = (df['order_delivered_customer_date'] - df['order_estimated_delivery_date']).dt.days
df['is_late'] = (df['delivery_delay_days'] >0).astype(int)
df['is_returned'] = (df['order_status'] == 'canceled').astype(int)
df['order_value'] = df['price'] + df['freight_value']

df['product_category_name'] = df['product_category_name'].fillna('Unknown')
df = df.drop_duplicates(subset = ['order_id', 'product_id'])

df['return_reason'] = np.where((df['is_returned']==1) & (df['is_late']==1),'Late Delivery',
                     np.where(df['is_returned']==1, 'product Issue', 'Not Returned'))

final = df[['order_id', 'order_purchase_timestamp', 'order_estimated_delivery_date',
            'is_late', 'is_returned', 'return_reason', 'product_category_name',
            'customer_state', 'customer_city', 'seller_id', 'price', 'order_value']]


final.to_csv("cleaned_ecommerce_orders.csv", index=False)
print(f"DONE! Created cleaned_ecommerce_orders.csv with {len(final)} rows")
print(f"Return Rate: {final['is_returned'].mean()*100:.2f}%")
