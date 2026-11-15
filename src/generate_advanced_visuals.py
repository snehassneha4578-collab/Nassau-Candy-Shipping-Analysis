import json
import math
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.patches import Rectangle, FancyArrowPatch, PathPatch
from matplotlib.path import Path as MplPath

PROJECT = Path(__file__).resolve().parents[1]
DATA = PROJECT / "data" / "original" / "Nassau Candy Distributor.csv"
PROCESSED = PROJECT / "data" / "processed"
CHARTS = PROJECT / "outputs" / "charts"
DIAGRAMS = PROJECT / "outputs" / "diagrams"
REPORTS = PROJECT / "outputs" / "reports"

for folder in [CHARTS, DIAGRAMS, REPORTS]:
    folder.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "figure.figsize": (12, 7),
    "figure.dpi": 120,
    "savefig.dpi": 220,
    "font.size": 10,
    "axes.titlesize": 15,
    "axes.grid": True,
    "grid.alpha": 0.22,
})

df = pd.read_csv(DATA)
routes = pd.read_csv(PROCESSED / "factory_to_state_routes.csv")
region_routes = pd.read_csv(PROCESSED / "factory_to_region_routes.csv")

for c in ["Sales", "Cost", "Gross Profit", "Units"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")

FACTORIES = {
    "Lot's O' Nuts": (32.881893, -111.768036),
    "Wicked Choccy's": (32.076176, -81.088371),
    "Sugar Shack": (48.11914, -96.18115),
    "Secret Factory": (41.446333, -90.565487),
    "The Other Factory": (35.1175, -89.971107),
}

# Approximate geographic centroids of US states.
# These are reference points, not customer addresses.
STATE_COORDS = {
    "Alabama":(32.806671,-86.791130),
    "Arizona":(33.729759,-111.431221),
    "Arkansas":(34.969704,-92.373123),
    "California":(36.116203,-119.681564),
    "Colorado":(39.059811,-105.311104),
    "Connecticut":(41.597782,-72.755371),
    "Delaware":(39.318523,-75.507141),
    "Florida":(27.766279,-81.686783),
    "Georgia":(33.040619,-83.643074),
    "Idaho":(44.240459,-114.478828),
    "Illinois":(40.349457,-88.986137),
    "Indiana":(39.849426,-86.258278),
    "Iowa":(42.011539,-93.210526),
    "Kansas":(38.526600,-96.726486),
    "Kentucky":(37.668140,-84.670067),
    "Louisiana":(31.169546,-91.867805),
    "Maine":(44.693947,-69.381927),
    "Maryland":(39.063946,-76.802101),
    "Massachusetts":(42.230171,-71.530106),
    "Michigan":(43.326618,-84.536095),
    "Minnesota":(45.694454,-93.900192),
    "Mississippi":(32.741646,-89.678696),
    "Missouri":(38.456085,-92.288368),
    "Montana":(46.921925,-110.454353),
    "Nebraska":(41.125370,-98.268082),
    "Nevada":(38.313515,-117.055374),
    "New Hampshire":(43.452492,-71.563896),
    "New Jersey":(40.298904,-74.521011),
    "New Mexico":(34.840515,-106.248482),
    "New York":(42.165726,-74.948051),
    "North Carolina":(35.630066,-79.806419),
    "North Dakota":(47.528912,-99.784012),
    "Ohio":(40.388783,-82.764915),
    "Oklahoma":(35.565342,-96.928917),
    "Oregon":(44.572021,-122.070938),
    "Pennsylvania":(40.590752,-77.209755),
    "Rhode Island":(41.680893,-71.511780),
    "South Carolina":(33.856892,-80.945007),
    "South Dakota":(44.299782,-99.438828),
    "Tennessee":(35.747845,-86.692345),
    "Texas":(31.054487,-97.563461),
    "Utah":(40.150032,-111.862434),
    "Vermont":(44.045876,-72.710686),
    "Virginia":(37.769337,-78.169968),
    "Washington":(47.400902,-121.490494),
    "West Virginia":(38.491226,-80.954453),
    "Wisconsin":(44.268543,-89.616508),
    "Wyoming":(42.755966,-107.302490),
    "District of Columbia":(38.9072,-77.0369),
}

generated = []

def save(fig, folder, filename):
    path = folder / filename
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    generated.append({
        "file": filename,
        "folder": str(folder),
        "size_bytes": path.stat().st_size,
        "type": "graph" if folder == CHARTS else "diagram"
    })
    print("PASS:", filename)

def haversine(lat1, lon1, lat2, lon2):
    radius = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2-lat1)
    dl = math.radians(lon2-lon1)
    a = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2 * radius * math.asin(math.sqrt(a))

