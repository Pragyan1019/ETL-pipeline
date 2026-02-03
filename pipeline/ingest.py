import pandas as pd;
import os 
csv_paths = "data/";
def load_csv(filename):
    path = os.path.join(csv_paths,filename)
    if not os.path.exists(path):
        raise FileExistsError(f"{filename} doesnot exists")
    else:
     df = pd.read_csv(path)
     df.columns = df.columns.str.lower().str.strip()
     print(len(df))
     return df;


def ingest_data():
    order = load_csv("order.csv");
    product = load_csv("products.csv");
    payments = load_csv("payments.csv")
    users = load_csv("users.csv")
    
    return order, users, product, payments