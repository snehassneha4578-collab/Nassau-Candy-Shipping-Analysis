# Executive Summary

## Project
Factory-to-Customer Shipping Route Efficiency Analysis for Nassau Candy Distributor

## Purpose

The project explores the available distributor dataset to understand factory distribution, customer geography, shipping-mode patterns, and financial performance.

## Dataset Profile

| Measure | Value |
|---|---:|
| Product-level records | 10,194 |
| Columns | 18 |
| Unique orders | 8,549 |
| Products | 15 |
| Mapped factories | 5 |

## Factory Distribution

| Factory | Records |
|---|---:|
| Lot's O' Nuts | 5,692 |
| Wicked Choccy's | 4,152 |
| Secret Factory | 217 |
| The Other Factory | 100 |
| Sugar Shack | 33 |

The two largest factory groups account for most of the product-level records. These counts are not shipment counts.

## Financial Observations

The existing factory summaries contain sales, cost, and gross-profit measures. These can be used to compare the financial contribution represented in the dataset.

Financial summaries should be interpreted as dataset-level observations and not as independently audited business results.

## Geographical Analysis

The project estimates straight-line distances between factory locations and approximate customer-state reference coordinates.

These estimates provide geographical context only. They are not actual road or delivery distances.

## Data Quality Findings

The Order Date and Ship Date fields contain unusual patterns and very large calculated differences.

The available date fields cannot reliably establish actual shipping transit times, delivery delays, or transportation efficiency. The cause of the inconsistencies has not been independently established.

## Conclusions

The dataset supports exploratory analysis of factory distribution, customer regions, shipping modes, and financial patterns.

It does not contain sufficient verified transportation information to prove actual route efficiency or delivery-time performance.

## Recommendations

1. Obtain verified customer coordinates.
2. Obtain actual transportation route or GPS data.
3. Validate order and shipment dates against operational records.
4. Use road-network distances for realistic route comparisons.
5. Maintain automated data-quality checks.
