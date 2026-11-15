import os
import json
import hashlib
import warnings
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

warnings.filterwarnings("ignore")

PROJECT = Path(__file__).resolve().parents[1]
DATA = PROJECT / "data" / "original" / "Nassau Candy Distributor.csv"
PROCESSED = PROJECT / "data" / "processed"
CHARTS = PROJECT / "outputs" / "charts"
REPORTS = PROJECT / "outputs" / "reports"

CHARTS.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "figure.figsize": (12, 7),
    "figure.dpi": 120,
    "savefig.dpi": 220,
    "font.size": 10,
    "axes.titlesize": 15,
    "axes.labelsize": 11,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.grid": True,
    "grid.alpha": 0.25,
})

df = pd.read_csv(DATA)
df["Order Date"] = pd.to_datetime(df["Order Date"], format="%d-%m-%Y", errors="coerce")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="%d-%m-%Y", errors="coerce")

for col in ["Sales", "Units", "Gross Profit", "Cost"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

route_region_path = PROCESSED / "factory_to_region_routes.csv"
route_state_path = PROCESSED / "factory_to_state_routes.csv"
factory_path = PROCESSED / "factory_summary.csv"
region_path = PROCESSED / "regional_summary.csv"
shipping_path = PROCESSED / "shipping_mode_summary.csv"

route_region = pd.read_csv(route_region_path)
route_state = pd.read_csv(route_state_path)
factory = pd.read_csv(factory_path)
region = pd.read_csv(region_path)
shipping = pd.read_csv(shipping_path)

created = []

def save_chart(fig, filename):
    path = CHARTS / filename
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    created.append({
        "file": filename,
        "path": str(path),
        "size_bytes": path.stat().st_size
    })
    print("PASS:", filename)

def bar_chart(data, x, y, title, xlabel, ylabel, filename,
              horizontal=False, rotation=0, color=None):
    fig, ax = plt.subplots()
    if horizontal:
        data = data.sort_values(y)
        ax.barh(data[x].astype(str), data[y], color=color)
        ax.set_xlabel(ylabel)
        ax.set_ylabel(xlabel)
    else:
        ax.bar(data[x].astype(str), data[y], color=color)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        plt.xticks(rotation=rotation, ha="right")
    ax.set_title(title, fontweight="bold")
    ax.yaxis.set_major_formatter(mticker.StrMethodFormatter("{x:,.0f}"))
    save_chart(fig, filename)

print("\nDATASET")
print("Rows:", len(df))
print("Columns:", len(df.columns))
print("Unique orders:", df["Order ID"].nunique())
print("Unique products:", df["Product Name"].nunique())

# 1. Factory distribution
bar_chart(
    factory, "Factory", "Record_Count",
    "Factory-wise Product Record Distribution",
    "Factory", "Product records",
    "01_factory_distribution.png", horizontal=True
)

# 2. US regional distribution
us_region = region[region["Country/Region"] == "United States"]
bar_chart(
    us_region, "Region", "Record_Count",
    "US Shipment Record Distribution by Region",
    "Region", "Product records",
    "02_us_regional_distribution.png"
)

# 3. Country comparison
country = df.groupby("Country/Region").agg(
    Record_Count=("Row ID", "count"),
    Unique_Orders=("Order ID", "nunique")
).reset_index()
bar_chart(
    country, "Country/Region", "Record_Count",
    "Product Records by Country",
    "Country", "Product records",
    "03_country_distribution.png"
)

# 4. Shipping mode
bar_chart(
    shipping, "Ship Mode", "Record_Count",
    "Shipping Mode - Product Record Distribution",
    "Shipping mode", "Product records",
    "04_shipping_mode_distribution.png",
    rotation=15
)

# 5. Product distribution
products = df.groupby("Product Name").agg(
    Record_Count=("Row ID", "count")
).reset_index().sort_values("Record_Count", ascending=False)
bar_chart(
    products, "Product Name", "Record_Count",
    "Product-wise Record Distribution",
    "Product", "Product records",
    "05_product_distribution.png",
    horizontal=True
)

# 6. Factory-region heatmap
pivot = route_region.pivot_table(
    index="Factory", columns="Region",
    values="Record_Count", aggfunc="sum", fill_value=0
)
fig, ax = plt.subplots(figsize=(11, 6))
im = ax.imshow(pivot.values, aspect="auto")
ax.set_xticks(range(len(pivot.columns)), pivot.columns)
ax.set_yticks(range(len(pivot.index)), pivot.index)
ax.set_title("Factory-to-Region Route Volume Heatmap", fontweight="bold")
ax.set_xlabel("Destination region")
ax.set_ylabel("Factory")
for i in range(pivot.shape[0]):
    for j in range(pivot.shape[1]):
        ax.text(j, i, f"{int(pivot.iloc[i, j]):,}",
                ha="center", va="center", fontsize=9)
fig.colorbar(im, ax=ax, label="Product records")
save_chart(fig, "06_factory_region_heatmap.png")

# 7. Top 20 factory-state routes
top_routes = route_state.sort_values(
    "Record_Count", ascending=False
).head(20).copy()
top_routes["Route"] = (
    top_routes["Factory"].astype(str) + " → " +
    top_routes["State/Province"].astype(str)
)
bar_chart(
    top_routes, "Route", "Record_Count",
    "Top 20 Factory-to-State Routes",
    "Factory to destination state", "Product records",
    "07_top_factory_state_routes.png",
    horizontal=True
)

# 8. Top destination states - US only
us = df[df["Country/Region"] == "United States"]
states = us.groupby("State/Province").agg(
    Record_Count=("Row ID", "count")
).reset_index().sort_values("Record_Count", ascending=False).head(20)
bar_chart(
    states, "State/Province", "Record_Count",
    "Top 20 US Destination States",
    "State", "Product records",
    "08_top_us_states.png",
    horizontal=True
)

# 9. Regional sales
regional_sales = df.groupby(
    ["Country/Region", "Region"], as_index=False
).agg(Total_Sales=("Sales", "sum"))
us_sales = regional_sales[regional_sales["Country/Region"] == "United States"]
bar_chart(
    us_sales, "Region", "Total_Sales",
    "US Regional Sales Comparison",
    "Region", "Sales",
    "09_us_regional_sales.png"
)

# 10. Factory gross profit
bar_chart(
    factory, "Factory", "Total_Gross_Profit",
    "Gross Profit by Factory",
    "Factory", "Gross profit",
    "10_factory_gross_profit.png",
    horizontal=True
)

# 11. Factory sales
bar_chart(
    factory, "Factory", "Total_Sales",
    "Total Sales by Factory",
    "Factory", "Sales",
    "11_factory_sales.png",
    horizontal=True
)

# 12. Factory profit margin
factory_margin = factory.copy()
factory_margin["Profit_Margin_Percent"] = np.where(
    factory_margin["Total_Sales"] != 0,
    factory_margin["Total_Gross_Profit"] /
    factory_margin["Total_Sales"] * 100,
    np.nan
)
bar_chart(
    factory_margin, "Factory", "Profit_Margin_Percent",
    "Gross Profit Margin by Factory",
    "Factory", "Gross profit margin (%)",
    "12_factory_profit_margin.png",
    horizontal=True
)

# 13. Sales versus cost
fig, ax = plt.subplots()
ax.scatter(df["Cost"], df["Sales"], alpha=0.35)
ax.set_title("Sales versus Cost Across Product Records", fontweight="bold")
ax.set_xlabel("Cost")
ax.set_ylabel("Sales")
save_chart(fig, "13_sales_vs_cost.png")

# 14. Monthly order record volume
monthly = df.dropna(subset=["Order Date"]).copy()
monthly["Order_Month"] = monthly["Order Date"].dt.to_period("M").astype(str)
monthly = monthly.groupby("Order_Month").agg(
    Record_Count=("Row ID", "count")
).reset_index()
fig, ax = plt.subplots(figsize=(13, 6))
ax.plot(monthly["Order_Month"], monthly["Record_Count"], marker="o")
ax.set_title("Monthly Order Record Volume", fontweight="bold")
ax.set_xlabel("Order month")
ax.set_ylabel("Product records")
ax.tick_params(axis="x", rotation=65)
save_chart(fig, "14_monthly_order_volume.png")

# 15. Units by factory
bar_chart(
    factory, "Factory", "Total_Units",
    "Total Units by Factory",
    "Factory", "Units",
    "15_factory_units.png",
    horizontal=True
)

# 16. Shipping mode sales
shipping_sales = df.groupby("Ship Mode", as_index=False).agg(
    Total_Sales=("Sales", "sum")
)
bar_chart(
    shipping_sales, "Ship Mode", "Total_Sales",
    "Sales by Shipping Mode",
    "Shipping mode", "Sales",
    "16_shipping_mode_sales.png",
    rotation=15
)

# 17. Lead-time anomaly - descriptive diagnostic only
lead = df.dropna(subset=["Order Date", "Ship Date"]).copy()
lead["Lead_Time_Days"] = (
    lead["Ship Date"] - lead["Order Date"]
).dt.days

fig, ax = plt.subplots()
ax.hist(lead["Lead_Time_Days"], bins=30, edgecolor="black")
ax.set_title(
    "Source-Date Diagnostic: Calculated Order-to-Ship Date Difference",
    fontweight="bold"
)
ax.set_xlabel("Calculated date difference (days)")
ax.set_ylabel("Product records")
save_chart(fig, "17_date_anomaly_distribution.png")

# 18. Lead-time by order year - diagnostic only
lead["Order_Year"] = lead["Order Date"].dt.year.astype(str)
fig, ax = plt.subplots()
years = sorted(lead["Order_Year"].dropna().unique())
values = [
    lead.loc[lead["Order_Year"] == year, "Lead_Time_Days"].values
    for year in years
]
ax.boxplot(values, tick_labels=years)
ax.set_title("Date Anomaly Diagnostic by Order Year", fontweight="bold")
ax.set_xlabel("Order year")
ax.set_ylabel("Calculated date difference (days)")
save_chart(fig, "18_date_anomaly_by_year.png")

# 19. Gross profit by region
regional_profit = df.groupby("Region", as_index=False).agg(
    Total_Gross_Profit=("Gross Profit", "sum")
)
bar_chart(
    regional_profit, "Region", "Total_Gross_Profit",
    "Gross Profit by Destination Region",
    "Region", "Gross profit",
    "19_regional_gross_profit.png"
)

# 20. Units versus sales
fig, ax = plt.subplots()
ax.scatter(df["Units"], df["Sales"], alpha=0.35)
ax.set_title("Units versus Sales", fontweight="bold")
ax.set_xlabel("Units")
ax.set_ylabel("Sales")
save_chart(fig, "20_units_vs_sales.png")

# Write manifest and summary
manifest = {
    "project": "Nassau Candy Shipping Route Efficiency Analysis",
    "dataset_rows": int(len(df)),
    "unique_orders": int(df["Order ID"].nunique()),
    "graphs_created": len(created),
    "date_warning": (
        "Date-derived differences are diagnostic only. "
        "Do not interpret them as actual delivery performance."
    ),
    "graphs": created
}

manifest_path = REPORTS / "graph_manifest.json"
with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=4)

print("\n============================================")
print("GRAPH GENERATION SUMMARY")
print("============================================")
print("Graphs generated:", len(created))
print("Chart folder:", CHARTS)
print("Manifest:", manifest_path)
print("Date-derived graphs are diagnostic only.")
