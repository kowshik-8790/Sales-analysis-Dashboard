# Power BI Dashboard Visual Design Specification

## Overview & Executive Canvas Specs
- **Canvas Size**: 16:9 Widescreen (1920 x 1080 px)
- **Primary Color Scheme**: Modern Executive Corporate Palette
  - **Primary Navy**: `#1E3A8A`
  - **Teal / Secondary**: `#0D9488`
  - **Accent Amber**: `#F59E0B`
  - **Profit Margin Green**: `#10B981`
  - **Alert / Loss Red**: `#EF4444`
  - **Background**: `#F8FAFC`
  - **Card Surface**: `#FFFFFF` with 1px border `#E2E8F0`

---

## Page 1: Executive Sales Overview (Strategic C-Suite View)

### Top Navigation Bar & Global Slicers
- **Left**: Corporate Logo + Dashboard Title `"Sales Performance Executive Dashboard"`
- **Right Filter Panel (Slicers)**:
  - Date Range Slider (`dim_date[date_id]`)
  - Region Dropdown (`dim_customers[region]`)
  - Category Dropdown (`dim_products[category]`)
  - Customer Segment (`dim_customers[segment]`)

### Row 1: High-Impact KPI Cards (Top 5 Cards)
1. **Total Revenue**: `$28.80M` | Subtext: `+12.4% YoY` (Green arrow)
2. **Total Profit**: `$5.16M` | Subtext: `Realized Net Margin: 17.92%`
3. **Total Orders**: `7,994` | Subtext: `Avg Order Value: $3,602.46`
4. **Units Sold**: `66,278` | Subtext: `Avg 8.3 units/order`
5. **Avg Fulfillment SLA**: `7.3 Days` | Subtext: `89.2% on-time delivery`

### Row 2: Trend & Category Breakdown (Main Charts)
- **Left (60% Width) - Line and Clustered Column Chart**:
  - *X-Axis*: `dim_date[month_year]` (Sorted chronologically)
  - *Column Y-Axis*: `[Total Revenue]` (Bars colored `#1E3A8A`)
  - *Line Y-Axis*: `[Profit Margin %]` (Accent line colored `#10B981` with data dots)
  - *Tooltip*: Revenue, Profit, Units, MoM Growth %
- **Right (40% Width) - Donut Chart & Category Contribution**:
  - *Legend*: `dim_products[category]` (Technology, Furniture, Office Supplies)
  - *Values*: `[Total Revenue]`
  - *Data Labels*: Category Name + Percent of Total

### Row 3: Regional Distribution & Top SKUs
- **Left (50% Width) - Clustered Bar Chart (Regional Profitability)**:
  - *Y-Axis*: `dim_customers[region]`
  - *X-Axis*: `[Total Revenue]` and `[Total Profit]`
  - *Conditional Formatting*: Color bars by `[Margin Health Status KPI]`
- **Right (50% Width) - Top 5 Products Table**:
  - *Columns*: Product Name, Category, Units Sold, Revenue, Profit Margin % (Data bar)

---

## Page 2: Product & Category Deep-Dive

### Key Visuals:
1. **Category & Sub-Category Treemap**:
   - *Group*: Category > Sub-Category
   - *Size*: `[Total Revenue]`
   - *Color Saturation*: `[Profit Margin %]` (Instantly spots high-revenue / low-margin categories like Tables)
2. **Scatter Plot (Margin vs. Discount Sensitivity)**:
   - *X-Axis*: `Average Discount %` (0% to 60%)
   - *Y-Axis*: `Profit Margin %` (-20% to 50%)
   - *Bubble Size*: `[Total Revenue]`
   - *Legend*: `dim_products[category]`
   - *Insight*: Visualizes steep margin erosion when discounts exceed 20%.
3. **Product Performance Matrix Table**:
   - Interactive search bar and Top N product parameter slider.
   - Column-level conditional formatting for Margin % (Green > 20%, Red < 10%).

---

## Page 3: Regional & Shipping Performance

### Key Visuals:
1. **Geographic Map (Shape / Azure Map)**:
   - *Location*: `dim_customers[state]`
   - *Bubble Size*: `[Total Revenue]`
   - *Color Heatmap*: `[Total Profit]`
2. **Shipping Mode Efficiency Gauge & Bar**:
   - Revenue and cost split across Standard Class, Second Class, First Class, Same Day.
   - Average Delivery Days vs. Delivery SLA target (Target: 5 days).
3. **State-Level Profitability Waterfall**:
   - Visualizing highest-margin states (Washington, California, New York) vs compressed margin states (Texas).

---

## Page 4: Customer Segmentation & RFM Value

### Key Visuals:
1. **RFM Segment Matrix (100% Stacked Bar)**:
   - Segments: Champions, Loyal Customers, At Risk, Hibernating, Standard.
   - Customer distribution and spend per segment.
2. **Customer Segment KPI Cards**:
   - Revenue per Corporate Customer vs Consumer vs Home Office.
3. **Repeat Purchase Cohort Analysis**:
   - Customer retention and order frequency distribution.
