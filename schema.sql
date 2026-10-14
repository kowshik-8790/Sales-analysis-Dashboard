-- ====================================================================
-- Sales Performance & Analytics Database Schema
-- Author: Kasanaboina Kowshik (kasanaboinakowshik@gmail.com)
-- Database: MySQL 8.0+ / MariaDB / Compatible RDBMS
-- ====================================================================

CREATE DATABASE IF NOT EXISTS sales_analytics_db;
USE sales_analytics_db;

-- Drop table if it exists
DROP TABLE IF EXISTS sales_transactions;

-- Create transactional sales table
CREATE TABLE sales_transactions (
    order_id VARCHAR(20) PRIMARY KEY,
    order_date DATE NOT NULL,
    region VARCHAR(50) NOT NULL,
    category VARCHAR(50) NOT NULL,
    product VARCHAR(100) NOT NULL,
    sales_channel VARCHAR(50) NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    gross_sales DECIMAL(12, 2) NOT NULL,
    discount_pct DECIMAL(5, 4) NOT NULL DEFAULT 0.0000,
    discount_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    net_revenue DECIMAL(12, 2) NOT NULL,
    total_cost DECIMAL(12, 2) NOT NULL,
    profit DECIMAL(12, 2) NOT NULL,
    profit_margin DECIMAL(6, 2) NOT NULL,
    high_discount_erosion BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_order_date (order_date),
    INDEX idx_region (region),
    INDEX idx_category (category),
    INDEX idx_product (product)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Sample query to load CSV into MySQL:
-- LOAD DATA INFILE 'sales_data.csv'
-- INTO TABLE sales_transactions
-- FIELDS TERMINATED BY ','
-- ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS;
