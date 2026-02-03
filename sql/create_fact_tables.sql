use pipeline1;
-- Fact table
create table fact_orders (
	fact_order_id int auto_increment primary key,
    order_id int,
    user_key int ,
    product_key int ,
    date_key int ,
    
    quantity int,
    unit_price decimal(10,2),
    total_amount decimal(10,2),
    
    foreign key (user_key) references dim_user(user_key),
    foreign key (product_key) references dim_product(product_key),
    foreign key (date_key) references dim_date(date_key)
);


create table fact_payments(
payment_key int auto_increment primary key,
payment_id int ,
order_key int ,
date_key int ,
amount  decimal(10,2),
status varchar(100)

foreign key (order_key) references fact_orders(fact_order_id),
foreign key (date_key) references dim_date(date_key)
);