# ------------------------------------------------
# GRAPH 21: Factory-to-destination network map
# ------------------------------------------------
us_routes = routes[routes["Country/Region"] == "United States"].copy()
us_routes["State/Province"] = us_routes["State/Province"].astype(str)

fig, ax = plt.subplots(figsize=(13, 8))
ax.set_xlim(-125, -66)
ax.set_ylim(24, 50)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_title("Factory-to-Customer Geographic Network - US", fontweight="bold")

for factory, (flat, flon) in FACTORIES.items():
    subset = us_routes[us_routes["Factory"] == factory]
    for _, row in subset.iterrows():
        coords = STATE_COORDS.get(row["State/Province"])
        if coords:
            slat, slon = coords
            ax.plot([flon, slon], [flat, slat], alpha=0.13, linewidth=0.6)
            ax.scatter(slon, slat, s=8, alpha=0.16)

for factory, (lat, lon) in FACTORIES.items():
    ax.scatter(lon, lat, s=100, marker="*", edgecolors="black", zorder=5)
    ax.annotate(factory, (lon, lat), xytext=(5, 5),
                textcoords="offset points", fontsize=8)

ax.text(
    0.01, 0.01,
    "Destination points use approximate state centroids, not customer addresses. "
    "Lines show conceptual geographic connections, not road routes.",
    transform=ax.transAxes, fontsize=8
)
save(fig, CHARTS, "21_factory_customer_network_map.png")

# ------------------------------------------------
# GRAPH 22: Factory-state estimated distance heatmap
# ------------------------------------------------
distance_rows = []
for factory, (flat, flon) in FACTORIES.items():
    for state, (slat, slon) in STATE_COORDS.items():
        distance_rows.append({
            "Factory": factory,
            "State": state,
            "Distance_km": haversine(flat, flon, slat, slon)
        })

dist_df = pd.DataFrame(distance_rows)
observed_states = set(us_routes["State/Province"].dropna())
dist_df = dist_df[dist_df["State"].isin(observed_states)]
distance_pivot = dist_df.pivot(
    index="Factory", columns="State", values="Distance_km"
)

fig, ax = plt.subplots(figsize=(16, 6))
im = ax.imshow(distance_pivot.values, aspect="auto")
ax.set_yticks(range(len(distance_pivot.index)), distance_pivot.index)
ax.set_xticks(range(len(distance_pivot.columns)), distance_pivot.columns, rotation=70)
ax.set_title("Estimated Straight-Line Factory-to-State Distance (km)", fontweight="bold")
ax.set_xlabel("US destination state reference centroid")
ax.set_ylabel("Factory")
fig.colorbar(im, ax=ax, label="Estimated distance (km)")
save(fig, CHARTS, "22_factory_state_distance_heatmap.png")

# ------------------------------------------------
# GRAPH 23: Factory-to-region flow diagram (Sankey-style)
# ------------------------------------------------
flow = region_routes[
    region_routes["Country/Region"] == "United States"
].groupby(["Factory", "Region"], as_index=False)["Record_Count"].sum()

factory_names = list(FACTORIES.keys())
region_names = ["Pacific", "Atlantic", "Interior", "Gulf"]

fig, ax = plt.subplots(figsize=(14, 9))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis("off")
ax.set_title("Factory-to-Region Product Record Flow", fontsize=16, fontweight="bold")

left_y = np.linspace(8.5, 1.5, len(factory_names))
right_y = np.linspace(8, 2, len(region_names))

for name, y in zip(factory_names, left_y):
    ax.add_patch(Rectangle((0.3, y-0.35), 2.0, 0.7, fill=False, linewidth=1.5))
    ax.text(1.3, y, name, ha="center", va="center", fontsize=9)

