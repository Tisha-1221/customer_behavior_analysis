--query 1
select gender, sum(purchase_amount) as revenue
from customer_data
group by gender;

-- query 2
select customer_id, purchase_amount
from customer_data
where discount_applied = 'yes' and purchase_amount >= (select avg(purchase_amount) from customer_data);

-- query 3
select item_purchased, ROUND(avg(review_rating), 2) as "Average product Rating"
from customer_data
group by item_purchased
order by avg(review_rating) desc;

--query 4
select shipping_type,
round(avg(purchase_amount),2) as purchaseAmount
from customer_data
where shipping_type in ('Standard', 'Express')
group by shipping_type;

-- query 5
select subscription_status,
COUNT(customer_id) as total_customers,
round(AVG(purchase_amount),2) as average_spend,
ROUND(sum(purchase_amount),2) as total_revenue
from customer_data
group by subscription_status
order by total_revenue, average_spend desc;

--query 6
select item_purchased,
round(100 * sum(case when discount_applied = 'yes' then 1 else 0 end)/count(*),2) as disount_rate
from customer_data
group by item_purchased
order by disount_rate desc;

-- query 7
with customer_type as(
select customer_id, previous_purchases,
CASE
	WHEN previous_purchases = 1 then 'New'
	when previous_purchases between 2 and 10 then 'returning'
	else 'Loyal'
	end as customer_segment
from customer_data
)
select customer_segment, COUNT(*) as 'Number Of Customer'
from customer_type
group by customer_segment;

-- query 8
with item_count as(
select category,
item_purchased,
count(customer_id) as total_orders,
row_number() over (partition by category order by count(customer_id) desc) as item_rank
from customer_data
group by category, item_purchased
)
select item_rank, category, item_purchased, total_orders
from item_count
where item_rank <= 3;

--query 9
select subscription_status, count(customer_id) as repeat_buyers
from customer_data
where previous_purchases > 5
group by subscription_status;

--query 10 what is the revenue contribution for each age group
select age_group,
sum(purchase_amount) as revenue
from customer_data
group by age_group
order by revenue desc;