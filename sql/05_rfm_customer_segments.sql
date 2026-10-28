-- ============================================================================
-- 05_rfm_customer_segments.sql
-- Customer RFM (Recency, Frequency, Monetary) Value Segmentation
-- ============================================================================

USE sales_analytics;

WITH customer_rfm_raw AS (
    SELECT 
        c.customer_id,
        c.customer_name,
        c.segment,
        c.region,
        -- Recency: Days since most recent purchase (relative to max dataset date)
        DATEDIFF(
            (SELECT MAX(order_date) FROM fact_sales), 
            MAX(f.order_date)
        ) AS recency_days,
        -- Frequency: Count of distinct orders
        COUNT(DISTINCT f.order_id) AS frequency_orders,
        -- Monetary: Total spend
        ROUND(SUM(f.sales), 2) AS monetary_value
    FROM dim_customers c
    JOIN fact_sales f ON c.customer_id = f.customer_id
    GROUP BY c.customer_id, c.customer_name, c.segment, c.region
),
rfm_scores AS (
    SELECT 
        customer_id,
        customer_name,
        segment,
        region,
        recency_days,
        frequency_orders,
        monetary_value,
        -- Rank recency (lower days = higher score 4 to 1)
        NTILE(4) OVER (ORDER BY recency_days DESC) AS r_score,
        -- Rank frequency (higher orders = higher score 1 to 4)
        NTILE(4) OVER (ORDER BY frequency_orders ASC) AS f_score,
        -- Rank monetary (higher sales = higher score 1 to 4)
        NTILE(4) OVER (ORDER BY monetary_value ASC) AS m_score
    FROM customer_rfm_raw
)
SELECT 
    customer_id,
    customer_name,
    segment,
    region,
    recency_days,
    frequency_orders,
    monetary_value,
    r_score,
    f_score,
    m_score,
    CONCAT(r_score, f_score, m_score) AS rfm_combined,
    CASE 
        WHEN r_score >= 3 AND f_score >= 3 AND m_score >= 3 THEN 'Champion / VIP'
        WHEN f_score >= 3 AND m_score >= 2 THEN 'Loyal Customer'
        WHEN r_score >= 3 AND f_score <= 2 THEN 'Recent High-Potential'
        WHEN r_score <= 2 AND f_score >= 3 THEN 'At Risk (Lapsing High-Value)'
        WHEN r_score <= 2 AND f_score <= 2 AND m_score >= 3 THEN 'Hibernating Big Spender'
        ELSE 'Standard / Occasional'
    END AS customer_tier
FROM rfm_scores
ORDER BY monetary_value DESC;
