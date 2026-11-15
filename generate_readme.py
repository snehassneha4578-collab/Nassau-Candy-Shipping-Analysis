from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path(__file__).resolve().parent
README = ROOT / "README.md"
ASSETS = ROOT / "assets"
CHARTS = ROOT / "outputs" / "charts"
DIAGRAMS = ROOT / "outputs" / "diagrams"
IMAGES = ROOT / "images"


def backup_readme():
    if README.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = ROOT / f"README_backup_{timestamp}.md"
        shutil.copy2(README, backup)
        print(f"[PASS] README backup created: {backup.name}")


def create_header():
    ASSETS.mkdir(parents=True, exist_ok=True)

    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="300" viewBox="0 0 1200 300">
<defs>
<linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
<stop offset="0%" stop-color="#25113d"/>
<stop offset="55%" stop-color="#7437a8"/>
<stop offset="100%" stop-color="#d94f91"/>
</linearGradient>
</defs>
<rect width="1200" height="300" rx="28" fill="url(#g)"/>
<circle cx="1050" cy="50" r="180" fill="#ffffff" opacity=".07"/>
<circle cx="1120" cy="260" r="130" fill="#9ff5d0" opacity=".12"/>
<text x="65" y="115" fill="#ffffff" font-size="45" font-family="Arial" font-weight="bold">NASSAU CANDY</text>
<text x="65" y="170" fill="#ffffff" font-size="29" font-family="Arial">Shipping Route Efficiency Analysis</text>
<text x="65" y="225" fill="#c9f7e5" font-size="19" font-family="Arial">Factory-to-Customer Distribution | Data Analytics</text>
</svg>"""

    (ASSETS / "readme_header.svg").write_text(svg, encoding="utf-8")
    print("[PASS] README visual header created")


def get_images(folder):
    if not folder.exists():
        return []

    extensions = {".png", ".jpg", ".jpeg", ".webp"}

    return sorted(
        path for path in folder.rglob("*")
        if path.is_file() and path.suffix.lower() in extensions
    )


def create_diagrams():
    output = []

    for file in get_images(DIAGRAMS):
        relative = file.relative_to(ROOT).as_posix()

        output.extend([
            f"### {file.stem.replace('_', ' ').title()}",
            "",
            f"![{file.stem}]({relative})",
            ""
        ])

    return "\n".join(output)


def create_charts():
    files = sorted(CHARTS.glob("*.png")) if CHARTS.exists() else []

    groups = {
        "Factory and Customer Distribution": [
            "01_", "02_", "03_", "04_", "05_"
        ],
        "Geographic and Route Analysis": [
            "06_", "07_", "08_", "21_", "22_", "23_", "24_", "26_"
        ],
        "Financial and Product Analysis": [
            "09_", "10_", "11_", "12_", "13_", "15_",
            "16_", "19_", "20_", "25_"
        ],
        "Order and Date Quality Analysis": [
            "14_", "17_", "18_"
        ]
    }

    output = []
    used = set()

    for heading, prefixes in groups.items():
        selected = [
            file for file in files
            if any(file.name.startswith(prefix) for prefix in prefixes)
        ]

        if selected:
            output.extend([f"### {heading}", ""])

        for file in selected:
            used.add(file)
            relative = file.relative_to(ROOT).as_posix()

            output.extend([
                f"#### {file.stem.replace('_', ' ').title()}",
                "",
                f"![{file.stem}]({relative})",
                ""
            ])

    remaining = [file for file in files if file not in used]

    if remaining:
        output.extend(["### Additional Visualizations", ""])

        for file in remaining:
            relative = file.relative_to(ROOT).as_posix()

            output.extend([
                f"#### {file.stem.replace('_', ' ').title()}",
                "",
                f"![{file.stem}]({relative})",
                ""
            ])

    return "\n".join(output), len(files)


def create_gallery():
    categories = {
        "Company Background": "company_background",
        "Product Assortment": "product_assortment",
        "Transportation": "transportation",
        "Supply Chain": "supply_chain",
        "Dashboard Illustrations": "dashboard_illustrations",
        "Historical Candy References": "historical_candy_references"
    }

    output = []

    for heading, folder in categories.items():
        files = get_images(IMAGES / folder)

        if not files:
            continue

        output.extend([f"### {heading}", ""])

        for file in files:
            relative = file.relative_to(ROOT).as_posix()

            output.extend([
                f"![{file.stem.replace('_', ' ')}]({relative})",
                ""
            ])

    return "\n".join(output)


def main():
    print("===== NASSAU CANDY README GENERATOR =====")

    backup_readme()
    create_header()

    charts, chart_count = create_charts()
    diagrams = create_diagrams()
    gallery = create_gallery()

    content = r"""<div align="center">

