import pandas as pd
import random
from faker import Faker

fake = Faker()

NUM_CUSTOMERS = 10000
NUM_ORDERS = 20000

# ---------------------------
# Customers
# ---------------------------
customers = []

for i in range(1, NUM_CUSTOMERS + 1):
    customers.append({
        "customer_id": i,
        "name": fake.name(),
        "email": fake.email(),
        "city": fake.city()
    })

customers_df = pd.DataFrame(customers)
customers_df.to_csv("customers_large.csv", index=False)

print("✅ customers_large.csv created")


# ---------------------------
# Orders
# ---------------------------
orders = []

for i in range(1, NUM_ORDERS + 1):
    orders.append({
        "order_id": i,
        "customer_id": random.randint(1, NUM_CUSTOMERS),  # join key
        "order_date": fake.date_between(start_date="-1y", end_date="today"),
        "total_amount": random.randint(500, 50000)
    })

orders_df = pd.DataFrame(orders)
orders_df.to_csv("orders_large.csv", index=False)

print("✅ orders_large.csv created")