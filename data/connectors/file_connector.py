from pathlib import Path

import pandas as pd


def load_file(path: str | Path) -> pd.DataFrame:
    """Load CSV or Excel data into a normalized DataFrame."""
    source = Path(path)
    if not source.exists():
        raise FileNotFoundError(f"Data file not found: {source}")

    if source.suffix.lower() == ".csv":
        frame = pd.read_csv(source)
    elif source.suffix.lower() in {".xlsx", ".xls"}:
        frame = pd.read_excel(source)
    else:
        raise ValueError("Only CSV and Excel files are supported.")

    return normalize_business_data(frame)


def normalize_business_data(frame: pd.DataFrame) -> pd.DataFrame:
    required = {
        "date",
        "region",
        "country",
        "city",
        "store",
        "category",
        "revenue",
        "orders",
        "active_users",
        "conversions",
        "sessions",
        "profit",
    }
    missing = required.difference(frame.columns)
    if missing:
        missing_list = ", ".join(sorted(missing))
        raise ValueError(f"Missing required columns: {missing_list}")

    cleaned = frame.copy()
    cleaned["date"] = pd.to_datetime(cleaned["date"])
    numeric_columns = ["revenue", "orders", "active_users", "conversions", "sessions", "profit"]
    cleaned[numeric_columns] = cleaned[numeric_columns].apply(pd.to_numeric, errors="coerce").fillna(0)
    return cleaned
