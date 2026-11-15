import pandas as pd
import json
from pathlib import Path

project = Path(__file__).resolve().parents[1]
source = project / "data" / "original" / "Nassau Candy Distributor.csv"
processed = project / "data" / "processed"
reports = project / "outputs" / "reports"

processed.mkdir(parents=True, exist_ok=True)
reports.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(source)

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

coordinates = {
    "Lot's O' Nuts": (32.881893, -111.768036),
    "Wicked Choccy's": (32.076176, -81.088371),
    "Sugar Shack": (48.119140, -96.181150),
    "Secret Factory": (41.446333, -90.565487),
    "The Other Factory": (35.117500, -89.971107)
}

df["Factory"] = df["Product Name"].map(mapping)

if df["Factory"].isna().any():
    raise ValueError("Unmapped product found. Route analysis stopped.")

df["Factory Latitude"] = df["Factory"].map(
    lambda x: coordinates[x][0]
)
df["Factory Longitude"] = df["Factory"].map(
    lambda x: coordinates[x][1]
)

print("\n========== 1. FACTORY ASSIGNMENT ==========")
print("Total records:", len(df))
print("Mapped records:", int(df["Factory"].notna().sum()))
print("Unmapped records:", int(df["Factory"].isna().sum()))
print("\nFactory distribution:")
print(df["Factory"].value_counts().to_string())

print("\n========== 2. ORDER STRUCTURE ==========")
print("Unique Order IDs:", df["Order ID"].nunique())
print("Unique Row IDs:", df["Row ID"].nunique())
print("Average records per order:", round(
    len(df) / df["Order ID"].nunique(), 2
))

order_factory = df.groupby("Order ID")["Factory"].nunique()
multi_factory_orders = order_factory[order_factory > 1]

print("Orders associated with multiple factories:", len(multi_factory_orders))
print("Orders associated with exactly one factory:",
      int((order_factory == 1).sum()))

print("\nSample multi-factory orders:")
if len(multi_factory_orders):
    print(
        df[df["Order ID"].isin(multi_factory_orders.index)]
        .groupby("Order ID")["Factory"]
        .agg(lambda x: ", ".join(sorted(set(x))))
        .head(15).to_string()
    )

print("\n========== 3. FACTORY TO REGION ROUTES ==========")

region_routes = (
    df.groupby(
        ["Country/Region", "Factory", "Region"],
        dropna=False
    )
    .agg(
        Record_Count=("Row ID", "count"),
        Unique_Order_Count=("Order ID", "nunique"),
        Unique_Products=("Product Name", "nunique"),
        Unique_States=("State/Province", "nunique"),
        Total_Units=("Units", "sum"),
        Total_Sales=("Sales", "sum"),
        Total_Gross_Profit=("Gross Profit", "sum")
    )
    .reset_index()
)

region_routes = region_routes.sort_values(
    ["Country/Region", "Record_Count"],
    ascending=[True, False]
)

region_routes.to_csv(
    processed / "factory_to_region_routes.csv",
    index=False
)

print(region_routes.to_string(index=False))

print("\n========== 4. FACTORY TO STATE ROUTES ==========")

state_routes = (
    df.groupby(
        ["Country/Region", "Factory", "Region", "State/Province"],
        dropna=False
    )
    .agg(
        Record_Count=("Row ID", "count"),
        Unique_Order_Count=("Order ID", "nunique"),
        Unique_Products=("Product Name", "nunique"),
        Total_Units=("Units", "sum"),
        Total_Sales=("Sales", "sum"),
        Total_Gross_Profit=("Gross Profit", "sum")
    )
    .reset_index()
)

state_routes = state_routes.sort_values(
    ["Record_Count"],
    ascending=False
)

state_routes.to_csv(
    processed / "factory_to_state_routes.csv",
    index=False
)

print("\nTop 20 factory-to-state routes by record count:")
print(state_routes.head(20).to_string(index=False))

print("\n========== 5. FACTORY SUMMARY ==========")

factory_summary = (
    df.groupby("Factory")
    .agg(
        Record_Count=("Row ID", "count"),
        Unique_Order_Count=("Order ID", "nunique"),
        Unique_Products=("Product Name", "nunique"),
        Unique_States=("State/Province", "nunique"),
        Unique_Regions=("Region", "nunique"),
        Total_Units=("Units", "sum"),
        Total_Sales=("Sales", "sum"),
        Total_Gross_Profit=("Gross Profit", "sum"),
        Total_Cost=("Cost", "sum")
    )
    .reset_index()
)

factory_summary.to_csv(
    processed / "factory_summary.csv",
    index=False
)

print(factory_summary.to_string(index=False))

print("\n========== 6. REGION SUMMARY ==========")

regional_summary = (
    df.groupby(["Country/Region", "Region"])
    .agg(
        Record_Count=("Row ID", "count"),
        Unique_Order_Count=("Order ID", "nunique"),
        Unique_States=("State/Province", "nunique"),
        Unique_Factories=("Factory", "nunique"),
        Total_Units=("Units", "sum"),
        Total_Sales=("Sales", "sum")
    )
    .reset_index()
)

regional_summary.to_csv(
    processed / "regional_summary.csv",
    index=False
)

print(regional_summary.to_string(index=False))

print("\n========== 7. SHIPPING MODE COUNTS ==========")

shipping_summary = (
    df.groupby("Ship Mode")
    .agg(
        Record_Count=("Row ID", "count"),
        Unique_Order_Count=("Order ID", "nunique"),
        Total_Units=("Units", "sum"),
        Total_Sales=("Sales", "sum")
    )
    .reset_index()
)

shipping_summary.to_csv(
    processed / "shipping_mode_summary.csv",
    index=False
)

print(shipping_summary.to_string(index=False))

print("\n========== 8. COUNTRY SUMMARY ==========")

country_summary = (
    df.groupby("Country/Region")
    .agg(
        Record_Count=("Row ID", "count"),
        Unique_Order_Count=("Order ID", "nunique"),
        Unique_States_Provinces=("State/Province", "nunique"),
        Unique_Factories=("Factory", "nunique")
    )
    .reset_index()
)

country_summary.to_csv(
    processed / "country_summary.csv",
    index=False
)

print(country_summary.to_string(index=False))

print("\n========== 9. SAVE ANALYSIS SUMMARY ==========")

summary = {
    "total_records": int(len(df)),
    "unique_orders": int(df["Order ID"].nunique()),
    "unique_products": int(df["Product Name"].nunique()),
    "mapped_factories": int(df["Factory"].nunique()),
    "unmapped_records": int(df["Factory"].isna().sum()),
    "multi_factory_orders": int(len(multi_factory_orders)),
    "route_region_combinations": int(len(region_routes)),
    "route_state_combinations": int(len(state_routes)),
    "date_warning": (
        "Shipping lead times are excluded from reliable performance "
        "interpretation pending investigation of source-date anomalies."
    ),
    "route_volume_definition": (
        "Record_Count counts product rows. Unique_Order_Count counts "
        "distinct Order IDs within each factory and destination group."
    )
}

(report := reports / "route_analysis_summary.json").write_text(
    json.dumps(summary, indent=4),
    encoding="utf-8"
)

print(json.dumps(summary, indent=4))
print("\nROUTE ANALYSIS COMPLETED.")
