-- ============================================================================
-- 01_schema_setup.sql
-- Star Schema Database Architecture for Sales Analytics
-- Compatible with MySQL 8.0+
-- ============================================================================

CREATE DATABASE IF NOT EXISTS sales_analytics
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE sales_analytics;

-- Drop tables in order of dependency if re-running
DROP TABLE IF EXISTS fact_sales;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS dim_regions;
DROP TABLE IF EXISTS dim_products;
DROP TABLE IF EXISTS dim_customers;

-- 1. Dimension: Customers
CREATE TABLE dim_customers (
    customer_id     VARCHAR(30) PRIMARY KEY,
    customer_name   VARCHAR(100) NOT NULL,
    segment         VARCHAR(50)  NOT NULL,
    city            VARCHAR(100) NOT NULL,
    state           VARCHAR(100) NOT NULL,
    region          VARCHAR(50)  NOT NULL,
    postal_code     VARCHAR(20)  DEFAULT '00000',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_cust_region (region),
    INDEX idx_cust_segment (segment)
) ENGINE=InnoDB;

-- 2. Dimension: Products
CREATE TABLE dim_products (
    product_id      VARCHAR(30) PRIMARY KEY,
    product_name    VARCHAR(200) NOT NULL,
    category        VARCHAR(50)  NOT NULL,
    sub_category    VARCHAR(50)  NOT NULL,
    unit_cost       DECIMAL(10, 2) NOT NULL,
    unit_price      DECIMAL(10, 2) NOT NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_prod_category (category),
    INDEX idx_prod_subcategory (sub_category)
) ENGINE=InnoDB;

-- 3. Dimension: Regions / Geography
CREATE TABLE dim_regions (
    region_id       VARCHAR(20) PRIMARY KEY,
    region          VARCHAR(50)  NOT NULL,
    state           VARCHAR(100) NOT NULL,
    city            VARCHAR(100) NOT NULL,
    INDEX idx_region_state (region, state)
) ENGINE=InnoDB;

-- 4. Dimension: Calendar Date
CREATE TABLE dim_date (
    date_id         DATE PRIMARY KEY,
    year            INT NOT NULL,
    quarter         VARCHAR(5) NOT NULL,
    month           INT NOT NULL,
    month_name      VARCHAR(20) NOT NULL,
    month_year      VARCHAR(20) NOT NULL,
    day             INT NOT NULL,
    day_name        VARCHAR(20) NOT NULL,
    is_weekend      TINYINT(1) DEFAULT 0,
    INDEX idx_date_year_month (year, month)
) ENGINE=InnoDB;

-- 5. Fact: Sales Transactions
CREATE TABLE fact_sales (
    transaction_id      VARCHAR(30) PRIMARY KEY,
    order_id            VARCHAR(30) NOT NULL,
    order_date          DATE NOT NULL,
    ship_date           DATE NOT NULL,
    customer_id         VARCHAR(30) NOT NULL,
    product_id          VARCHAR(30) NOT NULL,
    ship_mode           VARCHAR(50) NOT NULL DEFAULT 'Standard Class',
    quantity            INT NOT NULL CHECK (quantity > 0),
    unit_cost           DECIMAL(10, 2) NOT NULL,
    unit_price          DECIMAL(10, 2) NOT NULL,
    discount            DECIMAL(5, 2) NOT NULL DEFAULT 0.00,
    sales               DECIMAL(12, 2) NOT NULL,
    profit              DECIMAL(12, 2) NOT NULL,
    profit_margin_pct   DECIMAL(6, 2) NOT NULL,
    delivery_days       INT NOT NULL DEFAULT 0,
    discount_band       VARCHAR(30) DEFAULT 'No Discount (0%)',
    high_value_order    TINYINT(1) DEFAULT 0,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Key constraints
    CONSTRAINT fk_sales_customer FOREIGN KEY (customer_id) 
        REFERENCES dim_customers(customer_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_sales_product FOREIGN KEY (product_id) 
        REFERENCES dim_products(product_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_sales_order_date FOREIGN KEY (order_date) 
        REFERENCES dim_date(date_id) ON DELETE RESTRICT ON UPDATE CASCADE,
        
    -- Analytical Indexes
    INDEX idx_sales_order (order_id),
    INDEX idx_sales_order_date (order_date),
    INDEX idx_sales_customer (customer_id),
    INDEX idx_sales_product (product_id),
    INDEX idx_sales_ship_mode (ship_mode)
) ENGINE=InnoDB;
