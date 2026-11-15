# Factory-to-Customer Shipping Route Efficiency Analysis for Nassau Candy Distributor

## Abstract

This study presents an exploratory analysis of the Nassau Candy Distributor dataset. It examines factory distribution, customer geography, shipping-mode patterns, product distribution, financial measures, and approximate factory-to-state geographical distances. Python-based data processing and visualization are used to organize and interpret the available records. The study also investigates unusual date patterns that limit the interpretation of shipping performance. The results provide a descriptive view of the dataset rather than verified measurements of transportation efficiency.

## Keywords

Supply Chain Analytics, Data Analytics, Factory Distribution, Geographical Analysis, Financial Analysis, Data Quality, Python.

## 1. Introduction

Distribution analysis helps organizations understand how products, factories, and customer destinations are represented in operational datasets.

This project investigates the available Nassau Candy Distributor data to identify distribution patterns and summarize financial and geographical information.

## 2. Problem Statement

The project aims to organize and analyze factory-to-customer distribution information while identifying the limitations that prevent reliable conclusions about actual transportation performance.

## 3. Objectives

- Analyze factory-level product distribution.
- Examine customer distribution by region, country, and state.
- Study shipping-mode patterns.
- Compare financial measures across factories and regions.
- Estimate approximate factory-to-state geographical distances.
- Investigate date-field inconsistencies.
- Communicate results through analytical visualizations.

## 4. Dataset Description

The dataset contains 10,194 product-level records, 18 columns, 8,549 unique orders, 15 products, and five mapped factories.

The records represent product-level entries and should not be treated as unique shipments.

## 5. Tools and Technologies

Python, Pandas, NumPy, Matplotlib, and Seaborn are used for data processing and visualization. Streamlit is planned for interactive presentation of processed results.

## 6. Methodology

### 6.1 Data Inspection

The source data is inspected for structure, columns, missing values, and consistency.

### 6.2 Factory Mapping

Products are assigned to factories using the project's product-to-factory mapping.

### 6.3 Distribution Analysis

Factory, regional, country, state, product, and shipping-mode patterns are summarized.

### 6.4 Financial Analysis

Sales, costs, gross profit, and profit margins are examined using the processed summaries.

### 6.5 Geographical Estimation

Approximate straight-line distances are calculated between factory reference locations and customer-state reference coordinates.

### 6.6 Data-Quality Investigation

Order Date and Ship Date patterns are examined to identify inconsistencies and limitations.

## 7. Results and Discussion

The dataset contains five mapped factories. Lot's O' Nuts and Wicked Choccy's account for the largest product-level record counts.

The generated charts and processed summaries provide further views of regional distribution, product patterns, shipping modes, and financial measures.

The date fields show unusual patterns and very large calculated differences. These cannot be interpreted as verified transportation transit times or shipping delays.

## 8. Geographical Analysis Limitations

Customer-level coordinates are not available in the source dataset. The distance estimates use approximate geographical reference points and straight-line calculations.

They do not represent actual road distances, verified transportation routes, or measured delivery distances.

## 9. Limitations

- Date fields cannot reliably establish actual shipping performance.
- The cause of the date inconsistencies is not independently established.
- Customer-level coordinates are unavailable.
- Distance estimates are approximate straight-line estimates.
- The dataset does not provide verified GPS or road-route measurements.
- Product-level record counts are not unique shipment counts.

## 10. Recommendations

- Obtain validated order and shipment timestamps.
- Collect customer-level geographical coordinates.
- Integrate actual transportation route or GPS information.
- Use road-network routing for practical distance comparisons.
- Expand automated data-quality validation.

## 11. Conclusion

The project demonstrates an exploratory approach to distribution, geographical, and financial analysis using Python. The analysis provides useful descriptive information about the available records while documenting the limitations that prevent claims about actual delivery-time performance or operational route efficiency.

## References and Data Sources

Primary data source: Nassau Candy Distributor dataset supplied for this project.

Additional geographical reference coordinates and image sources should be documented with their original source details before final publication.

## Appendix

Generated analytical visualizations are available in `outputs/charts/`.

Technical diagrams are available in `outputs/diagrams/`.

Processed datasets and reports are available in `data/processed/` and `outputs/reports/`.
