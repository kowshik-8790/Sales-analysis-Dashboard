"""
Database Loader and SQL Execution Engine
Supports MySQL 8.0+ with seamless zero-configuration SQLite fallback,
allowing local execution of all SQL KPI queries and reporting scripts.
"""

import os
import sys
import sqlite3
import pandas as pd
from sqlalchemy import create_engine, text

# Configuration defaults
DEFAULT_MYSQL_URL = os.getenv(
    "MYSQL_URI", "mysql+pymysql://root:password@localhost:3306/sales_analytics"
)


def get_base_dir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_processed_data_to_sqlite():
    """Load processed star-schema tables into an embedded SQLite database for immediate testing."""
    base_dir = get_base_dir()
    db_path = os.path.join(base_dir, "data", "sales_analytics.db")
    proc_dir = os.path.join(base_dir, "data", "processed")

    print(f"Initializing local SQL database at: {db_path}")
    conn = sqlite3.connect(db_path)

    tables = {
        "dim_customers": "dim_customers.csv",
        "dim_products": "dim_products.csv",
        "dim_regions": "dim_regions.csv",
        "dim_date": "dim_date.csv",
        "fact_sales": "clean_fact_sales.csv",
    }

    for tbl_name, filename in tables.items():
        file_path = os.path.join(proc_dir, filename)
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df.to_sql(tbl_name, conn, if_exists="replace", index=False)
            print(f"  [OK] Loaded {len(df):,} rows into '{tbl_name}'")
        else:
            print(f"  [WARN] Warning: {file_path} not found.")

    conn.close()
    print("Database sync complete.\n")
    return db_path


def run_sample_kpis(db_path):
    """Run core business KPI queries against the database and display results."""
    conn = sqlite3.connect(db_path)

    print("=" * 70)
    print("             EXECUTIVE SALES PERFORMANCE KPI REPORT")
    print("=" * 70)

    # 1. High-Level Financials
    q1 = """
    SELECT 
        COUNT(DISTINCT order_id) AS total_orders,
        SUM(quantity) AS total_units_sold,
        ROUND(SUM(sales), 2) AS total_revenue,
        ROUND(SUM(profit), 2) AS total_profit,
        ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct,
        ROUND(AVG(delivery_days), 1) AS avg_delivery_days
    FROM fact_sales;
    """
    res1 = pd.read_sql_query(q1, conn)
    print("\n--- 1. OVERALL FINANCIAL HEALTH ---")
    print(res1.to_string(index=False))

    # 2. Regional Breakdown
    q2 = """
    SELECT 
        c.region,
        COUNT(DISTINCT f.order_id) AS orders,
        ROUND(SUM(f.sales), 2) AS revenue,
        ROUND(SUM(f.profit), 2) AS profit,
        ROUND((SUM(f.profit) / SUM(f.sales)) * 100, 2) AS margin_pct,
        ROUND(AVG(f.discount) * 100, 1) AS avg_discount_pct
    FROM fact_sales f
    JOIN dim_customers c ON f.customer_id = c.customer_id
    GROUP BY c.region
    ORDER BY revenue DESC;
    """
    res2 = pd.read_sql_query(q2, conn)
    print("\n--- 2. REGIONAL PERFORMANCE & MARGIN HEALTH ---")
    print(res2.to_string(index=False))

    # 3. Top 5 Products by Revenue
    q3 = """
    SELECT 
        p.product_name,
        p.category,
        SUM(f.quantity) AS units,
        ROUND(SUM(f.sales), 2) AS revenue,
        ROUND(SUM(f.profit), 2) AS profit,
        ROUND((SUM(f.profit) / SUM(f.sales)) * 100, 2) AS margin_pct
    FROM fact_sales f
    JOIN dim_products p ON f.product_id = p.product_id
    GROUP BY p.product_id, p.product_name, p.category
    ORDER BY revenue DESC
    LIMIT 5;
    """
    res3 = pd.read_sql_query(q3, conn)
    print("\n--- 3. TOP 5 REVENUE GENERATING PRODUCTS ---")
    print(res3.to_string(index=False))

    conn.close()
    print("\n" + "=" * 70)


def load_to_mysql(connection_uri=DEFAULT_MYSQL_URL):
    """Optional loader for live MySQL instance when available."""
    try:
        engine = create_engine(connection_uri)
        with engine.connect() as conn:
            print(f"Connected to MySQL successfully at {connection_uri}")
            base_dir = get_base_dir()
            proc_dir = os.path.join(base_dir, "data", "processed")

            for tbl, fname in [
                ("dim_customers", "dim_customers.csv"),
                ("dim_products", "dim_products.csv"),
                ("dim_regions", "dim_regions.csv"),
                ("dim_date", "dim_date.csv"),
                ("fact_sales", "clean_fact_sales.csv"),
            ]:
                df = pd.read_csv(os.path.join(proc_dir, fname))
                df.to_sql(tbl, engine, if_exists="append", index=False)
                print(f"  [OK] Exported {len(df)} rows to MySQL table `{tbl}`")
    except Exception as e:
        print(f"Note: MySQL live connection not established ({e}).")
        print("Using local standalone database engine for all SQL analyses.")


if __name__ == "__main__":
    db_file = load_processed_data_to_sqlite()
    run_sample_kpis(db_file)
    if len(sys.argv) > 1 and sys.argv[1] == "--mysql":
        load_to_mysql()
