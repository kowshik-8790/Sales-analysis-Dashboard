# Sales Data Analysis Dashboard - Complete Setup Guide

This guide walks through configuring the project across **Python**, **MySQL**, **Power BI Desktop**, and **VS Code**.

---

## 1. Environment Setup (VS Code & Python)

1. **Open Workspace in VS Code**:
   - Open VS Code.
   - Click `File` &rarr; `Open Folder...` &rarr; Select:
     `C:\Users\kasan\.gemini\antigravity\scratch\sales-data-analysis-dashboard`

2. **Verify Python Environment**:
   ```bash
   python --version
   pip install -r requirements.txt
   ```

3. **Run Data Generation and Cleaning Pipeline**:
   ```bash
   # Step 1: Generate Raw Data with anomalies
   python src/generate_raw_data.py

   # Step 2: Clean, sanitize, and create Star-Schema datasets
   python src/etl_pipeline.py

   # Step 3: Generate styled multi-sheet Excel Executive Workbook
   python src/generate_excel_report.py

   # Step 4: Sync to SQL database and run sample analytical KPIs
   python src/db_connector.py
   ```

---

## 2. MySQL Database Setup

1. **Launch MySQL Server**:
   Ensure MySQL 8.0+ service is active (`net start mysql` or via MySQL Workbench).

2. **Execute DDL Schema**:
   Open MySQL Workbench or your terminal:
   ```bash
   mysql -u root -p < sql/01_schema_setup.sql
   ```

3. **Populate MySQL Tables**:
   Run the Python loader with `--mysql` flag:
   ```bash
   python src/db_connector.py --mysql
   ```
   *(Ensure environment variable `MYSQL_URI` is set if different from default `root:password@localhost:3306/sales_analytics`)*.

4. **Run Analytical Queries**:
   - Execute `sql/02_data_cleaning_transform.sql` to instantiate reporting views.
   - Run `sql/03_kpi_analysis.sql` for MoM/YoY growth and margin trend analyses.
   - Run `sql/04_top_products_regional.sql` for SKU rankings and shipping SLAs.
   - Run `sql/05_rfm_customer_segments.sql` to generate RFM customer scorecards.

---

## 3. Power BI Desktop Connection & Dashboard Build

1. **Open Power BI Desktop**.
2. **Import Data**:
   - Option A (**Direct MySQL Connection**):
     - Click `Get Data` &rarr; `MySQL Database` &rarr; Server: `localhost:3306` &rarr; Database: `sales_analytics`.
     - Select tables: `dim_customers`, `dim_products`, `dim_regions`, `dim_date`, `fact_sales`.
   - Option B (**Clean CSV Import**):
     - Click `Get Data` &rarr; `Text/CSV` &rarr; Load each file from `data/processed/`.
3. **Verify Data Model Relationships**:
   - Navigate to the **Model View** tab.
   - Confirm Star-Schema links match `powerbi/data_model_architecture.md`.
4. **Load Custom DAX Measures**:
   - Open `powerbi/dax_measures.dax`.
   - Create a dedicated measure table `_Measures` and copy in the DAX formulas.
5. **Apply Executive Theme**:
   - Click `View` tab &rarr; Themes dropdown &rarr; `Browse for themes...` &rarr; Select `powerbi/powerbi_theme.json`.
6. **Design Visuals**:
   - Follow the layout specifications in `powerbi/dashboard_visual_spec.md`.

---

## 4. Viewing the Instant Interactive Browser Preview

Open `dashboard_preview/index.html` in any web browser to immediately interact with the executive dashboard, charts, KPI cards, and dynamic filters without requiring Power BI Desktop!
