use pipeline1;
-- Dimensional table

create table dim_user(
	user_key int auto_increment primary key,
    user_id int ,
    name varchar(100),
    email varchar(100),
    address varchar(100)
    );
create table dim_product(
	product_key int auto_increment primary key,
    product_id int ,
    name varchar(100),
    category varchar(100)
);
create table dim_date(
	date_key int primary key,
    full_date date,
    year int ,
    month int,
    day int 
)	;

