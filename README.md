# Factory-to-Customer Shipping Route Efficiency Analysis

## Project Overview

This project explores factory assignments, customer geography, shipping modes, product distribution, financial patterns, and estimated factory-to-state distances using the Nassau Candy Distributor dataset.

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
7. Approximate distance estimation.
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

## Date Quality Investigation

| Metric | Observed value |
|---|---|
| Order Date range | 2024-01-02 to 2025-12-31 |
| Ship Date range | 2026-06-30 to 2030-06-28 |
| Mean calculated lead time | 1,320.84 days |
| Median calculated lead time | 1,274 days |
| Lead times above 730 days | All records |

The cause of these unusual date patterns is unknown. These dates cannot establish actual shipping delays, transit time, or delivery performance.

## Geographic and Route Methodology

Factory coordinates and approximate state-centroid coordinates are used to estimate straight-line distances. These are not road distances, actual vehicle routes, or verified customer delivery distances.

## Data Visualizations

### factory distribution

![factory distribution](outputs/charts/01_factory_distribution.png)

### us regional distribution

![us regional distribution](outputs/charts/02_us_regional_distribution.png)

### country distribution

![country distribution](outputs/charts/03_country_distribution.png)

### shipping mode distribution

![shipping mode distribution](outputs/charts/04_shipping_mode_distribution.png)

### product distribution

![product distribution](outputs/charts/05_product_distribution.png)

### factory region heatmap

![factory region heatmap](outputs/charts/06_factory_region_heatmap.png)

### top factory state routes

![top factory state routes](outputs/charts/07_top_factory_state_routes.png)

### top us states

![top us states](outputs/charts/08_top_us_states.png)

### us regional sales

![us regional sales](outputs/charts/09_us_regional_sales.png)

### factory gross profit

![factory gross profit](outputs/charts/10_factory_gross_profit.png)

### factory sales

![factory sales](outputs/charts/11_factory_sales.png)

### factory profit margin

![factory profit margin](outputs/charts/12_factory_profit_margin.png)

### sales vs cost

![sales vs cost](outputs/charts/13_sales_vs_cost.png)

### monthly order volume

![monthly order volume](outputs/charts/14_monthly_order_volume.png)

### factory units

![factory units](outputs/charts/15_factory_units.png)

### shipping mode sales

![shipping mode sales](outputs/charts/16_shipping_mode_sales.png)

### date anomaly distribution

![date anomaly distribution](outputs/charts/17_date_anomaly_distribution.png)

### date anomaly by year

![date anomaly by year](outputs/charts/18_date_anomaly_by_year.png)

### regional gross profit

![regional gross profit](outputs/charts/19_regional_gross_profit.png)

### units vs sales

![units vs sales](outputs/charts/20_units_vs_sales.png)

### factory customer network map

![factory customer network map](outputs/charts/21_factory_customer_network_map.png)

### factory state distance heatmap

![factory state distance heatmap](outputs/charts/22_factory_state_distance_heatmap.png)

### factory region flow diagram

![factory region flow diagram](outputs/charts/23_factory_region_flow_diagram.png)

### factory state route pareto

![factory state route pareto](outputs/charts/24_factory_state_route_pareto.png)

### financial correlation heatmap

![financial correlation heatmap](outputs/charts/25_financial_correlation_heatmap.png)

### top estimated factory state distances

![top estimated factory state distances](outputs/charts/26_top_estimated_factory_state_distances.png)

## Project Diagrams

### diagram 01 project workflow

![diagram 01 project workflow](outputs/diagrams/diagram_01_project_workflow.png)

### diagram 02 data architecture

![diagram 02 data architecture](outputs/diagrams/diagram_02_data_architecture.png)

### diagram 03 route methodology

![diagram 03 route methodology](outputs/diagrams/diagram_03_route_methodology.png)

### diagram 04 date quality safeguard

![diagram 04 date quality safeguard](outputs/diagrams/diagram_04_date_quality_safeguard.png)

## Interactive Streamlit Dashboard

Run locally:

    pip install -r dashboard/requirements.txt
    streamlit run dashboard/app.py

## Project Validation

Run:

    python tests/validate_project.py

## Limitations

- Product records are not shipment records.
- Customer delivery coordinates are unavailable.
- Distance estimates are approximate straight-line measurements.
- Date anomalies require source-system verification.
- Illustrative images do not verify actual company facilities.
- Actual delivery performance cannot be established from this dataset.

## Future Improvements

- Obtain verified customer coordinates.
- Integrate road-network routing.
- Validate dates against source-system records.
- Obtain shipment-level tracking information.
- Extend dashboard functionality and automated testing.

## Conclusion

This project provides an exploratory analysis of factory distribution, customer geography, shipping modes, financial patterns, and approximate geographic relationships in the supplied dataset.

**Domain:** Data Analytics | Supply Chain Analytics | Business Intelligence
