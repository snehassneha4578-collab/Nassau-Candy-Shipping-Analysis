import pandas as pd
import numpy as np
import json
from pathlib import Path

project = Path(__file__).resolve().parents[1]
source = project / "data" / "original" / "Nassau Candy Distributor.csv"
out = project / "outputs" / "reports"
out.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(source)

order = pd.to_datetime(df["Order Date"], format="%d-%m-%Y", errors="coerce")
ship = pd.to_datetime(df["Ship Date"], format="%d-%m-%Y", errors="coerce")
lead = (ship - order).dt.days

df["Parsed Order Date"] = order
df["Parsed Ship Date"] = ship
df["Calculated Lead Time"] = lead

results = {}

print("\n========== 1. LEAD-TIME PATTERN ==========")
print("Unique lead-time values:", lead.nunique())
print("\nMost frequent lead-time values:")
print(lead.value_counts().head(20).to_string())

print("\nLead-time descriptive statistics:")
print(lead.describe(percentiles=[.01, .05, .10, .25, .50, .75, .90, .95, .99]).to_string())

results["unique_lead_time_values"] = int(lead.nunique())
results["most_frequent_lead_times"] = {
    str(k): int(v) for k, v in lead.value_counts().head(20).items()
}

print("\n========== 2. LEAD TIME BY SHIPPING MODE ==========")
mode_stats = df.groupby("Ship Mode")["Calculated Lead Time"].agg(
    ["count", "min", "median", "mean", "max", "std"]
).round(2)
print(mode_stats.to_string())
mode_stats.to_csv(out / "lead_time_by_ship_mode.csv")
results["lead_time_by_ship_mode"] = mode_stats.to_dict(orient="index")

print("\n========== 3. LEAD TIME BY ORDER YEAR ==========")
df["Order Year"] = order.dt.year
year_stats = df.groupby("Order Year")["Calculated Lead Time"].agg(
    ["count", "min", "median", "mean", "max"]
).round(2)
print(year_stats.to_string())
year_stats.to_csv(out / "lead_time_by_order_year.csv")
results["lead_time_by_order_year"] = year_stats.to_dict(orient="index")

print("\n========== 4. LEAD TIME BY ORDER MONTH ==========")
df["Order Month"] = order.dt.to_period("M").astype(str)
month_stats = df.groupby("Order Month")["Calculated Lead Time"].agg(
    ["count", "min", "median", "mean", "max"]
).round(2)
print(month_stats.to_string())
month_stats.to_csv(out / "lead_time_by_order_month.csv")
print("\nFirst 15 months:")
print(month_stats.head(15).to_string())
print("\nLast 15 months:")
print(month_stats.tail(15).to_string())

print("\n========== 5. DATE RANGE RELATIONSHIP ==========")
print("Order date range:", order.min(), "to", order.max())
print("Ship date range:", ship.min(), "to", ship.max())

print("\nOrder date frequency by year:")
print(order.dt.year.value_counts().sort_index().to_string())

print("\nShip date frequency by year:")
print(ship.dt.year.value_counts().sort_index().to_string())

print("\n========== 6. ROW ID AND DATE ORDER ==========")
row_order_corr = df["Row ID"].corr(lead)
row_ship_corr = df["Row ID"].corr(ship.map(pd.Timestamp.toordinal))
row_orderdate_corr = df["Row ID"].corr(order.map(pd.Timestamp.toordinal))

print("Correlation Row ID vs lead time:", round(row_order_corr, 4))
print("Correlation Row ID vs ship date:", round(row_ship_corr, 4))
print("Correlation Row ID vs order date:", round(row_orderdate_corr, 4))

print("\nFirst 10 records by Row ID:")
print(df.sort_values("Row ID")[[
    "Row ID", "Order ID", "Order Date", "Ship Date",
    "Ship Mode", "Calculated Lead Time"
]].head(10).to_string(index=False))

print("\nLast 10 records by Row ID:")
print(df.sort_values("Row ID")[[
    "Row ID", "Order ID", "Order Date", "Ship Date",
    "Ship Mode", "Calculated Lead Time"
]].tail(10).to_string(index=False))

print("\n========== 7. ORDER ID YEAR TOKEN CHECK ==========")
df["Order ID Year Token"] = df["Order ID"].astype(str).str.extract(r"US-(\d{4})", expand=False)
token_year = pd.to_numeric(df["Order ID Year Token"], errors="coerce")
mismatch = token_year.notna() & order.dt.year.notna() & (token_year != order.dt.year)

