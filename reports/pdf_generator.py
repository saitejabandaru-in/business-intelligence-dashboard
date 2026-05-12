from io import BytesIO

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from dashboard.kpi_cards import format_kpi


def build_executive_summary(frame: pd.DataFrame, kpis: dict) -> bytes:
    """Create a compact PDF executive summary and return it as bytes."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, title="BI Executive Summary")
    styles = getSampleStyleSheet()

    story = [
        Paragraph("BI Executive Summary", styles["Title"]),
        Paragraph("KPI snapshot generated from the current dashboard filters.", styles["BodyText"]),
        Spacer(1, 16),
    ]

    kpi_rows = [["Metric", "Value"]]
    for item in kpis.values():
        kpi_rows.append([item["label"], format_kpi(item["value"], item["format"])])
    story.append(_styled_table(kpi_rows))
    story.append(Spacer(1, 18))

    region_rows = [["Region", "Revenue", "Profit"]]
    for row in frame.groupby("region", as_index=False)[["revenue", "profit"]].sum().itertuples(index=False):
        region_rows.append([row.region, f"${row.revenue:,.0f}", f"${row.profit:,.0f}"])
    story.append(Paragraph("Regional Performance", styles["Heading2"]))
    story.append(_styled_table(region_rows))

    doc.build(story)
    return buffer.getvalue()


def _styled_table(rows: list[list[str]]) -> Table:
    table = Table(rows, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1D4350")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#C9D4DC")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F4F7F9")]),
                ("PADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return table
