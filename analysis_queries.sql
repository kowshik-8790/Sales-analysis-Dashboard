-- ====================================================================
-- Sales Performance & Business Decision Queries
-- Author: Kasanaboina Kowshik (kasanaboinakowshik@gmail.com)
-- ====================================================================

USE sales_analytics_db;

-- 1. OVERALL EXECUTIVE KPIs (Revenue, Gross Sales, Total Profit, Profit Margin)
SELECT 
    COUNT(order_id) AS total_orders,
    ROUND(SUM(gross_sales), 2) AS total_gross_sales,
    ROUND(SUM(discount_amount), 2) AS total_discounts_given,
    ROUND(SUM(net_revenue), 2) AS total_net_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(net_revenue)) * 100, 2) AS overall_profit_margin_pct
FROM sales_transactions;

-- 2. REGIONAL PERFORMANCE COMPARISON
SELECT 
    region,
    COUNT(order_id) AS order_count,
    ROUND(SUM(net_revenue), 2) AS region_revenue,
    ROUND(SUM(profit), 2) AS region_profit,
    ROUND((SUM(profit) / SUM(net_revenue)) * 100, 2) AS profit_margin_pct,
    ROUND((SUM(net_revenue) / (SELECT SUM(net_revenue) FROM sales_transactions)) * 100, 2) AS revenue_contribution_pct
FROM sales_transactions
GROUP BY region
ORDER BY region_revenue DESC;

-- 3. PRODUCT CATEGORY REVENUE & PROFITABILITY
SELECT 
    category,
    COUNT(order_id) AS total_transactions,
    ROUND(SUM(net_revenue), 2) AS category_revenue,
    ROUND(SUM(profit), 2) AS category_profit,
    ROUND((SUM(profit) / SUM(net_revenue)) * 100, 2) AS profit_margin_pct
FROM sales_transactions
GROUP BY category
ORDER BY category_revenue DESC;

-- 4. TOP 5 BEST-SELLING & MOST PROFITABLE PRODUCTS
SELECT 
    product,
    category,
    SUM(quantity) AS total_units_sold,
    ROUND(SUM(net_revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(net_revenue)) * 100, 2) AS profit_margin_pct
FROM sales_transactions
GROUP BY product, category
ORDER BY total_revenue DESC
LIMIT 5;

-- 5. MONTHLY SALES TREND (Time Series Performance)
SELECT 
    DATE_FORMAT(order_date, '%Y-%m') AS sales_month,
    COUNT(order_id) AS total_orders,
    ROUND(SUM(net_revenue), 2) AS monthly_revenue,
    ROUND(SUM(profit), 2) AS monthly_profit,
    ROUND((SUM(profit) / SUM(net_revenue)) * 100, 2) AS monthly_margin_pct
FROM sales_transactions
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY sales_month ASC;

-- 6. HIGH-DISCOUNT MARGIN EROSION ANALYSIS (Discount >= 25%)
-- Evaluates how heavy discounting erodes corporate profit margins
SELECT 
    CASE 
        WHEN discount_pct >= 0.25 THEN 'High Discount (>= 25%)'
        ELSE 'Normal Discount (< 25%)'
    END AS discount_tier,
    COUNT(order_id) AS order_count,
    ROUND(SUM(net_revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(net_revenue)) * 100, 2) AS realized_profit_margin_pct
FROM sales_transactions
GROUP BY discount_tier;

-- 7. SALES CHANNELS PERFORMANCE BREAKDOWN
SELECT 
    sales_channel,
    COUNT(order_id) AS transactions,
    ROUND(SUM(net_revenue), 2) AS channel_revenue,
    ROUND(SUM(profit), 2) AS channel_profit,
    ROUND(AVG(net_revenue), 2) AS avg_order_value
FROM sales_transactions
GROUP BY sales_channel
ORDER BY channel_revenue DESC;
