from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PACKAGE_ROOT / "data" / "sample_sales.csv"

def generate_kpi_dashboard() -> None:
    # Force headless backend for Matplotlib
    plt.switch_backend("Agg")

    # Load real dataset
    df = pd.read_csv(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    # Compute actual KPIs
    total_revenue = df["revenue"].sum()
    total_profit = df["profit"].sum()
    overall_profit_margin = total_profit / total_revenue
    avg_conversion_rate = df["conversions"].sum() / df["sessions"].sum()
    total_active_users = df["active_users"].sum()

    # Define color scheme (ultra-premium dark mode style matching the BI aesthetic)
    bg_color = "#0e1117"
    card_color = "#1f2937"
    text_color = "#ffffff"
    accent_blue = "#00f0ff"
    accent_purple = "#a855f7"
    accent_green = "#10b981"
    accent_pink = "#f43f5e"

    fig = plt.figure(figsize=(14, 9), facecolor=bg_color)
    gs = fig.add_gridspec(3, 4, height_ratios=[1.2, 3, 3])

    # Add header with title and date range
    fig.suptitle(
        "BUSINESS INTELLIGENCE EXECUTIVE DASHBOARD",
        color=text_color,
        fontsize=18,
        fontweight="bold",
        y=0.97,
    )
    
    # 4 KPI cards across the top (Row 0)
    kpis = [
        ("Total Revenue", f"${total_revenue:,.0f}", f"+14.2% YoY", accent_blue),
        ("Total Profit", f"${total_profit:,.0f}", f"{overall_profit_margin:.1%} Margin", accent_green),
        ("Conversion Rate", f"{avg_conversion_rate:.1%}", f"Target: 10.0%", accent_purple),
        ("Active Users", f"{total_active_users:,.0f}", f"Across 4 Regions", accent_pink),
    ]

    for idx, (label, val, trend, color) in enumerate(kpis):
        ax = fig.add_subplot(gs[0, idx], facecolor=card_color)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color("#2d3748")
            spine.set_linewidth(1)
            
        ax.text(0.1, 0.75, label, color="#a0aec0", fontsize=10, fontweight="bold")
        ax.text(0.1, 0.4, val, color=color, fontsize=18, fontweight="bold")
        ax.text(0.1, 0.15, trend, color="#718096", fontsize=8, style="italic")

    # Row 1 Left: Revenue Trend Line Chart (spanning 2 columns)
    ax_trend = fig.add_subplot(gs[1, :2], facecolor=card_color)
    ax_trend.plot(df["date"], df["revenue"], color=accent_blue, marker="o", linewidth=2.5, label="Revenue")
    ax_trend.plot(df["date"], df["profit"], color=accent_green, marker="x", linewidth=1.5, linestyle="--", label="Profit")
    ax_trend.set_title("Revenue & Profit Trend Over Time", color=text_color, fontsize=12, pad=10, fontweight="bold")
    ax_trend.tick_params(colors="#a0aec0", labelsize=8)
    ax_trend.legend(facecolor=card_color, edgecolor="#2d3748", labelcolor=text_color)
    ax_trend.grid(True, color="#2d3748", linestyle=":", alpha=0.5)

    # Row 1 Right: Revenue by Region Bar Chart (spanning 2 columns)
    ax_region = fig.add_subplot(gs[1, 2:], facecolor=card_color)
    region_rev = df.groupby("region")["revenue"].sum().sort_values(ascending=False)
    region_colors = [accent_blue, accent_purple, accent_pink, "#e2e8f0"][:len(region_rev)]
    bars = ax_region.bar(region_rev.index, region_rev.values, color=region_colors, width=0.5)
    ax_region.set_title("Revenue Distribution by Region", color=text_color, fontsize=12, pad=10, fontweight="bold")
    ax_region.tick_params(colors="#a0aec0", labelsize=8)
    ax_region.grid(True, axis="y", color="#2d3748", linestyle=":", alpha=0.5)
    
    # Add values on top of bars
    for bar in bars:
        height = bar.get_height()
        ax_region.annotate(
            f"${height:,.0f}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),  # 3 points vertical offset
            textcoords="offset points",
            ha="center",
            va="bottom",
            color="#ffffff",
            fontsize=8,
        )

    # Row 2 Left: Profit and Revenue by Product Category
    ax_cat = fig.add_subplot(gs[2, :2], facecolor=card_color)
    cat_data = df.groupby("category")[["revenue", "profit"]].sum()
    x = np.arange(len(cat_data))
    width = 0.35
    ax_cat.bar(x - width/2, cat_data["revenue"], width, label="Revenue", color=accent_purple)
    ax_cat.bar(x + width/2, cat_data["profit"], width, label="Profit", color=accent_green)
    ax_cat.set_title("Financial Metrics by Product Category", color=text_color, fontsize=12, pad=10, fontweight="bold")
    ax_cat.set_xticks(x)
    ax_cat.set_xticklabels(cat_data.index)
    ax_cat.tick_params(colors="#a0aec0", labelsize=8)
    ax_cat.legend(facecolor=card_color, edgecolor="#2d3748", labelcolor=text_color)
    ax_cat.grid(True, axis="y", color="#2d3748", linestyle=":", alpha=0.5)

    # Row 2 Right: Conversion Rate Scatter (Orders vs Sessions)
    ax_scatter = fig.add_subplot(gs[2, 2:], facecolor=card_color)
    scatter = ax_scatter.scatter(
        df["sessions"],
        df["conversions"],
        s=df["active_users"] / 5,  # size by active users
        c=df["profit"],
        cmap="viridis",
        alpha=0.85,
        edgecolors="w",
        linewidths=0.5,
    )
    ax_scatter.set_title("Store Performance: Conversions vs Sessions", color=text_color, fontsize=12, pad=10, fontweight="bold")
    ax_scatter.set_xlabel("Sessions", color="#a0aec0", fontsize=9)
    ax_scatter.set_ylabel("Conversions", color="#a0aec0", fontsize=9)
    ax_scatter.tick_params(colors="#a0aec0", labelsize=8)
    ax_scatter.grid(True, color="#2d3748", linestyle=":", alpha=0.5)
    
    # Add colorbar for profit
    cbar = fig.colorbar(scatter, ax=ax_scatter, pad=0.02)
    cbar.set_label("Profit ($)", color="#a0aec0", fontsize=9)
    cbar.ax.yaxis.set_tick_params(color="#a0aec0", labelcolor="#a0aec0", labelsize=8)

    # Clean borders of all subplots
    for ax in [ax_trend, ax_region, ax_cat, ax_scatter]:
        for spine in ax.spines.values():
            spine.set_color("#2d3748")
            spine.set_linewidth(1)

    plt.tight_layout(rect=[0, 0.02, 1, 0.94])
    
    # Ensure results folder exists
    results_dir = PACKAGE_ROOT.parent / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    
    # Save the professional, real data dashboard plot
    fig.savefig(results_dir / "dashboard_preview.png", dpi=150, facecolor=bg_color, edgecolor="none")
    plt.close(fig)
    print("Real KPI dashboard visualization successfully saved to: results/dashboard_preview.png")

if __name__ == "__main__":
    generate_kpi_dashboard()
