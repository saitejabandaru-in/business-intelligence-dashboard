import pandas as pd


def apply_filters(
    frame: pd.DataFrame,
    regions: list[str] | None = None,
    countries: list[str] | None = None,
    categories: list[str] | None = None,
    date_range: tuple[pd.Timestamp, pd.Timestamp] | None = None,
) -> pd.DataFrame:
    filtered = frame.copy()
    if regions:
        filtered = filtered[filtered["region"].isin(regions)]
    if countries:
        filtered = filtered[filtered["country"].isin(countries)]
    if categories:
        filtered = filtered[filtered["category"].isin(categories)]
    if date_range:
        start, end = date_range
        filtered = filtered[(filtered["date"] >= start) & (filtered["date"] <= end)]
    return filtered
