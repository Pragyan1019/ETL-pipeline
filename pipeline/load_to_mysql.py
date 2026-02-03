import pandas as pd;
from db_connection import get_connection;
def connection():
    conn = get_connection()
    if conn.is_connected():
        print("Connected to mysql")

    return conn.cursor(),conn;     

def read_dataframes():
    user = pd.read_csv("data/clean/users_clean.csv");
    order = pd.read_csv("data/clean/orders_clean.csv");
    product = pd.read_csv("data/clean/products_clean.csv");
    payment = pd.read_csv("data/clean/payments_clean.csv");
    order["order_date"]=pd.to_datetime(order["order_date"])
    payment["payment_date"]= pd.to_datetime(payment["payment_date"])
    return user,order,product,payment;

def insertion_queries():
    sql_users = """
    insert into users(user_id,name,email,age,address)
    values(%s,%s,%s,%s,%s)
    """
    sql_orders = """
    insert into orders(order_id,user_id,product_id,quantity,order_date,total_amount,price)
    values(%s,%s,%s,%s,%s,%s,%s)
    """
    sql_products = """
    insert into products(product_id,name,category,price,stock)
    values(%s,%s,%s,%s,%s)
    """
    sql_payments ="""
    insert into payments(payment_id,order_id,amount,payment_date,status)
    values(%s,%s,%s,%s,%s)
    """
    return sql_users,sql_orders,sql_products,sql_payments;

def insert_fact_table():
    dim_user = """insert into dim_user(user_id,name,email,address) 
    select distinct user_id,name,email,address from users"""

    dim_product= """insert into dim_product(product_id,name,category)
    select distinct product_id,name,category from products"""

    dim_date = """insert into dim_date(date_key,full_date,year,month,day)
    select distinct date_format(order_date,'%Y%m%d') as date_key,order_date,year(order_date),
    month(order_date),day(order_date) from orders"""

    fact_orders = """insert into 
    fact_orders(order_id,user_key,product_key,date_key,quantity,unit_price,total_amount)
    select o.order_id,du.user_key,dp.product_key,dd.date_key,o.quantity,o.price,o.total_amount
    from orders o 
    join dim_user du
    on o.user_id = du.user_id
    join dim_product dp
    on o.product_id  =dp.product_id 
    join dim_date dd
    on o.order_date = dd.full_date;
    """
    return dim_user,dim_product,dim_date,fact_orders


def load_file():
    try:
        sql_users,sql_orders,sql_products,sql_payments=insertion_queries();
        dim_user , dim_product, dim_date,fact_orders = insert_fact_table();
        user,order,product,payment=read_dataframes();
        cursor,conn = connection();
        cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
        for table in ["users","products","orders","payments"]:
            cursor.execute(f"TRUNCATE TABLE {table};")
        cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
        cursor.executemany(sql_users, user.values.tolist())
        cursor.executemany(sql_products, product.values.tolist())
        cursor.executemany(sql_orders, order.values.tolist())
        cursor.executemany(sql_payments, payment.values.tolist())
        cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
        for table in ["dim_user","dim_product","dim_date","fact_orders"]:
            cursor.execute(f"TRUNCATE TABLE {table}")
        cursor.execute(dim_user);
        cursor.execute(dim_product);
        cursor.execute(dim_date);  
        cursor.execute(fact_orders)
        cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
        conn.commit()    
        cursor.close()
        conn.close();
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error: {e}")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:    
            conn.close();