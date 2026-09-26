import pandas as pd
import numpy as np
import datetime
import json

# Set random seed for reproducibility
np.random.seed(42)

# Generate 1,250 transactional records to match "1,200+ transactional records"
n_records = 1250

categories = {
    'Technology': ['Enterprise Laptops', 'UltraHD Monitors', 'Wireless Headsets', 'Cloud Servers', 'Smart Projectors'],
    'Office Supplies': ['Ergonomic Chairs', 'Executive Desks', 'Filing Cabinets', 'Laser Printers', 'Paper Shredders'],
    'Furniture': ['Modern Conference Tables', 'Modular Workstations', 'Acoustic Panels', 'Task Lighting', 'Storage Shelves'],
    'Software & Services': ['SaaS Enterprise Licenses', 'Data Analytics Suite', 'Cybersecurity Audits', 'Cloud Migration Services']
}

regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America']
sales_channels = ['Direct Enterprise', 'Online Portal', 'Partner Reseller', 'Retail Store']

start_date = datetime.date(2025, 1, 1)
date_list = [start_date + datetime.timedelta(days=int(i)) for i in range(365)]

data = []

total_rev_target = 1490000.0  # $1.49M Target
running_revenue = 0.0

for i in range(1, n_records + 1):
    order_id = f"ORD-{2025000 + i}"
    order_date = np.random.choice(date_list)
    region = np.random.choice(regions, p=[0.40, 0.28, 0.20, 0.12])
    category = np.random.choice(list(categories.keys()), p=[0.45, 0.25, 0.18, 0.12])
    product = np.random.choice(categories[category])
    channel = np.random.choice(sales_channels)
    
    quantity = int(np.random.randint(1, 15))
    unit_price = float(np.random.uniform(50, 1800))
    
    # Discount between 0% and 40%
    discount_pct = float(np.random.choice([0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40], p=[0.25, 0.20, 0.20, 0.15, 0.08, 0.05, 0.04, 0.02, 0.01]))
    
    base_cost_ratio = np.random.uniform(0.55, 0.72)
    unit_cost = unit_price * base_cost_ratio
    
    gross_sales = round(quantity * unit_price, 2)
    discount_amount = round(gross_sales * discount_pct, 2)
    net_revenue = round(gross_sales - discount_amount, 2)
    total_cost = round(quantity * unit_cost, 2)
    profit = round(net_revenue - total_cost, 2)
    profit_margin = round((profit / net_revenue) * 100, 2) if net_revenue > 0 else 0.0
    
    high_discount_flag = discount_pct >= 0.25
    
    data.append({
        'order_id': order_id,
        'order_date': order_date.strftime('%Y-%m-%d'),
        'region': region,
        'category': category,
        'product': product,
        'sales_channel': channel,
        'quantity': quantity,
        'unit_price': unit_price,
        'gross_sales': gross_sales,
        'discount_pct': discount_pct,
        'discount_amount': discount_amount,
        'net_revenue': net_revenue,
        'total_cost': total_cost,
        'profit': profit,
        'profit_margin': profit_margin,
        'high_discount_erosion': high_discount_flag
    })

df = pd.DataFrame(data)

# Scaling factor to match exactly ~$1.49M Revenue and ~20.7% Profit Margin
rev_scale = 1490000.0 / df['net_revenue'].sum()
df['gross_sales'] = (df['gross_sales'] * rev_scale).round(2)
df['discount_amount'] = (df['discount_amount'] * rev_scale).round(2)
df['net_revenue'] = (df['net_revenue'] * rev_scale).round(2)

# Adjust cost to get 20.7% profit margin overall
target_profit = df['net_revenue'].sum() * 0.207
current_profit = df['profit'].sum()
profit_scale = target_profit / current_profit
df['profit'] = (df['profit'] * profit_scale).round(2)
df['total_cost'] = (df['net_revenue'] - df['profit']).round(2)
df['profit_margin'] = ((df['profit'] / df['net_revenue']) * 100).round(2)

df.to_csv('sales_data.csv', index=False)
print(f"Generated {len(df)} records.")
print(f"Total Revenue: ${df['net_revenue'].sum():,.2f}")
print(f"Total Profit: ${df['profit'].sum():,.2f}")
print(f"Profit Margin: {(df['profit'].sum()/df['net_revenue'].sum())*100:.2f}%")
print(f"High Discount Erosion Orders (>=25%): {df['high_discount_erosion'].sum()}")

# Export JSON for static frontend web dashboard
df.to_json('sales_data.json', orient='records')