for name, y in zip(region_names, right_y):
    ax.add_patch(Rectangle((7.7, y-0.35), 1.8, 0.7, fill=False, linewidth=1.5))
    ax.text(8.6, y, name, ha="center", va="center", fontsize=10)

max_value = max(flow["Record_Count"].max(), 1)
for i, factory in enumerate(factory_names):
    for j, region_name in enumerate(region_names):
        match = flow[
            (flow["Factory"] == factory) &
            (flow["Region"] == region_name)
        ]
        if match.empty:
            continue
        value = int(match["Record_Count"].iloc[0])
        ax.add_patch(FancyArrowPatch(
            (2.35, left_y[i]), (7.65, right_y[j]),
            arrowstyle="-", linewidth=0.5 + 5*value/max_value,
            alpha=0.35, connectionstyle="arc3,rad=0.04"
        ))

ax.text(1.3, 9.4, "FACTORIES", ha="center", fontweight="bold")
ax.text(8.6, 9.4, "US REGIONS", ha="center", fontweight="bold")
ax.text(5, 0.5, "Connection width represents product-record volume.",
        ha="center", fontsize=9)
save(fig, CHARTS, "23_factory_region_flow_diagram.png")

# ------------------------------------------------
# GRAPH 24: Pareto analysis of factory-state routes
# ------------------------------------------------
pareto = us_routes.groupby(
    ["Factory", "State/Province"], as_index=False
)["Record_Count"].sum().sort_values("Record_Count", ascending=False)

pareto["Route"] = pareto["Factory"] + " → " + pareto["State/Province"]
pareto = pareto.reset_index(drop=True)
pareto["Cumulative_Percent"] = (
    pareto["Record_Count"].cumsum() / pareto["Record_Count"].sum() * 100
)

top = pareto.head(20)
fig, ax1 = plt.subplots(figsize=(14, 7))
ax1.bar(top["Route"], top["Record_Count"])
ax1.set_ylabel("Product records")
ax1.set_title("Pareto Analysis - Top 20 Factory-to-State Routes", fontweight="bold")
ax1.tick_params(axis="x", rotation=70)
ax2 = ax1.twinx()
ax2.plot(top["Route"], top["Cumulative_Percent"], marker="o")
ax2.set_ylabel("Cumulative share (%)")
ax2.set_ylim(0, 105)
save(fig, CHARTS, "24_factory_state_route_pareto.png")

# ------------------------------------------------
# GRAPH 25: Financial correlation heatmap
# ------------------------------------------------
financial = df[["Sales", "Cost", "Gross Profit", "Units"]].corr()
fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(financial.values, vmin=-1, vmax=1)
ax.set_xticks(range(4), financial.columns, rotation=25)
ax.set_yticks(range(4), financial.index)
ax.set_title("Financial and Units Correlation Matrix", fontweight="bold")
for i in range(4):
    for j in range(4):
        ax.text(j, i, f"{financial.iloc[i,j]:.2f}",
                ha="center", va="center")
fig.colorbar(im, ax=ax, label="Correlation coefficient")
save(fig, CHARTS, "25_financial_correlation_heatmap.png")

# ------------------------------------------------
# GRAPH 26: Top 20 estimated factory-state distances
# ------------------------------------------------
observed = us_routes.groupby(
    ["Factory", "State/Province"], as_index=False
)["Record_Count"].sum()

observed["Estimated_Distance_km"] = observed.apply(
    lambda r: haversine(
        *FACTORIES[r["Factory"]],
        *STATE_COORDS[r["State/Province"]]
    ) if r["State/Province"] in STATE_COORDS else np.nan,
    axis=1
)

top_distance = observed.dropna().sort_values(
    "Estimated_Distance_km", ascending=False
).head(20).copy()
top_distance["Route"] = (
    top_distance["Factory"] + " → " + top_distance["State/Province"]
)

fig, ax = plt.subplots(figsize=(12, 8))
ordered = top_distance.sort_values("Estimated_Distance_km")
ax.barh(ordered["Route"], ordered["Estimated_Distance_km"])
ax.set_xlabel("Estimated straight-line distance (km)")
ax.set_title("Top 20 Estimated Factory-to-State Distances", fontweight="bold")
save(fig, CHARTS, "26_top_estimated_factory_state_distances.png")

