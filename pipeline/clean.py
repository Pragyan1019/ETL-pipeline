import pandas as pd;
import os 
csv_paths = "data/";
def load_csv(filename):
    path = os.path.join(csv_paths,filename)
    if not os.path.exists(path):
        raise FileExistsError(f"{filename} doesnot exists")
    else:
     df = pd.read_csv(path)
     return df;


def ingest_data():
    valid_order = load_csv("valid_order.csv");
    valid_products = load_csv("valid_products.csv");
    valid_payments = load_csv("valid_payments.csv")
    valid_users = load_csv("valid_users.csv")
    
    return valid_order, valid_users, valid_products, valid_payments

def clean_order(valid_order,valid_products):
    valid_order['order_date'] = pd.to_datetime( valid_order['order_date'], errors='coerce')
    valid_order = valid_order.merge(
   valid_products[['product_id','price']],
   on="product_id",
   how="left"
    )
    valid_order["total_amount"]= (valid_order["quantity"]*valid_order["price"]).round(2);
    orders_clean =valid_order.drop_duplicates("order_id") 
    return orders_clean;

def clean_user(valid_users):
    valid_users['age']=valid_users['age'].astype(int);
    valid_users['name']=valid_users['name'].str.strip().str.title();
    valid_users["email"]=valid_users['email'].str.lower();
    valid_users["address"]=valid_users["address"].fillna("Unknown")
    users_clean =valid_users.drop_duplicates("user_id") 
    return users_clean;

def clean_product(valid_products):
    valid_products['stock']= valid_products['stock'].astype(int);
    valid_products["category"] = valid_products["category"].str.strip().str.title()
    products_clean =valid_products.drop_duplicates("product_id") 
    return products_clean;

def clean_payment(valid_payments):
    valid_payments['payment_date']= pd.to_datetime(valid_payments['payment_date'],errors="coerce");
    payments_clean = valid_payments.drop_duplicates("payment_id")
    return payments_clean;


def clean_all():
    valid_order, valid_users, valid_products, valid_payments = ingest_data()
    orders_clean=clean_order(valid_order,valid_products)
    users_clean=clean_user(valid_users)
    products_clean = clean_product(valid_products)
    payments_clean = clean_payment(valid_payments)
    orders_clean.to_csv("data/clean/orders_clean.csv", index=False)
    users_clean.to_csv("data/clean/users_clean.csv", index=False)
    products_clean.to_csv("data/clean/products_clean.csv", index=False)
    payments_clean.to_csv("data/clean/payments_clean.csv", index=False)