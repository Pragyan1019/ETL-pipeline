import pandas as pd
import re

EMAIL_PATTERN = r'^[A-Za-z0-9.+/_&-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'


def validate_users(users: pd.DataFrame):
    valid_email = users["email"].str.match(EMAIL_PATTERN, na=False)
    valid_age = (users["age"] > 0) & users["age"].notna()
    valid_user_id = ~users["user_id"].duplicated()

    mask = valid_email & valid_age & valid_user_id
    return users[mask], users[~mask]


def validate_products(products: pd.DataFrame):
    valid_price = products["price"] > 0
    valid_stock = products["stock"].notna() & (products["stock"] >= 0)
    valid_product_id = ~products["product_id"].duplicated()

    mask = valid_price & valid_stock & valid_product_id
    return products[mask], products[~mask]


def validate_orders(orders, valid_users, valid_products):
    valid_user = orders["user_id"].isin(valid_users["user_id"])
    valid_product = orders["product_id"].isin(valid_products["product_id"])
    valid_quantity = orders["quantity"].notna() & (orders["quantity"] > 0)
    valid_total = orders["total_amount"].notna()
    valid_order_id = ~orders["order_id"].duplicated()

    mask = (
        valid_user
        & valid_product
        & valid_quantity
        & valid_total
        & valid_order_id
    )
    return orders[mask], orders[~mask]


def validate_payments(payments, valid_orders):
    valid_order = payments["order_id"].isin(valid_orders["order_id"])
    valid_amount = payments["amount"].notna() & (payments["amount"] > 0)
    valid_status = payments["status"].notna()
    valid_payment_id = ~payments["payment_id"].duplicated()

    mask = valid_order & valid_amount & valid_status & valid_payment_id
    return payments[mask], payments[~mask]


def validate_all():
    users = pd.read_csv("data/users.csv")
    products = pd.read_csv("data/products.csv")
    orders = pd.read_csv("data/order.csv")
    payments = pd.read_csv("data/payments.csv")

    valid_users, invalid_users = validate_users(users)
    valid_products, invalid_products = validate_products(products)
    valid_orders, invalid_orders = validate_orders(
        orders, valid_users, valid_products
    )
    valid_payments, invalid_payments = validate_payments(
        payments, valid_orders
    )

    valid_users.to_csv("data/valid_users.csv", index=False)
    invalid_users.to_csv("data/invalid_users.csv", index=False)

    valid_products.to_csv("data/valid_products.csv", index=False)
    invalid_products.to_csv("data/invalid_products.csv", index=False)

    valid_orders.to_csv("data/valid_order.csv", index=False)
    invalid_orders.to_csv("data/invalid_order.csv", index=False)

    valid_payments.to_csv("data/valid_payments.csv", index=False)
    invalid_payments.to_csv("data/invalid_payments.csv", index=False)

    return {
        "users": valid_users,
        "products": valid_products,
        "orders": valid_orders,
        "payments": valid_payments,
    }