# ------------------------------------------------
# DIAGRAM 1: Project workflow
# ------------------------------------------------
def flow_diagram(title, boxes, filename):
    fig, ax = plt.subplots(figsize=(11, 9))
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, len(boxes)*1.45 + 1)
    ax.set_title(title, fontweight="bold", fontsize=16)

    ys = np.arange(len(boxes))[::-1] * 1.45 + 0.7
    for i, (label, y) in enumerate(zip(boxes, ys)):
        ax.add_patch(Rectangle((1.5, y), 7, 0.72, fill=False, linewidth=1.5))
        ax.text(5, y+0.36, label, ha="center", va="center", fontsize=10)
        if i < len(boxes)-1:
            ax.annotate("", xy=(5, ys[i+1]+0.75), xytext=(5, y),
                        arrowprops={"arrowstyle":"->", "lw":1.5})
    save(fig, DIAGRAMS, filename)

flow_diagram(
    "Nassau Candy - Analytical Project Workflow",
    [
        "Original Nassau Candy Distributor Dataset",
        "Data Quality and Consistency Checks",
        "Product-to-Factory Mapping",
        "Factory and Destination Route Aggregation",
        "Geographic and Financial Analysis",
        "Graphs, Technical Visuals and Dashboard",
        "Research Findings and Recommendations"
    ],
    "diagram_01_project_workflow.png"
)

# DIAGRAM 2: Dataset architecture
flow_diagram(
    "Dataset and Analysis Architecture",
    [
        "Original CSV - 10,194 Records and 18 Columns",
        "Order, Product, Location and Financial Fields",
        "Product-to-Factory Mapping Reference",
        "Factory Coordinates and Destination References",
        "Processed Route and Summary Tables",
        "Analytical Graphs and Visualizations",
        "Executive Summary and Research Paper"
    ],
    "diagram_02_data_architecture.png"
)

# DIAGRAM 3: Route analysis methodology
flow_diagram(
    "Factory-to-Customer Route Analysis Methodology",
    [
        "Identify Product Records and Order IDs",
        "Assign Products to Their Mapped Factories",
        "Attach Verified Factory Coordinates",
        "Group Records by Destination State and Region",
        "Calculate Estimated Straight-Line Distances",
        "Compare Route Volume and Geographic Coverage",
        "Interpret Findings with Data Limitations"
    ],
    "diagram_03_route_methodology.png"
)

# DIAGRAM 4: Date anomaly warning
flow_diagram(
    "Date Data Validation and Interpretation Safeguard",
    [
        "Read Order Date and Ship Date",
        "Parse Dates Using the Dataset Date Format",
        "Calculate Date Difference for Diagnostic Purposes",
        "Detect Unusually Large Date Differences",
        "Investigate Source-Date Inconsistency",
        "Exclude Unverified Lead Times from Performance Claims"
    ],
    "diagram_04_date_quality_safeguard.png"
)

# Save distance data for reproducibility
dist_df.to_csv(PROCESSED / "estimated_factory_state_distances.csv", index=False)
observed.to_csv(PROCESSED / "observed_route_distance_estimates.csv", index=False)
pareto.to_csv(PROCESSED / "factory_state_route_pareto.csv", index=False)

manifest = {
    "project": "Nassau Candy Shipping Route Efficiency Analysis",
    "source_records": int(len(df)),
    "additional_graphs": 6,
    "technical_diagrams": 4,
    "generated_visuals": generated,
    "distance_method": "Haversine straight-line distance using factory coordinates and approximate US state centroids",
    "distance_warning": "Not actual road distance, travel time, or delivery route.",
    "network_map_warning": "State centroids are approximate reference points, not individual customer locations.",
    "date_warning": "Date differences are diagnostic only pending investigation."
}

with open(REPORTS / "advanced_visuals_manifest.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=4)

print("\nADVANCED VISUAL GENERATION SUMMARY")
print("Additional graphs:", 6)
print("Technical diagrams:", 4)
print("Total new visuals:", len(generated))
print("Saved distance reference CSVs: 3")
print("Manifest saved.")
