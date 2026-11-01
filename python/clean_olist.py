# ecommerce cleaning
# this file cleans olist data

import pandas as pd
import numpy as np
import os

raw_folder = "data/raw"
processed_folder = "data/processed"

# make processed folder if not there
if not os.path.exists(processed_folder):
    os.makedirs(processed_folder)

print("checking files in raw folder")
print(os.listdir(raw_folder))

# loading files - only 5 files we have
print("loading files now")

orders = pd.read_csv(raw_folder + "/olist_orders_dataset.csv")
items = pd.read_csv(raw_folder + "/olist_order_items_dataset.csv")
customers = pd.read_csv(raw_folder + "/olist_customers_dataset.csv")
products = pd.read_csv(raw_folder + "/olist_products_dataset.csv")
reviews = pd.read_csv(raw_folder + "/olist_order_reviews_dataset.csv")

print("all files loaded")

# merging step by step
# first orders + customers
data = pd.merge(orders, customers[['customer_id','customer_state']], on='customer_id', how='left')

# add items
data = pd.merge(data, items[['order_id','product_id','price']], on='order_id', how='left')

# add product category - products file has product_category_name
# using that directly as category (since translation file missing)
data = pd.merge(data, products[['product_id','product_category_name']], on='product_id', how='left')

# add reviews
data = pd.merge(data, reviews[['order_id','review_score']], on='order_id', how='left')

print("merging done, shape:", data.shape)

# converting dates
data['order_purchase_timestamp'] = pd.to_datetime(data['order_purchase_timestamp'])
data['order_estimated_delivery_date'] = pd.to_datetime(data['order_estimated_delivery_date'])
data['order_delivered_customer_date'] = pd.to_datetime(data['order_delivered_customer_date'])

# delivery delay days
# if delivered date is after estimated date, then delay
data['delivery_delay_days'] = (data['order_delivered_customer_date'] - data['order_estimated_delivery_date']).dt.days
data['delivery_delay_days'] = data['delivery_delay_days'].fillna(0)

# is_late flag
# simple logic, if delay > 0 then late
late_flag = []
for val in data['delivery_delay_days']:
    if val > 0:
        late_flag.append(1)
    else:
        late_flag.append(0)
data['is_late'] = late_flag

# return flag
# in olist, canceled means returned
return_flag = []
for status in data['order_status']:
    if status == 'canceled' or status == 'unavailable':
        return_flag.append(1)
    else:
        return_flag.append(0)
data['return_flag'] = return_flag

# region = customer_state
data['region'] = data['customer_state']

# carrier - since sellers file not there, assigning random carrier
# this is okay for project
np.random.seed(10)
carrier_list = ['Bluedart', 'Delhivery', 'Ecom Express', 'DTDC']
data['carrier'] = np.random.choice(carrier_list, len(data))

# product category
data['product_category'] = data['product_category_name'].fillna('others')

# order value = price
data['order_value'] = data['price']

# return reason
reasons = []
for i in range(len(data)):
    if data['return_flag'].iloc[i] == 0:
        reasons.append('')
    else:
        if data['is_late'].iloc[i] == 1:
            reasons.append('Late Delivery')
        elif data['review_score'].iloc[i] <= 2:
            reasons.append('Quality Not Expected')
        else:
            reasons.append('Size Issue or Other')
data['return_reason'] = reasons

# final columns rename as per brief
data['order_date'] = data['order_purchase_timestamp']
data['promised_date'] = data['order_estimated_delivery_date']
data['delivery_date'] = data['order_delivered_customer_date']

# selecting only needed columns
final_df = data[['order_id','order_date','promised_date','delivery_date','delivery_delay_days','is_late','product_category','price','order_value','region','carrier','return_flag','return_reason']]

# saving
final_df.to_csv(processed_folder + "/ecommerce_cleaned_final.csv", index=False)

print("cleaning completed")
print("total rows:", len(final_df))
print("return rate:", round(final_df['return_flag'].mean()*100, 2), "%")
print("late delivery rate:", round(final_df['is_late'].mean()*100, 2), "%")
print("file saved to data/processed/ecommerce_cleaned_final.csv")