"""
ETL Pipeline & Data Cleaning Script
Cleans raw sales data using Python, Pandas, and NumPy, applies feature engineering,
creates star-schema dimension and fact tables, and exports clean datasets for
MySQL database ingestion and Power BI reporting.
"""

import os
import re
import numpy as np
import pandas as pd


def clean_currency_string(val):
    """Strip currency symbols, commas, and whitespace, returning float."""
    if pd.isna(val):
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    val_str = str(val).replace("$", "").replace(",", "").strip()
    try:
        return float(val_str)
    except ValueError:
        return 0.0


def parse_mixed_dates(series):
    """Parse dates with multiple format patterns safely."""
    return pd.to_datetime(series, format="mixed", dayfirst=False, errors="coerce")


def run_etl():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_path = os.path.join(base_dir, "data", "raw", "sales_raw_transactions.csv")
    proc_dir = os.path.join(base_dir, "data", "processed")
    os.makedirs(proc_dir, exist_ok=True)

    print("Step 1: Ingesting raw transactions...")
    df = pd.read_csv(raw_path, dtype={"Postal_Code": str})
    initial_rows = len(df)
    print(f"Loaded {initial_rows} raw records.")

    print("\nStep 2: Deduplication...")
    df = df.drop_duplicates(subset=["Transaction_ID"], keep="first")
    print(f"Deduplicated records: dropped {initial_rows - len(df)} duplicate transactions.")

    print("\nStep 3: Text & String Sanitization...")
    text_cols = ["Customer_Name", "Segment", "City", "State", "Region", "Product_Name", "Category", "Sub_Category", "Ship_Mode"]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Standardize casing
    df["Segment"] = df["Segment"].str.title()
    df["Category"] = df["Category"].str.title()
    df["Sub_Category"] = df["Sub_Category"].str.title()
    df["Region"] = df["Region"].str.title()

    print("\nStep 4: Imputing Missing Values...")
    df["Ship_Mode"] = df["Ship_Mode"].replace(["nan", "None", ""], "Standard Class").fillna("Standard Class")
    df["Postal_Code"] = df["Postal_Code"].replace(["nan", "None", ""], np.nan).fillna("00000")

    print("\nStep 5: Numeric & Currency Parsing...")
    df["Sales"] = df["Sales"].apply(clean_currency_string)
    df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce").fillna(0.0)
    df["Unit_Cost"] = pd.to_numeric(df["Unit_Cost"], errors="coerce").fillna(0.0)
    df["Unit_Price"] = pd.to_numeric(df["Unit_Price"], errors="coerce").fillna(0.0)
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(1).astype(int)
    df["Discount"] = pd.to_numeric(df["Discount"], errors="coerce").fillna(0.0)

    # Re-verify and clamp aberrant discount or quantity values
    df["Discount"] = df["Discount"].clip(lower=0.0, upper=0.70)
    df["Quantity"] = df["Quantity"].clip(lower=1, upper=50)

    print("\nStep 6: Date Parsing & Temporal Validation...")
    df["Order_Date"] = parse_mixed_dates(df["Order_Date"])
    df["Ship_Date"] = parse_mixed_dates(df["Ship_Date"])

    # Handle any unparseable dates
    df = df.dropna(subset=["Order_Date", "Ship_Date"]).copy()

    # Ensure Ship_Date is on or after Order_Date
    invalid_dates = df["Ship_Date"] < df["Order_Date"]
    if invalid_dates.any():
        df.loc[invalid_dates, "Ship_Date"] = df.loc[invalid_dates, "Order_Date"] + pd.Timedelta(days=2)

    print("\nStep 7: Feature Engineering...")
    # Shipping delivery duration
    df["Delivery_Days"] = (df["Ship_Date"] - df["Order_Date"]).dt.days

    # Calculated metrics
    df["Gross_Sales"] = np.round(df["Quantity"] * df["Unit_Price"], 2)
    df["Total_Cost"] = np.round(df["Quantity"] * df["Unit_Cost"], 2)
    df["Profit_Margin_Pct"] = np.where(df["Sales"] > 0, np.round((df["Profit"] / df["Sales"]) * 100, 2), 0.0)

    # Date dimensional attributes
    df["Order_Year"] = df["Order_Date"].dt.year
    df["Order_Month"] = df["Order_Date"].dt.month
    df["Order_Quarter"] = "Q" + df["Order_Date"].dt.quarter.astype(str)
    df["Order_Year_Month"] = df["Order_Date"].dt.strftime("%Y-%m")
    df["Order_Day_Name"] = df["Order_Date"].dt.day_name()

    # Business segmentation tags
    df["Discount_Band"] = pd.cut(
        df["Discount"],
        bins=[-0.01, 0.0, 0.10, 0.25, 1.0],
        labels=["No Discount (0%)", "Low (1-10%)", "Medium (11-25%)", "High (>25%)"]
    )
    df["Is_Profitable"] = df["Profit"] > 0
    df["High_Value_Order"] = df["Sales"] >= 1000.0

    print("\nStep 8: Star Schema Modeling & Export...")

    # Dimension: Customers
    dim_customers = (
        df[["Customer_ID", "Customer_Name", "Segment", "City", "State", "Region", "Postal_Code"]]
        .drop_duplicates(subset=["Customer_ID"])
        .sort_values(by="Customer_ID")
    )
    cust_path = os.path.join(proc_dir, "dim_customers.csv")
    dim_customers.to_csv(cust_path, index=False)
    print(f"Exported {len(dim_customers)} records to {cust_path}")

    # Dimension: Products
    dim_products = (
        df[["Product_ID", "Product_Name", "Category", "Sub_Category", "Unit_Cost", "Unit_Price"]]
        .drop_duplicates(subset=["Product_ID"])
        .sort_values(by="Product_ID")
    )
    prod_path = os.path.join(proc_dir, "dim_products.csv")
    dim_products.to_csv(prod_path, index=False)
    print(f"Exported {len(dim_products)} records to {prod_path}")

    # Dimension: Regions / Geography
    dim_regions = (
        df[["Region", "State", "City"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    dim_regions["Region_ID"] = [f"REG-{i+101}" for i in range(len(dim_regions))]
    dim_regions = dim_regions[["Region_ID", "Region", "State", "City"]]
    reg_path = os.path.join(proc_dir, "dim_regions.csv")
    dim_regions.to_csv(reg_path, index=False)
    print(f"Exported {len(dim_regions)} records to {reg_path}")

    # Dimension: Calendar Date
    min_date = df["Order_Date"].min()
    max_date = max(df["Ship_Date"].max(), df["Order_Date"].max())
    date_range = pd.date_range(start=min_date, end=max_date, freq="D")
    dim_date = pd.DataFrame({
        "Date": date_range.strftime("%Y-%m-%d"),
        "Year": date_range.year,
        "Quarter": "Q" + date_range.quarter.astype(str),
        "Month": date_range.month,
        "Month_Name": date_range.strftime("%B"),
        "Month_Year": date_range.strftime("%b %Y"),
        "Day": date_range.day,
        "Day_Name": date_range.strftime("%A"),
        "Is_Weekend": date_range.dayofweek.isin([5, 6]).astype(int)
    })
    date_path = os.path.join(proc_dir, "dim_date.csv")
    dim_date.to_csv(date_path, index=False)
    print(f"Exported {len(dim_date)} dates to {date_path}")

    # Fact: Sales Transactions
    fact_cols = [
        "Transaction_ID", "Order_ID", "Order_Date", "Ship_Date", "Customer_ID",
        "Product_ID", "Ship_Mode", "Quantity", "Unit_Cost", "Unit_Price",
        "Discount", "Sales", "Profit", "Profit_Margin_Pct", "Delivery_Days",
        "Discount_Band", "High_Value_Order"
    ]
    fact_sales = df[fact_cols].copy()
    fact_sales["Order_Date"] = fact_sales["Order_Date"].dt.strftime("%Y-%m-%d")
    fact_sales["Ship_Date"] = fact_sales["Ship_Date"].dt.strftime("%Y-%m-%d")

    fact_path = os.path.join(proc_dir, "clean_fact_sales.csv")
    fact_sales.to_csv(fact_path, index=False)
    print(f"Exported {len(fact_sales)} fact records to {fact_path}")

    # Consolidated Denormalized Clean Dataset for Direct Power BI / Excel Import
    denorm_path = os.path.join(proc_dir, "clean_sales_data_complete.csv")
    df_clean_export = df.copy()
    df_clean_export["Order_Date"] = df_clean_export["Order_Date"].dt.strftime("%Y-%m-%d")
    df_clean_export["Ship_Date"] = df_clean_export["Ship_Date"].dt.strftime("%Y-%m-%d")
    df_clean_export.to_csv(denorm_path, index=False)
    print(f"Exported consolidated dataset ({len(df_clean_export)} rows) to {denorm_path}")

    print("\nETL Pipeline completed successfully!")
    print(f"Summary KPIs:")
    print(f"  • Total Revenue:       ${df['Sales'].sum():,.2f}")
    print(f"  • Total Profit:        ${df['Profit'].sum():,.2f}")
    print(f"  • Profit Margin:       {(df['Profit'].sum() / df['Sales'].sum()) * 100:.2f}%")
    print(f"  • Total Orders:        {df['Order_ID'].nunique():,}")
    print(f"  • Avg Delivery Days:   {df['Delivery_Days'].mean():.1f} days")


if __name__ == "__main__":
    run_etl()
