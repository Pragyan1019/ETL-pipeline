use pipeline1;
-- insert data into fact table
insert into 
fact_orders(order_id,user_key,product_key,date_key,quantity,unit_price,total_amount)
select o.order_id,du.user_key,dp.product_key,dd.date_key,o.quantity,o.price,o.total_amount
from orders o 
join dim_user du
on o.user_id = du.user_id
join dim_product dp
on o.product_id  =dp.product_id 
join dim_date dd
on o.order_date = dd.full_date;
