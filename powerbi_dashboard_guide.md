# 📈 Power BI Sales Performance Dashboard Blueprint

**Author:** Kasanaboina Kowshik  
**Email:** kasanaboinakowshik@gmail.com  
**Tools:** Power BI Desktop, DAX, Power Query, Excel  

---

## 🏗️ 1. Data Model & Star Schema Architecture
The dashboard connects to `sales_data.csv` (or directly to MySQL `sales_analytics_db.sales_transactions`).
- **Fact Table:** `Fact_Sales` (`order_id`, `order_date`, `region`, `category`, `product`, `quantity`, `unit_price`, `gross_sales`, `discount_amount`, `net_revenue`, `total_cost`, `profit`)
- **Dimension 1 (Calendar):** Auto-generated Date Dimension via `CALENDARAUTO()`
- **Dimension 2 (Products):** Category and Product hierarchies
- **Dimension 3 (Geography):** Sales Regions (North America, Europe, Asia Pacific, Latin America)

---

## 🧮 2. Key DAX Measures
Create a dedicated `_Measures` table in Power BI and add the following DAX calculations:

```dax
// 1. Total Net Revenue
Total Revenue = SUM(Fact_Sales[net_revenue])

// 2. Total Gross Sales
Total Gross Sales = SUM(Fact_Sales[gross_sales])

// 3. Total Profit
Total Profit = SUM(Fact_Sales[profit])

// 4. Profit Margin Percentage
Profit Margin % = 
DIVIDE([Total Profit], [Total Revenue], 0)

// 5. Total Units Sold
Total Quantity Sold = SUM(Fact_Sales[quantity])

// 6. Average Order Value (AOV)
Average Order Value = 
DIVIDE([Total Revenue], DISTINCTCOUNT(Fact_Sales[order_id]), 0)

// 7. Discount Impact %
Overall Discount Rate % = 
DIVIDE(SUM(Fact_Sales[discount_amount]), [Total Gross Sales], 0)

// 8. High-Discount Margin Erosion Flag Measure
High Discount Revenue Loss = 
CALCULATE(
    [Total Revenue],
    Fact_Sales[discount_pct] >= 0.25
)
```

---

## 📊 3. Dashboard Visuals & Canvas Layout
1. **Top KPI Header Cards:**
   - Card 1: `Total Revenue` formatted as `$1.49M`
   - Card 2: `Total Profit` formatted as `$308.4K`
   - Card 3: `Profit Margin %` with conditional KPI color (Green if > 20%, Red if < 15%)
   - Card 4: `Total Orders` (1,250 transactions)

2. **Trend Analysis (Area / Line Chart):**
   - X-Axis: `Order Date (Month)`
   - Y-Axis: `Total Revenue` and `Total Profit`
   - Tooltip: `Profit Margin %`

3. **Regional Breakdown (Donut & Map Chart):**
   - Legend: `Region`
   - Values: `Total Revenue`
   - Percentage of total slice breakdown

4. **Product Category & Top 5 Matrix (Clustered Bar Chart):**
   - Axis: `Product`
   - Values: `Total Revenue` sorted descending
   - Drill-up/Drill-down: `Category` -> `Product`

5. **Discount Erosion Scatter / Bar:**
   - Grouping orders with `< 25%` vs `>= 25%` discount to demonstrate profit decay from 28.5% down to 8.4%.

6. **Interactive Slicers:**
   - Date Range slider
   - Region dropdown (Multi-select)
   - Product Category tiles
   - Sales Channel dropdown
