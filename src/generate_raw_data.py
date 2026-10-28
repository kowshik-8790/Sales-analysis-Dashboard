"""
Raw Sales Data Generator
Generates realistic multi-year enterprise sales transactions with intentional
data quality quirks (duplicates, missing values, inconsistent casing, mixed date formats)
to showcase robust cleaning workflows across Python, SQL, and Excel.
"""

import os
import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

# Set deterministic seed for reproducibility
np.random.seed(42)
random.seed(42)

TOTAL_RECORDS = 12000

# Base Reference Data
CUSTOMERS = [
    ("CUST-1001", "Aaron Bergman", "Consumer", "Seattle", "Washington", "West", "98101"),
    ("CUST-1002", "Darrin Martin", "Consumer", "Los Angeles", "California", "West", "90001"),
    ("CUST-1003", "Sean O'Donnell", "Consumer", "San Francisco", "California", "West", "94102"),
    ("CUST-1004", "Brosina Hoffman", "Consumer", "San Diego", "California", "West", "92101"),
    ("CUST-1005", "Zuschuss Donatelli", "Consumer", "Denver", "Colorado", "West", "80201"),
    ("CUST-1006", "Pete Kriz", "Consumer", "Phoenix", "Arizona", "West", "85001"),
    ("CUST-1007", "Ken Black", "Corporate", "New York City", "New York", "East", "10001"),
    ("CUST-1008", "Sandra Flanagan", "Corporate", "Philadelphia", "Pennsylvania", "East", "19102"),
    ("CUST-1009", "Emily Phan", "Consumer", "Boston", "Massachusetts", "East", "02108"),
    ("CUST-1010", "Eric Hoffmann", "Consumer", "Columbus", "Ohio", "East", "43215"),
    ("CUST-1011", "Tracy Blumstein", "Home Office", "Chicago", "Illinois", "Central", "60601"),
    ("CUST-1012", "Matt Abelman", "Home Office", "Detroit", "Michigan", "Central", "48201"),
    ("CUST-1013", "Gene Hale", "Corporate", "Minneapolis", "Minnesota", "Central", "55401"),
    ("CUST-1014", "Steve Nguyen", "Home Office", "Dallas", "Texas", "Central", "75201"),
    ("CUST-1015", "Linda Cazamias", "Corporate", "Houston", "Texas", "Central", "77001"),
    ("CUST-1016", "Ruben Ausman", "Corporate", "Atlanta", "Georgia", "South", "30301"),
    ("CUST-1017", "Erin Smith", "Corporate", "Miami", "Florida", "South", "33101"),
    ("CUST-1018", "Odessa Haupt", "Consumer", "Charlotte", "North Carolina", "South", "28201"),
    ("CUST-1019", "Harold Pawlan", "Home Office", "Nashville", "Tennessee", "South", "37201"),
    ("CUST-1020", "Patrick O'Brill", "Consumer", "Richmond", "Virginia", "South", "23219"),
    ("CUST-1021", "Mick Brown", "Consumer", "Austin", "Texas", "Central", "73301"),
    ("CUST-1022", "Jane Waco", "Corporate", "Portland", "Oregon", "West", "97201"),
    ("CUST-1023", "Dave Poirier", "Corporate", "San Jose", "California", "West", "95101"),
    ("CUST-1024", "Seth Vernon", "Consumer", "Tampa", "Florida", "South", "33601"),
    ("CUST-1025", "Bill Tyler", "Corporate", "Indianapolis", "Indiana", "Central", "46201"),
]

PRODUCTS = [
    # Technology
    ("TEC-PH-1001", "Apple iPhone 15 Pro", "Technology", "Phones", 750.00, 999.00),
    ("TEC-PH-1002", "Samsung Galaxy S24 Ultra", "Technology", "Phones", 800.00, 1199.00),
    ("TEC-PH-1003", "Google Pixel 8 Pro", "Technology", "Phones", 550.00, 799.00),
    ("TEC-AC-1004", "Sony WH-1000XM5 Headphones", "Technology", "Accessories", 220.00, 399.00),
    ("TEC-AC-1005", "Logitech MX Master 3S Mouse", "Technology", "Accessories", 50.00, 99.00),
    ("TEC-CO-1006", "Dell XPS 15 Laptop", "Technology", "Computers", 1200.00, 1899.00),
    ("TEC-CO-1007", "MacBook Pro 14 M3", "Technology", "Computers", 1400.00, 1999.00),
    ("TEC-PR-1008", "HP LaserJet Pro Multi-Function", "Technology", "Machines", 280.00, 449.00),
    # Furniture
    ("FUR-CH-2001", "Herman Miller Aeron Chair", "Furniture", "Chairs", 700.00, 1250.00),
    ("FUR-CH-2002", "Steelcase Gesture Ergonomic Chair", "Furniture", "Chairs", 650.00, 1120.00),
    ("FUR-TA-2003", "ApexDesk Height Adjustable Desk", "Furniture", "Tables", 350.00, 680.00),
    ("FUR-TA-2004", "Bush Business Conference Table", "Furniture", "Tables", 420.00, 850.00),
    ("FUR-BO-2005", "Sauder 5-Shelf Bookcase", "Furniture", "Bookcases", 110.00, 219.00),
    ("FUR-FU-2006", "Tenex Anti-Fatigue Floor Mat", "Furniture", "Furnishings", 35.00, 69.00),
    # Office Supplies
    ("OFF-ST-3001", "Fellowes Heavy-Duty Storage Box", "Office Supplies", "Storage", 15.00, 32.00),
    ("OFF-BI-3002", "GBC VeloBind Binding System", "Office Supplies", "Binders", 130.00, 260.00),
    ("OFF-PA-3003", "Hammermill Premium Multipurpose Paper", "Office Supplies", "Paper", 22.00, 48.00),
    ("OFF-AP-3004", "Breville Compact Microwave Oven", "Office Supplies", "Appliances", 90.00, 179.00),
    ("OFF-AR-3005", "Prismacolor Premier Colored Pencils", "Office Supplies", "Art", 12.00, 28.00),
    ("OFF-EN-3006", "Quality Park Security Envelopes 500pk", "Office Supplies", "Envelopes", 18.00, 39.00),
    ("OFF-FA-3007", "Staples Heavy Duty Stapler & Staples", "Office Supplies", "Fasteners", 10.00, 24.00),
    ("OFF-SU-3008", "Fiskars Titanium Easy Action Scissors", "Office Supplies", "Supplies", 8.00, 19.00),
]

