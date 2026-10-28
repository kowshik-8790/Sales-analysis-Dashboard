-- ============================================================================
-- 03_kpi_analysis.sql
-- Core Business KPIs: Revenue, Profit Margin, MoM Growth, YoY Growth, Trends
-- ============================================================================

USE sales_analytics;

-- ----------------------------------------------------------------------------
-- KPI 1: Overall High-Level Business Summary
-- ----------------------------------------------------------------------------
SELECT 
    COUNT(DISTINCT order_id)                                AS total_orders,
    SUM(quantity)                                           AS total_units_sold,
    ROUND(SUM(sales), 2)                                    AS total_revenue,
    ROUND(SUM(profit), 2)                                   AS total_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2)              AS overall_profit_margin_pct,
    ROUND(SUM(sales) / COUNT(DISTINCT order_id), 2)         AS average_order_value,
    ROUND(AVG(delivery_days), 1)                            AS avg_fulfillment_days
FROM fact_sales;

-- ----------------------------------------------------------------------------
-- KPI 2: Monthly Sales Trend with MoM (Month-over-Month) Growth
-- Utilizes LAG() window function to calculate progression
-- ----------------------------------------------------------------------------
WITH monthly_metrics AS (
    SELECT 
        d.year,
        d.month,
        d.month_year,
        ROUND(SUM(f.sales), 2) AS monthly_revenue,
        ROUND(SUM(f.profit), 2) AS monthly_profit,
        ROUND((SUM(f.profit) / SUM(f.sales)) * 100, 2) AS monthly_margin_pct
    FROM fact_sales f
    JOIN dim_date d ON f.order_date = d.date_id
    GROUP BY d.year, d.month, d.month_year
)
SELECT 
    year,
    month,
    month_year,
    monthly_revenue,
    LAG(monthly_revenue, 1) OVER (ORDER BY year, month) AS prev_month_revenue,
    ROUND(
        ((monthly_revenue - LAG(monthly_revenue, 1) OVER (ORDER BY year, month)) 
         / NULLIF(LAG(monthly_revenue, 1) OVER (ORDER BY year, month), 0)) * 100, 
        2
    ) AS mom_revenue_growth_pct,
    monthly_profit,
    monthly_margin_pct,
    -- 3-Month Rolling Average Revenue
    ROUND(AVG(monthly_revenue) OVER (
        ORDER BY year, month 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS rolling_3m_avg_revenue
FROM monthly_metrics
ORDER BY year, month;

-- ----------------------------------------------------------------------------
-- KPI 3: Year-Over-Year (YoY) Sales & Profit Performance
-- ----------------------------------------------------------------------------
WITH annual_metrics AS (
    SELECT 
        d.year,
        COUNT(DISTINCT f.order_id) AS annual_orders,
        ROUND(SUM(f.sales), 2)     AS annual_revenue,
        ROUND(SUM(f.profit), 2)    AS annual_profit
    FROM fact_sales f
    JOIN dim_date d ON f.order_date = d.date_id
    GROUP BY d.year
)
SELECT 
    year,
    annual_orders,
    annual_revenue,
    LAG(annual_revenue, 1) OVER (ORDER BY year) AS prev_year_revenue,
    ROUND(
        ((annual_revenue - LAG(annual_revenue, 1) OVER (ORDER BY year)) 
         / NULLIF(LAG(annual_revenue, 1) OVER (ORDER BY year), 0)) * 100, 
        2
    ) AS yoy_revenue_growth_pct,
    annual_profit,
    ROUND((annual_profit / annual_revenue) * 100, 2) AS annual_margin_pct
FROM annual_metrics
ORDER BY year;

-- ----------------------------------------------------------------------------
-- KPI 4: Impact of Discounting on Profit Margin
-- Demonstrates how aggressive promotions degrade profitability
-- ----------------------------------------------------------------------------
SELECT 
    f.discount_band,
    COUNT(f.transaction_id)                         AS transaction_count,
    ROUND(SUM(f.sales), 2)                          AS total_sales,
    ROUND(SUM(f.profit), 2)                         AS total_profit,
    ROUND((SUM(f.profit) / SUM(f.sales)) * 100, 2)  AS realized_profit_margin_pct,
    ROUND(AVG(f.discount) * 100, 1)                 AS avg_discount_rate
FROM fact_sales f
GROUP BY f.discount_band
ORDER BY avg_discount_rate ASC;
