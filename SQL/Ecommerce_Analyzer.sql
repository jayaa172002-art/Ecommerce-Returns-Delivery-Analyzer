--Project: Ecommerce-Returns & Late Delivery Analysis  
--DB: ecommerce_analyzer|Table: ecom_orders (99,441 orders)

--1. Check Total Rows
SELECT COUNT(*) FROM ecom_orders;
   

--2. Late Delivery Rate by State (Late vs On-Time)
SELECT
     CASE WHEN is_late=1 THEN 'Late' ELSE 'ON-Time' END as status
	 ROUND(AVG(is_returned)*100,2) as return_rate
FROM ecom_orders 
GROUP BY is_late;


--3. Top 5 Return Rate by Category
SELECT product_category_name, Round(AVG(is_returned)*100,2) AS return_rate
FROM ecom_orders 
GROUP BY 1
ORDER BY 2 DESC 
LIMIT 5;

--4. Top 5 Late Delivery Rate by state
SELECT customer_state, Round(AVG(is_late)*100,2) AS late_rate
FROM ecom_orders 
GROUP BY 1
ORDER BY 2 DESC
LIMIT 5;




    
    