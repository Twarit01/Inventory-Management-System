import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

store_name = "My Inventory "

inventory_list = [
    {"product_id": 101, "name": "Basic T-Shirt", "category": "Clothing", "price": 299},
    {"product_id": 102, "name": "Wireless Mouse", "category": "Electronics", "price": 599},
]
# === Functions ===
def add_tax(price, tax_percent=18):
    return price * (1 + tax_percent / 100)

# === NumPy operations ===
np.random.seed(42)

product_ids = np.arange(201, 207)
prices = np.round(np.random.uniform(100, 2000, size=6), 2)

monthly_units = np.random.randint(10, 200, size=(6, 6))

# Revenue calculations
revenue_matrix = monthly_units * prices.reshape(6, 1)

product_total_units = monthly_units.sum(axis=1)
product_total_revenue = revenue_matrix.sum(axis=1)

# --------------------------------- ENCAPSULATION ---------------------------------
class Product:
    def __init__(self, product_id, name, category, price, stock=0):
        self.product_id = product_id
        self.name = name
        self.category = category
        self._price = price          # Protected attribute → Encapsulation
        self.stock = stock

#POLYMORPHISM (Base Method)
    def info(self):
        return f"{self.name} ({self.category}) - ₹{self._price} | Stock: {self.stock}"

class Electronics(Product):
    def __init__(self, product_id, name, price, stock=0, warranty_months=12):
        super().__init__(product_id, name, "Electronics", price, stock)
        self.warranty = warranty_months

    def info(self):
        return super().info() + f" | Warranty: {self.warranty} months"

class Clothing(Product):
    def __init__(self, product_id, name, price, stock=0, sizes=None):
        super().__init__(product_id, name, "Clothing", price, stock)
        self.sizes = sizes or ["S", "M", "L"]
    # --------------------------- METHOD OVERRIDING ---------------------------------
    def info(self):
        return super().info() + f" | Sizes: {', '.join(self.sizes)}"

def print_product_info(item: Product):
    print(item.info())
    
# === Pandas DataFrames ===
inventory_df = pd.DataFrame({
    "product_id": product_ids,
    "name": [f"Product_{i}" for i in product_ids],
    "category": ["Electronics", "Clothing", "Electronics", "Clothing", "Home", "Electronics"],
    "price": prices,
    "stock": np.random.randint(5, 50, size=6),
})

months = pd.date_range(start="2025-01-01", periods=6, freq="MS").strftime("%Y-%m").tolist()

rows = []
for i, pid in enumerate(product_ids):
    for m_idx, month in enumerate(months):
        rows.append({
            "product_id": int(pid),
            "month": month,
            "units_sold": int(monthly_units[i, m_idx]),
            "unit_price": float(prices[i]),
        })

sales_df = pd.DataFrame(rows) #list of dict
sales_df["revenue"] = sales_df["units_sold"] * sales_df["unit_price"] #new column

# Missing Value fix
sales_df["units_sold"] = sales_df["units_sold"].fillna(0).astype(int)
sales_df["revenue"] = sales_df["units_sold"] * sales_df["unit_price"]

# Monthly summary
monthly_summary = sales_df.groupby("month").agg(
    total_revenue=("revenue", "sum"),
    total_units=("units_sold", "sum")
).reset_index()

# Add price with tax
inventory_df["price_with_tax"] = inventory_df["price"].apply(add_tax)

def create_plots_bar():
    plt.figure(figsize=(10, 5))
    plt.bar(product_ids, product_total_revenue)
    plt.title("Total Revenue per Product")
    plt.xlabel("Product ID")
    plt.ylabel("Revenue")
    plt.tight_layout()
    plt.show()

def create_plots_line():
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=monthly_summary, x="month", y="total_revenue", marker="o")
    plt.xticks(rotation=45)
    plt.title("Monthly Total Revenue (6 Months)")
    plt.tight_layout()
    plt.show()

def add_product_interactive():
    try:
        pid = int(input("Enter Product ID: "))
        name = input("Enter Name: ")
        category = input("Enter Category: ")
        price = float(input("Enter Price: "))
        stock = int(input("Enter Stock: "))

        new_row = pd.DataFrame({
            "product_id": [pid],
            "name": [name],
            "category": [category],
            "price": [price],
            "stock": [stock],
        })

        global inventory_df
        inventory_df = pd.concat([inventory_df, new_row], ignore_index=True)
        inventory_df["price_with_tax"] = inventory_df["price"].apply(add_tax)

        print("Product added successfully!")

    except Exception as e:
        print("Error adding product:", e)

def graph_menu():
    while True:
        print("\n====== GRAPH MENU ======")
        print("1. Revenue per Product")
        print("2. Monthly Revenue")
        print("3. Back")
        g = input("Enter choice: ").strip()
        if g == "1":
            create_plots_bar()
        elif g == "2":
            create_plots_line()
        elif g == "3":
            break
        else:
            print("Invalid choice!")
def menu():
    while True:
        print("\n====== ONLINE STORE MENU ======")
        print("1. View Inventory DataFrame")
        print("2. View Sales DataFrame")
        print("3. Show Monthly Revenue Summary")
        print("4. Display Graphs Menu")
        print("5. Add New Product")
        print("6. Exit")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            print("\n--- INVENTORY DATAFRAME ---\n")
            print(inventory_df)
        elif choice == "2":
            print("\n--- SALES DATAFRAME ---\n")
            print(sales_df.sample(6))
        elif choice == "3":
            print("\n--- MONTHLY SUMMARY ---\n")
            print(monthly_summary)
        elif choice == "4":
            graph_menu()
        elif choice == "5":
            add_product_interactive()
        elif choice == "6":
            print("Exiting...")
            break
if __name__ == "__main__":
    menu()
