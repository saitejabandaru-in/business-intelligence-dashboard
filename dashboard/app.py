from pathlib import Path
import sys

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dashboard.charts import category_mix, conversion_scatter, drilldown_treemap, revenue_by_region, revenue_trend
from dashboard.filters import apply_filters
from dashboard.kpi_cards import compute_kpis, format_kpi, load_kpi_definitions
from data.connectors.file_connector import load_file
from reports.pdf_generator import build_executive_summary

DATA_PATH = ROOT / "data" / "sample_sales.csv"
KPI_PATH = ROOT / "data" / "models" / "kpi_definitions.yaml"


@st.cache_data
def load_dashboard_data(uploaded_file=None) -> pd.DataFrame:
    if uploaded_file is not None:
        return load_file(uploaded_file)
    return load_file(DATA_PATH)


st.set_page_config(page_title="BI & Reporting Dashboard", page_icon="📊", layout="wide")
st.title("BI & Reporting Dashboard")

uploaded = st.sidebar.file_uploader("Upload CSV or Excel data", type=["csv", "xlsx", "xls"])
data = load_dashboard_data(uploaded)

st.sidebar.header("Filters")
regions = st.sidebar.multiselect("Region", sorted(data["region"].unique()))
countries = st.sidebar.multiselect("Country", sorted(data["country"].unique()))
categories = st.sidebar.multiselect("Category", sorted(data["category"].unique()))
date_bounds = st.sidebar.date_input(
    "Date range",
    value=(data["date"].min().date(), data["date"].max().date()),
    min_value=data["date"].min().date(),
    max_value=data["date"].max().date(),
)

date_range = None
if isinstance(date_bounds, tuple) and len(date_bounds) == 2:
    date_range = (pd.Timestamp(date_bounds[0]), pd.Timestamp(date_bounds[1]))

filtered = apply_filters(data, regions, countries, categories, date_range)
kpis = compute_kpis(filtered, load_kpi_definitions(KPI_PATH))

cols = st.columns(len(kpis))
for column, item in zip(cols, kpis.values(), strict=True):
    column.metric(item["label"], format_kpi(item["value"], item["format"]))

left, right = st.columns(2)
left.plotly_chart(revenue_trend(filtered), use_container_width=True)
right.plotly_chart(revenue_by_region(filtered), use_container_width=True)

left, right = st.columns(2)
left.plotly_chart(category_mix(filtered), use_container_width=True)
right.plotly_chart(conversion_scatter(filtered), use_container_width=True)

st.plotly_chart(drilldown_treemap(filtered), use_container_width=True)

with st.expander("Filtered data", expanded=False):
    st.dataframe(filtered, use_container_width=True, hide_index=True)

filtered_csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download filtered data CSV",
    data=filtered_csv,
    file_name="filtered_data.csv",
    mime="text/csv",
)

report_bytes = build_executive_summary(filtered, kpis)
st.download_button(
    "Download executive PDF report",
    data=report_bytes,
    file_name="bi_executive_summary.pdf",
    mime="application/pdf",
)
