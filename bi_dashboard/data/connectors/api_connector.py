from collections.abc import Mapping

import pandas as pd
import requests


def load_api(url: str, params: Mapping[str, str] | None = None, records_path: str | None = None) -> pd.DataFrame:
    """Fetch JSON records from a REST endpoint."""
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()

    if records_path:
        for key in records_path.split("."):
            payload = payload[key]

    return pd.DataFrame(payload)
