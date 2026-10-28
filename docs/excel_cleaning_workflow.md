# Excel Data Cleaning & Processing Workflow Guide

This guide details the end-to-end data processing workflow using **Microsoft Excel** and **Power Query (Get & Transform)** for enterprise sales transactions.

---

## 1. Power Query ETL Pipeline Steps

When opening the raw transaction file (`data/raw/sales_raw_dataset.xlsx`) in Excel:

1. **Import via Power Query**:
   - Navigate to `Data` &rarr; `Get Data` &rarr; `From File` &rarr; `From Workbook`.
   - Select `Raw_Transactions` sheet &rarr; Click **Transform Data**.

2. **Deduplication**:
   - Select column `Transaction_ID`.
   - Right-click &rarr; **Remove Duplicates**.

3. **Text Cleaning & Casing Normalization**:
   - Select `Customer_Name`, `City`, `State`, `Region`, `Product_Name`.
   - Right-click &rarr; `Transform` &rarr; `Trim` (removes leading/trailing whitespace).
   - Select `Segment` &rarr; `Transform` &rarr; `Capitalize Each Word` (`Consumer`, `Corporate`, `Home Office`).

4. **Mixed Date Type Parsing**:
   - Select `Order_Date` and `Ship_Date`.
   - Click `Change Type` &rarr; `Using Locale...` &rarr; Data Type: `Date` &rarr; Locale: `English (United States)`.

5. **Currency String Cleaning**:
   - For `Sales` column with string values like `"$1,249.99"`:
   - Click `Transform` &rarr; `Replace Values` &rarr; Replace `$` with empty string.
   - Click `Change Type` &rarr; `Currency` / `Decimal Number`.

6. **Missing Value Imputation**:
   - Right-click `Postal_Code` &rarr; `Replace Values` &rarr; Replace `null` with `"00000"`.
   - Right-click `Ship_Mode` &rarr; `Replace Values` &rarr; Replace `null` with `"Standard Class"`.

7. **Feature Engineering via Custom Columns**:
   - **Delivery Days**: Add Custom Column `[Ship_Date] - [Order_Date]` &rarr; Transform to Total Days.
   - **Profit Margin %**: Add Custom Column `if [Sales] > 0 then ([Profit] / [Sales]) * 100 else 0`.
   - **High Value Tag**: Add Conditional Column: If `[Sales] >= 1000` then `"High Value"` else `"Standard"`.

---

## 2. Excel Formulas & Lookup Modeling

| Objective | Excel Formula |
| :--- | :--- |
| **Clean Whitespace** | `=TRIM(CLEAN(A2))` |
| **Title Case Normalization** | `=PROPER(B2)` |
| **Delivery Lead Time** | `=DATEDIF(Order_Date, Ship_Date, "d")` |
| **Profit Margin %** | `=IFERROR(Profit / Sales, 0)` *(formatted as Percentage)* |
| **Customer Segment Lookup** | `=XLOOKUP(C2, dim_customers[Customer_ID], dim_customers[Segment], "Unknown")` |
| **Multi-Condition Revenue** | `=SUMIFS(Sales_Range, Region_Range, "West", Category_Range, "Technology")` |

---

## 3. Pivot Tables & Executive Reporting in Excel

1. **Category Summary Pivot**:
   - Rows: `Category`, `Sub_Category`
   - Values: `Sum of Sales` (Format: `$#,##0`), `Sum of Profit` (Format: `$#,##0`), `Average Profit Margin %`
2. **Regional Breakdown Pivot**:
   - Rows: `Region`
   - Columns: `Year`
   - Values: `Sum of Sales`
3. **Conditional Formatting**:
   - Apply 3-Color Scale to `Profit Margin %` (Green = &ge;20%, Yellow = 15%, Red = &le;5%).
   - Apply Data Bars to `Total Revenue` for instant visual comparison.