print("Rows with year token:", int(token_year.notna().sum()))
print("Rows where Order ID year differs from Order Date year:", int(mismatch.sum()))
if mismatch.any():
    print(df.loc[mismatch, [
        "Row ID", "Order ID", "Order Date", "Ship Date"
    ]].head(15).to_string(index=False))

print("\n========== 8. PRODUCT-TO-FACTORY MAPPING ==========")

mapping = {
    "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious": "Lot's O' Nuts",
    "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",
    "Laffy Taffy": "Sugar Shack",
    "SweeTARTS": "Sugar Shack",
    "Nerds": "Sugar Shack",
    "Fun Dip": "Sugar Shack",
    "Fizzy Lifting Drinks": "Sugar Shack",
    "Everlasting Gobstopper": "Secret Factory",
    "Hair Toffee": "The Other Factory",
    "Lickable Wallpaper": "Secret Factory",
    "Wonka Gum": "Secret Factory",
    "Kazookles": "The Other Factory"
}

df["Mapped Factory"] = df["Product Name"].map(mapping)

unmapped = sorted(df.loc[df["Mapped Factory"].isna(), "Product Name"].dropna().unique())
print("Unique dataset products:", df["Product Name"].nunique())
print("Products in supplied mapping:", len(mapping))
print("Unmapped product names:", unmapped if unmapped else "None")
print("\nRecords by mapped factory:")
print(df["Mapped Factory"].value_counts(dropna=False).to_string())

factory_counts = df.groupby("Mapped Factory", dropna=False).size()
factory_counts.to_csv(out / "records_by_mapped_factory.csv")

print("\nProduct counts and records:")
product_counts = df.groupby(["Product Name", "Mapped Factory"], dropna=False).size().reset_index(name="Records")
print(product_counts.to_string(index=False))
product_counts.to_csv(out / "product_factory_mapping_check.csv", index=False)

print("\n========== 9. COUNTRY AND GEOGRAPHY CHECK ==========")
print("Country counts:")
print(df["Country/Region"].value_counts(dropna=False).to_string())

print("\nCountry by region:")
print(pd.crosstab(df["Country/Region"], df["Region"]).to_string())

print("\nCountry by state/province - top values:")
print(df.groupby(["Country/Region", "State/Province"]).size().sort_values(ascending=False).head(30).to_string())

print("\n========== 10. SAVE INVESTIGATION REPORT ==========")

results["order_id_year_mismatch_count"] = int(mismatch.sum())
results["unmapped_products"] = unmapped
results["product_mapping"] = mapping
results["country_counts"] = {
    str(k): int(v) for k, v in df["Country/Region"].value_counts(dropna=False).items()
}
results["row_id_correlations"] = {
    "row_id_vs_lead_time": float(row_order_corr),
    "row_id_vs_ship_date": float(row_ship_corr),
    "row_id_vs_order_date": float(row_orderdate_corr)
}

json_file = out / "date_and_mapping_investigation.json"
txt_file = out / "date_and_mapping_investigation.txt"

json_file.write_text(json.dumps(results, indent=4, default=str), encoding="utf-8")

with txt_file.open("w", encoding="utf-8") as f:
    f.write("NASSAU CANDY - DATE AND MAPPING INVESTIGATION\n")
    f.write("=" * 55 + "\n\n")
    f.write("Unique lead-time values: " + str(lead.nunique()) + "\n")
    f.write("\nLead time by shipping mode:\n" + mode_stats.to_string())
    f.write("\n\nLead time by order year:\n" + year_stats.to_string())
    f.write("\n\nLead time by order month:\n" + month_stats.to_string())
    f.write("\n\nOrder ID year mismatch count: " + str(int(mismatch.sum())))
    f.write("\n\nUnmapped products: " + str(unmapped))
    f.write("\n\nCountry counts:\n" + df["Country/Region"].value_counts().to_string())

print("Saved:", json_file)
print("Saved:", txt_file)
print("Saved: lead_time_by_ship_mode.csv")
print("Saved: lead_time_by_order_year.csv")
print("Saved: lead_time_by_order_month.csv")
print("Saved: product_factory_mapping_check.csv")
print("Saved: records_by_mapped_factory.csv")
print("\nINVESTIGATION SCRIPT COMPLETED.")
