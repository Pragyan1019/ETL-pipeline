use pipeline1;

insert into dim_user(user_id,name,email,address) 
select distinct user_id,name,email,address from users;

insert into dim_product(product_id,name,category)
select distinct product_id,name,category from products;

insert into dim_date(date_key,full_date,year,month,day)
select distinct date_format(order_date,'%y%m%d') as date_key,order_date,year(order_date),
month(order_date),day(order_date) from orders
