# ECommerce Returns & Late Delivery Analyzer

Analyzing why e-commerce orders get returned or delivered late & where we are losing money.

**Dashboard Preview:** 
Total Orders: 114092 | Total Revenue: 1,36,51,923.47 | Late %: 6.39% | Return %: 1.16% | Revenue Lost: 97,728.16 | Avg Delay: -11.69 days

### Business Problem

E-commerce loses money in two places - late delivery and returns. I wanted to find:
1. Are late orders more likely to be returned?
2. Which categories are returned most?
3. Which regions and carriers are always late?

### Data I Used

I used Brazilian Olist dataset (7 files) - similar to Indian e-commerce.

**Raw files from my laptop:**
- olist_orders_dataset.csv
- olist_order_items_dataset.csv
- olist_customers_dataset.csv
- olist_products_dataset.csv
- olist_order_reviews_dataset.csv

**Final file I created:** `ecommerce_cleaned_final.csv` - 114092 rows

**Columns I created as per brief:**
`order_id, order_date, promised_date, delivery_date, delivery_delay_days, is_late, product_category, price, order_value, region, carrier, return_flag, return_reason`

### How I Cleaned - My Code `clean_olist.py`


1. **Merging:** orders + customers on customer_id (to get customer_state as region), + items on order_id (price), + products on product_id (product_category_name), + reviews on order_id (review_score)
2. **Dates:** Converted order_purchase_timestamp to order_date, order_estimated_delivery_date to promised_date, order_delivered_customer_date to delivery_date
3. **Delivery Delay:** delivery_delay_days = delivery_date - promised_date, fillna(0). is_late = 1 if delay > 0 else 0
4. **Return Flag:** In Olist, order_status = 'canceled' or 'unavailable' means returned. So return_flag = 1 for those.
5. **Region:** region = customer_state
6. **Carrier:** Original data has no carrier, so I did `np.random.seed(10)` and assigned random - ['Bluedart', 'Delhivery', 'Ecom Express', 'DTDC'] - This is my assumption, mentioned in code comment.
7. **Product Category:** product_category = product_category_name.fillna('others')
8. **Order Value:** order_value = price
9. **Return Reason:** Logic from my code:
   - if return_flag == 0 -> ''
   - else if is_late == 1 -> 'Late Delivery'
   - elif review_score <=2 -> 'Quality Not Expected'
   - else -> 'Size Issue or Other'
10. **Save:** Saved only needed columns as `ecommerce_cleaned_final.csv` and printed total rows, return rate %, late rate %

### Dashboard - What My Screenshot Shows

**Top 6 KPIs:**
- Total Orders 114092
- Total Revenue 1,36,51,923.47
- Late Delivery Rate % 6.39%
- Return Rate 1.16%
- Revenue Lost 97,728.16
- Avg Delivery Delays -11.69 (negative means we deliver early on average)

**6 Visuals:**

1. **Carrier Late %:** Ecom Express 0.07 (7%), Bluedart 0.07 (7%), Delhivery 0.06 (6%), DTDC 0.06 (6%) - Almost same because random, but Ecom slightly higher.
2. **Late Delivery vs Return Rate:** 0 = 0.012 (~1.2%) return, 1 = 0.0001 (~0.01%) return. So in my data late orders look LESS likely to return.
3. **Return by Category:** others 784, esporte_lazer 51, utilidades_domesticas 49, informatica_acessorios 48 - others is highest.
4. **Region Performance Late %:** AL 0.20 (20%), MA 0.17 (17%), SE 0.16 (16%), CE 0.13, PI 0.13 - AL, MA, SE worst.
5. **Return Reason by Product Category:** others has mix of Late Delivery, Quality Not Expected, Size Issue. Shows late is main reason.
6. **Trend over Time Late Delivery % (Jan 2017-Jul 2018):** Early Jan 2017 spike to 0.40 (40%), then stable low 0.00-0.05, then spike again Jan 2018 to 0.18 (18%) - festival season.

# My Findings
**1. Are late orders more likely to be returned?**
'others' category - 784 returns. This is not real category, it's blank product names I filled as 'others'. So 59% returns are from missing data.
Reason is data definition - when order is canceled, it has no delivery_data, so my code is_late = 0. So cancelled orders can never be marked late.
In real business, late does cause return but in this dataset we can't prove. I learnt this.

**2. Which categories are returned most?**
'others' category - 784 returns. This is not real category, it's blank product names I filled as 'others'. So 59% returns are from missing data.
Real categories - esporte_lazer 51, utilidades_domesticas 49, informatica_accessorios 48.

**3. Which regions and carriers are always late?**
Region - AL 20%, MA 17%, SE 16%. All are far North-East states from Sao Paulo hub. Average is 6.39%, these are 3 times more.
Carrier - Ecom Express 7%, Bluedart 7% vs Delhivery 6%, DTDC 6%. 
Trend - Late was 40% in Jan 2017 and 18% in Jan 2018. Both are sale season.

## My Recommendations
**1. Fix 'others' Category Mapping**
Metric: Return by Category - others 784 // Return Rate 1.16%
Pattern: 59% returns are from blank category.
Action: Clean product_category master table first.

**2. Fix AL, MA, SE Regions**
 Metric: Region late % AL 20% MA 17% SE 16% vs Avg 6.39%
 Pattern: Remote North-East states far from Sao Paulo warehouse
 Action: Increase promise_date by +2 days for these states or tie up with local partner like DTDC for last-mile. 
         If we bring these 3 from- 18% to 8% late, overall late drop from 6.39% to ~5%.

 **3. Audit Ecom Express & Bluedart**
 Metric: Carrier Late % 7% vs 6%
 Pattern: 1% gap = 1140 orders at risk
 Action: For AL/MA/SE regions, stop using Ecom Express, route via Delhivery/DTDC for 1 month as test.

**4. Don't use Average Delay Alone**
Metric: Avg Delay - 11.69 days but still Late% 6.39%
Pattern: Average shows we deliver 11 days early, but 6.39% still late
Action: Track median + 95th percentile delay, not just average. Sent daily alert if any region late% > 10%. Average hides the real problem.

**5. Reduce Revenue Lost 97,728 and Capture Real Return Reason**
Metric: Revenue Lost 97,728.16
Pattern: Return Reason chart shows most returns guessesd as Late Delivery / Quality Not Expected
Action: Currently i guessed return reason from is_late and review_score. Start capturing reason at return time - Late, Damaged, Size Issue, Not as Described.
Then we can fix chart for esporte_lazer and quality check for utilidaded=s_dometicas. If we cut late from 6.39% to 3%, we can save ~48000 revenue.
 




