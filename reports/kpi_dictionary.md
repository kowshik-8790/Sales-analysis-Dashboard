# Key Performance Indicators (KPI) Business Dictionary

| KPI Name | Business Definition | Mathematical Formula / DAX | Target Benchmark | Business Action When Off-Track |
| :--- | :--- | :--- | :--- | :--- |
| **Gross Revenue** | Total monetary value of completed sales after applying promotional discounts. | `SUM(Sales)` | Growth &ge; 10% YoY | Audit sales pipeline, adjust marketing mix, assess lead generation channels. |
| **Total Profit** | Realized net income remaining after deducting cost of goods sold (COGS). | `SUM(Profit)` | Growth &ge; 12% YoY | Review pricing strategy, vendor unit costs, and promotional expenditure. |
| **Profit Margin %** | Proportion of revenue that translates into profit. | `(Total Profit / Total Revenue) * 100` | &ge; 20.0% | Restrict discount bands, eliminate loss-making SKUs, promote high-margin bundles. |
| **Average Order Value (AOV)** | Average dollar spend generated per distinct customer order. | `Total Revenue / Total Orders` | &ge; \$3,500 | Implement minimum order thresholds for free shipping; introduce upsell/cross-sell prompts. |
| **MoM Revenue Growth %** | Rate of revenue expansion or contraction relative to the previous month. | `(Rev_Curr - Rev_Prev) / Rev_Prev * 100` | &ge; 2.5% MoM | Run seasonal flash campaigns, re-engage lapsed customer segments. |
| **Average Delivery Lead Time** | Average elapsed calendar days from order placement to customer receipt. | `AVERAGE(Ship_Date - Order_Date)` | &le; 5.0 Days | Optimize carrier contracts, reallocate safety stock across regional fulfillment nodes. |
| **Discount Rate %** | Average percentage markdown granted off base MSRP list price. | `AVERAGE(Discount)` | &le; 18.0% | Enforce approval matrices for discounts exceeding 15%; incentivize reps on margin, not just revenue. |
