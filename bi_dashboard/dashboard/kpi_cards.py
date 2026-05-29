from pathlib import Path

import pandas as pd

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover - exercised in minimal runtimes
    yaml = None


def load_kpi_definitions(path: str | Path) -> dict:
    config_text = Path(path).read_text(encoding="utf-8")
    if yaml is not None:
        return yaml.safe_load(config_text)["kpis"]
    return _parse_simple_kpi_yaml(config_text)


def compute_kpis(frame: pd.DataFrame, definitions: dict) -> dict:
    results = {}
    for key, definition in definitions.items():
        if definition["aggregation"] == "sum":
            value = frame[definition["column"]].sum()
        elif definition["aggregation"] == "ratio":
            denominator = frame[definition["denominator"]].sum()
            value = 0 if denominator == 0 else frame[definition["numerator"]].sum() / denominator
        else:
            raise ValueError(f"Unsupported KPI aggregation: {definition['aggregation']}")

        results[key] = {
            "label": definition["label"],
            "value": value,
            "format": definition.get("format", "number"),
        }
    return results


def format_kpi(value: float, style: str) -> str:
    if style == "currency":
        return f"${value:,.0f}"
    if style == "percent":
        return f"{value:.1%}"
    if style == "integer":
        return f"{value:,.0f}"
    return f"{value:,.2f}"


def _parse_simple_kpi_yaml(config_text: str) -> dict:
    """Parse the repository's simple KPI YAML without requiring PyYAML."""
    kpis: dict[str, dict[str, str]] = {}
    current_key = None
    for raw_line in config_text.splitlines():
        line = raw_line.rstrip()
        if not line.strip() or line.strip() == "kpis:":
            continue
        if line.startswith("  ") and line.endswith(":") and not line.startswith("    "):
            current_key = line.strip().removesuffix(":")
            kpis[current_key] = {}
            continue
        if current_key and line.startswith("    ") and ":" in line:
            key, value = line.strip().split(":", 1)
            kpis[current_key][key] = value.strip()
    return kpis
