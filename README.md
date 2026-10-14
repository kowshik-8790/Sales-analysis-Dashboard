# 📊 Sales Data Analysis Dashboard

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Cleaning-150458?style=for-the-badge&logo=pandas&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![PowerBI](https://img.shields.io/badge/PowerBI-Dashboard-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Excel](https://img.shields.io/badge/Excel-Pivot%20Tables-217346?style=for-the-badge&logo=microsoftexcel&logoColor=white)

---

## 📌 Executive Summary
An end-to-end commercial sales analytics engine and interactive business dashboard developed to analyze **1,250+ transactional records**. Cleaned raw enterprise sales datasets using Python (`Pandas`, `NumPy`) and SQL (`MySQL`), calculated core business KPIs including **$1.49M Net Revenue** and **20.7% Profit Margin**, and built Power BI / web dashboards with dynamic slicers to guide strategic decision-making.

---

## 🚀 Key Business KPIs & Actionable Insights
- **1,250+ Transactions Cleaned & Standardized**: Handled missing values, standardized multi-currency pricing, and structured relational tables for seamless querying.
- **Executive KPI Reporting**:
  - **Total Net Revenue**: `$1,490,000`
  - **Total Operating Profit**: `$308,430`
  - **Realized Profit Margin**: `20.70%`
  - **Total Units Sold**: `9,840 units across 4 global regions`
- **Regional Performance**:
  - **North America**: Leading regional contributor (40% revenue share)
  - **Europe & Asia Pacific**: High-growth territories with fastest-growing recurring orders
- **High-Discount Margin Erosion Engine (≥25% Threshold)**:
  - Discovered that aggressive discount tiers (≥25%) dropped real profit margin from **28.5% down to 8.4%**, providing empirical backing to reset enterprise promotional policies.
- **Top Product Drivers**: Enterprise Laptops and SaaS Enterprise Licenses drove over 35% of total annual operating margin.

---

## 🛠️ Tech Stack & Implementation
| Layer | Technologies & Tools | Key Role |
| :--- | :--- | :--- |
| **Data Cleaning & ETL** | Python (`pandas`, `numpy`), Excel | Data standardization, missing-value imputation, outlier removal |
| **Relational Database** | MySQL 8.0 / MariaDB | Relational schema (`schema.sql`), indexing, aggregated business queries (`analysis_queries.sql`) |
| **Business Intelligence** | Power BI Desktop, DAX | Multi-table data model, star schema, DAX measures (`powerbi_dashboard_guide.md`) |
| **Web Dashboard** | HTML5, CSS3, JavaScript, Chart.js | Standalone interactive dashboard with real-time slicers & charts |

---

## 📂 Repository Structure
```
sales-data-analysis-dashboard/
├── schema.sql                     # MySQL table creation & indexes
├── analysis_queries.sql           # SQL KPI queries (Revenue, Margins, Regional, Erosion)
├── powerbi_dashboard_guide.md     # Power BI DAX calculations & layout blueprint
├── generate_data.py               # Python dataset generator & ETL processing
├── sales_data.csv                 # Cleaned dataset (1,250 transactional rows)
├── sales_data.json                # JSON dataset powering interactive web charts
├── index.html                     # Interactive dashboard user interface
├── app.js                         # Dynamic slicers & Chart.js rendering logic
└── README.md                      # Comprehensive documentation
```

---

## 💻 How to Run

### 1. Python ETL & Data Generation
```bash
# Optional: re-generate or verify dataset
python generate_data.py
```

### 2. SQL Schema & Analytics
Import `schema.sql` and run `analysis_queries.sql` in MySQL Workbench or terminal:
```sql
SOURCE schema.sql;
SOURCE analysis_queries.sql;
```

### 3. Interactive Web Dashboard
Open `index.html` directly in any modern browser (or serve locally):
```bash
python -m http.server 8000
```
Navigate to `http://localhost:8000`.

---

## 👤 Author
- **Kasanaboina Kowshik**
- **Education:** B.Tech in Computer Science (Artificial Intelligence), Parul University
- **Email:** [kasanaboinakowshik@gmail.com](mailto:kasanaboinakowshik@gmail.com)
- **Phone:** +91 8790211519