![Nassau Candy Shipping Analysis](assets/readme_header.svg)

# Factory-to-Customer Shipping Route Efficiency Analysis

**Nassau Candy Distributor | Data Analytics Project**

</div>

---

## 1. Project Overview

This project explores factory-to-customer distribution patterns for Nassau Candy Distributor using product-level order records.

The analysis examines factory assignments, customer geography, shipping modes, sales, costs, gross profit, and estimated geographic distances.

This is an exploratory distribution-network analysis. It does not establish actual delivery speed or road-route efficiency.

## 2. Project Objectives

- Analyze product distribution across mapped factories.
- Examine customer distribution across regions and states.
- Explore shipping-mode usage and sales patterns.
- Compare factory-level sales, costs, and gross profit.
- Estimate approximate straight-line factory-to-state distances.
- Investigate unusual date patterns and data-quality limitations.
- Present findings through visualizations and an interactive dashboard.

## 3. Dataset Overview

| Dataset characteristic | Value |
|---|---:|
| Product-level records | 10,194 |
| Unique orders | 8,549 |
| Products | 15 |
| Mapped factories | 5 |
| Unmapped product records | 0 |
| Multi-factory orders | 0 |

**Important:** Product-level records are not equivalent to unique shipments. One order may contain multiple product records.

## 4. Technology Stack

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly
- Streamlit
- Git and GitHub

## 5. Project Workflow

1. Dataset inspection and preservation.
2. Data cleaning and validation.
3. Product-to-factory mapping.
4. Factory and customer geography analysis.
5. Shipping-mode analysis.
6. Financial analysis.
7. Approximate geographic distance estimation.
8. Date anomaly investigation.
9. Visualization and dashboard development.

## 6. Project Architecture and Methodology

"""

    content += diagrams

    content += r"""

## 7. Factory Distribution Analysis

The dataset maps 10,194 product records to five factories.

| Factory | Product records |
|---|---:|
| Lot's O' Nuts | 5,692 |
| Wicked Choccy's | 4,152 |
| Secret Factory | 217 |
| The Other Factory | 100 |
| Sugar Shack | 33 |

These values represent product-level records, not independent shipments.

## 8. Financial Analysis

The analysis includes factory-level:

- Sales
- Cost
- Gross profit
- Profit margin
- Units sold

These are descriptive summaries of the supplied dataset, not independently audited financial statements.

## 9. Geographic and Route Analysis

Approximate factory coordinates and approximate state-centroid coordinates are used to estimate straight-line distances.

**Geographic limitations:**

- Estimated distances are not road distances.
- Customer delivery coordinates are unavailable.
- Estimates do not represent actual vehicle routes.
- No fastest or slowest delivery route can be established from these estimates.

## 10. Date Quality Investigation

The supplied date fields show unusual patterns:

| Metric | Observed value |
|---|---|
| Order Date range | 2024-01-02 to 2025-12-31 |
| Ship Date range | 2026-06-30 to 2030-06-28 |
| Mean calculated lead time | 1,320.84 days |
| Median calculated lead time | 1,274 days |
| Lead times above 730 days | All records |

These patterns require verification against the original source system. Their underlying cause is unknown.

Therefore, these dates cannot support reliable claims about actual shipping delays, transit time, or delivery performance.

## 11. Data Visualizations

The charts are grouped by analytical topic.

"""

    content += charts

    content += r"""

## 12. Interactive Streamlit Dashboard

The project includes a Streamlit dashboard.

### Run locally

```bash
pip install -r dashboard/requirements.txt
streamlit run dashboard/app.py