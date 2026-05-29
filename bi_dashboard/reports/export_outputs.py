from pathlib import Path

from bi_dashboard.dashboard.kpi_cards import compute_kpis, load_kpi_definitions
from bi_dashboard.data.connectors.file_connector import load_file
from bi_dashboard.reports.pdf_generator import build_executive_summary

PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def export_sample_outputs() -> None:
    """Write committed dashboard output examples for the sample dataset."""
    output_dir = PACKAGE_ROOT / "reports" / "generated"
    output_dir.mkdir(parents=True, exist_ok=True)

    frame = load_file(PACKAGE_ROOT / "data" / "sample_sales.csv").sort_values("city")
    definitions = load_kpi_definitions(PACKAGE_ROOT / "data" / "models" / "kpi_definitions.yaml")
    kpis = compute_kpis(frame, definitions)

    frame.to_csv(output_dir / "filtered_data.csv", index=False)
    (output_dir / "bi_executive_summary.pdf").write_bytes(build_executive_summary(frame, kpis))


if __name__ == "__main__":
    export_sample_outputs()
