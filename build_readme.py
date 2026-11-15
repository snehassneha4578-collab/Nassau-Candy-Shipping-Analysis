from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path(__file__).resolve().parent
README = ROOT / "README.md"

def image_section(folder, heading):
    path = ROOT / folder
    lines = [f"## {heading}", ""]
    if path.exists():
        files = sorted(path.rglob("*.png"))
        for file in files:
            rel = file.relative_to(ROOT).as_posix()
            lines += [f"### {file.stem.replace('_', ' ').title()}", "",
                      f"![{file.stem}]({rel})", ""]
    return "\n".join(lines)

def main():
    charts = image_section("outputs/charts", "Data Visualizations")
    diagrams = image_section("outputs/diagrams", "Project Diagrams")

    content = """# Factory-to-Customer Shipping Route Efficiency Analysis

## Project Overview

An exploratory data analytics project examining factory assignments, customer geography, shipping modes, product distribution, financial patterns, and estimated factory-to-state distances for Nassau Candy Distributor.

## Dataset Overview

| Metric | Value |
|---|---:|
| Product-level records | 10,194 |
| Unique orders | 8,549 |
| Products | 15 |
| Mapped factories | 5 |
| Unmapped product records | 0 |
| Multi-factory orders | 0 |

Product-level records must not be interpreted as unique shipments.

## Project Objectives

- Analyze factory and product distribution.
- Examine customer distribution by geography.
- Explore shipping-mode patterns.
- Compare factory-level sales, costs, and gross profit.
- Estimate approximate factory-to-state distances.
- Investigate unusual date patterns.
- Present results through charts and a dashboard.

## Technology Stack

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly
- Streamlit

## Project Workflow

1. Dataset inspection and preservation.
2. Data cleaning and validation.
3. Product-to-factory mapping.
4. Geographic distribution analysis.
5. Shipping-mode analysis.
6. Financial analysis.
7. Distance estimation.
8. Date-quality investigation.
9. Visualization and reporting.

## Factory Distribution

| Factory | Product records |
|---|---:|
| Lot's O' Nuts | 5,692 |
| Wicked Choccy's | 4,152 |
| Secret Factory | 217 |
| The Other Factory | 100 |
| Sugar Shack | 33 |

## Financial Analysis

The project examines factory-level sales, costs, gross profit, profit margins, and units sold. These are descriptive dataset summaries, not independently audited financial statements.

## Geographic and Route Methodology

Factory coordinates and approximate state-centroid coordinates are used to estimate straight-line distances.

- These are not road distances.
- Customer delivery coordinates are unavailable.
- Estimates do not represent actual vehicle routes.
- Actual fastest or slowest routes cannot be established.

## Date Quality Investigation

| Metric | Observed value |
|---|---|
| Order Date range | 2024-01-02 to 2025-12-31 |
| Ship Date range | 2026-06-30 to 2030-06-28 |
| Mean calculated lead time | 1,320.84 days |
| Median calculated lead time | 1,274 days |
| Lead times above 730 days | All records |

The cause of these unusual date patterns is unknown. They cannot establish actual shipping delays, transit time, or delivery performance.

"""

    content += diagrams + "\n" + charts

    content += """
## Interactive Streamlit Dashboard

Run locally:

```bash
pip install -r dashboard/requirements.txt
streamlit run dashboard/app.py