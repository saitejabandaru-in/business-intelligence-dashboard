from pathlib import Path

from dashboard.kpi_cards import compute_kpis, format_kpi, load_kpi_definitions
from data.connectors.file_connector import load_file


ROOT = Path(__file__).resolve().parents[1]


def test_file_connector_loads_sample_data():
    frame = load_file(ROOT / "data" / "sample_sales.csv")

    assert len(frame) == 12
    assert frame["revenue"].sum() == 220790


def test_compute_kpis_from_yaml_definitions():
    frame = load_file(ROOT / "data" / "sample_sales.csv")
    definitions = load_kpi_definitions(ROOT / "data" / "models" / "kpi_definitions.yaml")

    kpis = compute_kpis(frame, definitions)

    assert kpis["revenue"]["value"] == 220790
    assert round(kpis["conversion_rate"]["value"], 4) == 0.1074
    assert format_kpi(kpis["revenue"]["value"], "currency") == "$220,790"
