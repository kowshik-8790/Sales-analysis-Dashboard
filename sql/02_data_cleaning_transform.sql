-- ============================================================================
-- 02_data_cleaning_transform.sql
-- Data Cleaning, Sanitization, and Analytical Views in SQL
-- ============================================================================

USE sales_analytics;

-- 1. Cleaning Script: Check for and purge duplicate transaction records
DELETE t1 FROM fact_sales t1
INNER JOIN fact_sales t2 
WHERE t1.created_at > t2.created_at 
  AND t1.transaction_id = t2.transaction_id;

-- 2. Clean trailing whitespaces and normalize casing across dimensions
UPDATE dim_customers
SET 
    customer_name = TRIM(customer_name),
    city          = TRIM(city),
    state         = TRIM(state),
    region        = TRIM(region),
    segment       = CONCAT(UPPER(SUBSTRING(segment, 1, 1)), LOWER(SUBSTRING(segment, 2)));

UPDATE dim_products
SET 
    product_name = TRIM(product_name),
    category     = TRIM(category),
    sub_category = TRIM(sub_category);

-- 3. Fix NULL or missing postal codes
UPDATE dim_customers
SET postal_code = '00000'
WHERE postal_code IS NULL OR postal_code = '' OR postal_code = 'nan';

-- 4. Analytical View: Executive Overview View
CREATE OR REPLACE VIEW v_executive_sales_summary AS
SELECT 
    d.year,
    d.quarter,
    d.month,
    d.month_name,
    COUNT(DISTINCT f.order_id)          AS total_orders,
    COUNT(f.transaction_id)             AS total_transactions,
    SUM(f.quantity)                     AS total_units_sold,
    ROUND(SUM(f.sales), 2)              AS total_revenue,
    ROUND(SUM(f.profit), 2)             AS total_profit,
    ROUND((SUM(f.profit) / NULLIF(SUM(f.sales), 0)) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(f.delivery_days), 1)      AS avg_delivery_days,
    ROUND(SUM(f.sales) / NULLIF(COUNT(DISTINCT f.order_id), 0), 2) AS avg_order_value
FROM fact_sales f
JOIN dim_date d ON f.order_date = d.date_id
GROUP BY d.year, d.quarter, d.month, d.month_name;

-- 5. Analytical View: Regional Breakdown View
CREATE OR REPLACE VIEW v_regional_performance AS
SELECT 
    c.region,
    c.state,
    c.city,
    COUNT(DISTINCT c.customer_id)       AS unique_customers,
    COUNT(DISTINCT f.order_id)          AS total_orders,
    SUM(f.quantity)                     AS units_sold,
    ROUND(SUM(f.sales), 2)              AS total_revenue,
    ROUND(SUM(f.profit), 2)             AS total_profit,
    ROUND((SUM(f.profit) / NULLIF(SUM(f.sales), 0)) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(f.discount) * 100, 1)     AS avg_discount_pct,
    ROUND(AVG(f.delivery_days), 1)      AS avg_delivery_days
FROM fact_sales f
JOIN dim_customers c ON f.customer_id = c.customer_id
GROUP BY c.region, c.state, c.city;
