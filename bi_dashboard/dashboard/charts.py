import pandas as pd
import plotly.express as px


def revenue_trend(frame: pd.DataFrame):
    monthly = (
        frame.assign(month=frame["date"].dt.to_period("M").dt.to_timestamp())
        .groupby("month", as_index=False)["revenue"]
        .sum()
    )
    return px.line(monthly, x="month", y="revenue", markers=True, title="Revenue Trend")


def revenue_by_region(frame: pd.DataFrame):
    grouped = frame.groupby("region", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
    return px.bar(grouped, x="region", y="revenue", color="region", title="Revenue by Region")


def category_mix(frame: pd.DataFrame):
    grouped = frame.groupby("category", as_index=False)["revenue"].sum()
    return px.pie(grouped, names="category", values="revenue", title="Category Mix", hole=0.42)


def drilldown_treemap(frame: pd.DataFrame):
    return px.treemap(
        frame,
        path=["region", "country", "city", "store"],
        values="revenue",
        color="profit",
        title="Region to Store Drill-Down",
    )


def conversion_scatter(frame: pd.DataFrame):
    plotted = frame.assign(conversion_rate=frame["conversions"] / frame["sessions"].replace(0, pd.NA))
    return px.scatter(
        plotted,
        x="active_users",
        y="conversion_rate",
        size="revenue",
        color="category",
        hover_name="store",
        title="Users vs Conversion Rate",
    )
