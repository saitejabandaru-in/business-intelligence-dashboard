# 📊 Power BI Dashboard Integration

This directory contains enterprise-grade **Power BI integration scripts** that enable you to build a mirror image of the Python Streamlit dashboard using **Microsoft Power BI Desktop**.

---

## 🗂️ Resources

* 📜 **[power_query_etl.m](power_query_etl.m):** Power Query (M-code) to import, normalize, and cleanse the sample dataset.
* 📈 **[dax_measures.dax](dax_measures.dax):** Production DAX formulas defining key business KPIs, conversion rates, margins, and advanced time-intelligence metrics.

---

## 🚀 Setup Instructions

### Step 1: Import Data (Power Query)
1. Open **Power BI Desktop**.
2. Click **Get Data** -> **Blank Query**.
3. In the Home tab of the Power Query Editor, click **Advanced Editor**.
4. Copy the entire contents of `power_query_etl.m` and paste them over the blank query.
5. In the script, locate the path to the CSV file:
   ```powerquery
   File.Contents("C:\path\to\your\sample_sales.csv")
   ```
   Modify this path to match the absolute location of `sample_sales.csv` on your local machine.
6. Click **Done**, rename the table to `sample_sales`, and click **Close & Apply**.

---

### Step 2: Set Up the Calendar Table
For time-intelligence measures (like Month-over-Month growth and Year-to-Date revenue) to work correctly, you need a contiguous Calendar table:
1. In the **Report** or **Data** view, navigate to the **Modeling** tab.
2. Click **New Table**.
3. Copy and paste the DAX code for the `Calendar` table from `dax_measures.dax`:
   ```dax
   Calendar = ...
   ```
4. Press Enter. This dynamically generates a date table bounded by the minimum and maximum dates in your dataset.
5. Navigate to the **Model** view and drag the `date` field from the `Calendar` table to the `date` field in `sample_sales` to establish a **1:Many (1:*)** relationship.

---

### Step 3: Implement KPIs (DAX Measures)
1. In the **Modeling** tab, click **New Measure**.
2. Copy and paste the measures from `dax_measures.dax` one by one (e.g., `Total Revenue`, `Conversion Rate`, `Profit Margin`, `MoM Revenue Growth`).
3. Set the appropriate formatting for each measure:
   - **Conversion Rate & Profit Margin:** Format as **Percentage (%)** with `1` decimal place.
   - **Total Revenue & Total Profit:** Format as **Currency ($)** with `0` decimal places.
   - **Active Users & Orders:** Format as **Whole Number** with comma separators.

---

### Step 4: Design the Report Layout
To recreate the visual elegance of the Streamlit dashboard:
1. **KPI Cards:** Use the **Multi-row Card** or standard **Card** visuals to showcase `Total Revenue`, `Conversion Rate`, `Total Active Users`, and `Profit Margin`.
2. **Revenue Trend:** Use a **Line Chart** with `Calendar[Year-Month]` on the X-axis and `Total Revenue` on the Y-axis.
3. **Revenue by Region:** Use a **Clustered Bar Chart** with `sample_sales[region]` on the Axis and `Total Revenue` on the Value.
4. **Category Mix:** Use a **Donut Chart** with `sample_sales[category]` on the Legend and `Total Revenue` on the Value.
5. **Drill-down Analytics:** Use a **Matrix** or **Treemap** visual with the hierarchy: `region` -> `country` -> `city` -> `store` and `Total Revenue` as the values.
