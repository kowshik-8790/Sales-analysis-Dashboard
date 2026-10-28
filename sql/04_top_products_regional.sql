-- ============================================================================
-- 04_top_products_regional.sql
-- Product and Geographic Deep-Dive Analysis
-- ============================================================================

USE sales_analytics;

-- ----------------------------------------------------------------------------
-- 1. Top 10 Revenue-Generating Products
-- ----------------------------------------------------------------------------
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    p.sub_category,
    SUM(f.quantity)                         AS units_sold,
    ROUND(SUM(f.sales), 2)                  AS total_revenue,
    ROUND(SUM(f.profit), 2)                 AS total_profit,
    ROUND((SUM(f.profit) / SUM(f.sales)) * 100, 2) AS profit_margin_pct,
    DENSE_RANK() OVER (ORDER BY SUM(f.sales) DESC) AS revenue_rank
FROM fact_sales f
JOIN dim_products p ON f.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category, p.sub_category
ORDER BY revenue_rank ASC
LIMIT 10;

-- ----------------------------------------------------------------------------
-- 2. Bottom 5 Margin / Loss-Making Products (Identify margin leakage)
-- ----------------------------------------------------------------------------
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    p.sub_category,
    SUM(f.quantity)                         AS units_sold,
    ROUND(SUM(f.sales), 2)                  AS total_revenue,
    ROUND(SUM(f.profit), 2)                 AS total_profit,
    ROUND((SUM(f.profit) / SUM(f.sales)) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(f.discount) * 100, 1)         AS avg_discount_pct
FROM fact_sales f
JOIN dim_products p ON f.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category, p.sub_category
ORDER BY profit_margin_pct ASC
LIMIT 5;

-- ----------------------------------------------------------------------------
-- 3. Regional Performance Comparison
-- ----------------------------------------------------------------------------
SELECT 
    c.region,
    COUNT(DISTINCT f.order_id)              AS order_volume,
    SUM(f.quantity)                         AS total_units,
    ROUND(SUM(f.sales), 2)                  AS total_revenue,
    ROUND(SUM(f.profit), 2)                 AS total_profit,
    ROUND((SUM(f.profit) / SUM(f.sales)) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(f.discount) * 100, 2)         AS avg_discount_applied,
    ROUND(AVG(f.delivery_days), 1)          AS avg_shipping_days
FROM fact_sales f
JOIN dim_customers c ON f.customer_id = c.customer_id
GROUP BY c.region
ORDER BY total_revenue DESC;

-- ----------------------------------------------------------------------------
-- 4. Shipping Mode Cost & Speed Trade-Off
-- ----------------------------------------------------------------------------
SELECT 
    f.ship_mode,
    COUNT(f.transaction_id)                 AS shipment_count,
    ROUND(SUM(f.sales), 2)                  AS total_sales,
    ROUND(SUM(f.profit), 2)                 AS total_profit,
    ROUND((SUM(f.profit) / SUM(f.sales)) * 100, 2) AS margin_pct,
    ROUND(AVG(f.delivery_days), 1)          AS avg_delivery_days,
    MIN(f.delivery_days)                    AS min_delivery_days,
    MAX(f.delivery_days)                    AS max_delivery_days
FROM fact_sales f
GROUP BY f.ship_mode
ORDER BY avg_delivery_days ASC;