SHIP_MODES = ["Standard Class", "Second Class", "First Class", "Same Day"]
DISCOUNT_CHOICES = [0.0, 0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50]


def generate_sales_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, "data", "raw")
    os.makedirs(raw_dir, exist_ok=True)

    start_date = datetime(2023, 1, 1)
    end_date = datetime(2025, 12, 31)
    date_range_days = (end_date - start_date).days

    rows = []
    order_counter = 100000

    for i in range(TOTAL_RECORDS):
        order_counter += random.choice([0, 0, 1, 1, 1, 2])
        order_id = f"CA-{order_counter}"

        cust = random.choice(CUSTOMERS)
        prod = random.choice(PRODUCTS)

        # Seasonal order date distribution (higher volume in Q4)
        day_offset = random.randint(0, date_range_days)
        order_dt = start_date + timedelta(days=day_offset)

        # Shipping delay 1-6 days
        ship_delay = random.choice([1, 2, 3, 3, 4, 5, 6])
        ship_dt = order_dt + timedelta(days=ship_delay)

        ship_mode = random.choice(SHIP_MODES)
        quantity = random.randint(1, 10)
        unit_cost = prod[4]
        unit_price = prod[5]
        discount = random.choice(DISCOUNT_CHOICES)

        # Introduce high discounts occasionally to simulate margin pressure in South/Central
        if cust[5] in ["Central", "South"] and random.random() < 0.25:
            discount = random.choice([0.30, 0.40, 0.50, 0.60])

        gross_sales = quantity * unit_price
        net_sales = round(gross_sales * (1.0 - discount), 2)
        total_cost = round(quantity * unit_cost, 2)
        profit = round(net_sales - total_cost, 2)

        # Inconsistent date format simulation for 8% of records
        date_format_flavor = random.random()
        if date_format_flavor < 0.70:
            order_date_str = order_dt.strftime("%Y-%m-%d")
            ship_date_str = ship_dt.strftime("%Y-%m-%d")
        elif date_format_flavor < 0.85:
            order_date_str = order_dt.strftime("%m/%d/%Y")
            ship_date_str = ship_dt.strftime("%m/%d/%Y")
        else:
            order_date_str = order_dt.strftime("%d-%m-%Y")
            ship_date_str = ship_dt.strftime("%d-%m-%Y")

        # Casing inconsistency simulation
        segment_val = cust[2]
        if random.random() < 0.05:
            segment_val = segment_val.upper() if random.random() < 0.5 else segment_val.lower()

        # Whitespace quirks simulation
        cust_name = cust[1]
        if random.random() < 0.04:
            cust_name = f"  {cust_name}  "

        # Missing postal code simulation
        postal_code = cust[6]
        if random.random() < 0.03:
            postal_code = None

        # Missing ship mode simulation
        if random.random() < 0.02:
            ship_mode = None

        # Dirty string sales formatting for 3% of records
        sales_val = net_sales
        if random.random() < 0.03:
            sales_val = f"${net_sales:,.2f}"

        rows.append({
            "Transaction_ID": f"TRX-{100000 + i}",
            "Order_ID": order_id,
            "Order_Date": order_date_str,
            "Ship_Date": ship_date_str,
            "Ship_Mode": ship_mode,
            "Customer_ID": cust[0],
            "Customer_Name": cust_name,
            "Segment": segment_val,
            "City": cust[3],
            "State": cust[4],
            "Region": cust[5],
            "Postal_Code": postal_code,
            "Product_ID": prod[0],
            "Product_Name": prod[1],
            "Category": prod[2],
            "Sub_Category": prod[3],
            "Unit_Cost": unit_cost,
            "Unit_Price": unit_price,
            "Quantity": quantity,
            "Discount": discount,
            "Sales": sales_val,
            "Profit": profit
        })

    df = pd.DataFrame(rows)

    # Inject ~50 duplicate rows to mimic real enterprise batch glitches
    dup_sample = df.sample(n=50, random_state=42)
    df = pd.concat([df, dup_sample], ignore_index=True)

    csv_path = os.path.join(raw_dir, "sales_raw_transactions.csv")
    df.to_csv(csv_path, index=False)
    print(f"Generated raw transactions CSV: {csv_path} ({len(df)} records)")

    # Also save an Excel raw file with first 3,000 records for Excel workflow demo
    excel_path = os.path.join(raw_dir, "sales_raw_dataset.xlsx")
    df.head(3000).to_excel(excel_path, sheet_name="Raw_Transactions", index=False)
    print(f"Generated raw transactions Excel: {excel_path} (3000 sample records)")

    return csv_path


if __name__ == "__main__":
    generate_sales_data()
