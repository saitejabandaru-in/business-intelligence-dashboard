import pandas as pd
from sqlalchemy import create_engine, text


def load_sql(connection_url: str, query: str) -> pd.DataFrame:
    """Run a SQL query and return the result as a DataFrame."""
    engine = create_engine(connection_url)
    with engine.connect() as connection:
        return pd.read_sql_query(text(query), connection)
