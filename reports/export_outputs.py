from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dashboard.kpi_cards import compute_kpis, load_kpi_definitions
from data.connectors.file_connector import load_file
from reports.pdf_generator import build_executive_summary


def export_sample_outputs() -> None:
    """Write committed dashboard output examples for the sample dataset."""
    output_dir = ROOT / "reports" / "generated"
    output_dir.mkdir(parents=True, exist_ok=True)

    frame = load_file(ROOT / "data" / "sample_sales.csv").sort_values("city")
    definitions = load_kpi_definitions(ROOT / "data" / "models" / "kpi_definitions.yaml")
    kpis = compute_kpis(frame, definitions)

    frame.to_csv(output_dir / "filtered_data.csv", index=False)
    (output_dir / "bi_executive_summary.pdf").write_bytes(build_executive_summary(frame, kpis))


if __name__ == "__main__":
    export_sample_outputs()
