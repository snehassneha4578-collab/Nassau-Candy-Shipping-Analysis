import pandas as pd
import numpy as np
import json
from pathlib import Path
from datetime import datetime

project = Path(__file__).resolve().parents[1]
source = project / "data" / "original" / "Nassau Candy Distributor.csv"
report_dir = project / "outputs" / "reports"
report_dir.mkdir(parents=True, exist_ok=True)

print("\nLoading original dataset...")
df = pd.read_csv(source)

print("\n========== DATASET OVERVIEW ==========")
print("Rows:", len(df))
print("Columns:", len(df.columns))
print("Column names:")
for col in df.columns:
    print(" -", repr(col))

print("\n========== DATA TYPES ==========")
print(df.dtypes.to_string())

print("\n========== MISSING VALUES ==========")
missing = df.isna().sum()
print(missing.to_string())
print("Total missing cells:", int(missing.sum()))

print("\n========== DUPLICATE RECORDS ==========")
print("Exact duplicate rows:", int(df.duplicated().sum()))
if "Row ID" in df.columns:
    print("Duplicate Row IDs:", int(df["Row ID"].duplicated().sum()))

print("\n========== DATE INVESTIGATION ==========")
date_report = {}

for col in ["Order Date", "Ship Date"]:
    if col in df.columns:
        parsed = pd.to_datetime(df[col], format="%d-%m-%Y", errors="coerce")
        invalid = int(parsed.isna().sum())
        date_report[col] = {
            "invalid_dates": invalid,
            "minimum": str(parsed.min()) if parsed.notna().any() else None,
            "maximum": str(parsed.max()) if parsed.notna().any() else None
        }
        print(f"\n{col}")
        print("Invalid dates:", invalid)
        print("Minimum:", parsed.min())
        print("Maximum:", parsed.max())

if all(c in df.columns for c in ["Order Date", "Ship Date"]):
    order = pd.to_datetime(df["Order Date"], format="%d-%m-%Y", errors="coerce")
    ship = pd.to_datetime(df["Ship Date"], format="%d-%m-%Y", errors="coerce")
    lead = (ship - order).dt.days

    valid = lead.dropna()
    negative = int((valid < 0).sum())
    zero = int((valid == 0).sum())
    positive = valid[valid > 0]

    print("\nShipping lead time in days:")
    print("Valid date pairs:", int(lead.notna().sum()))
    print("Negative lead times:", negative)
    print("Zero-day lead times:", zero)
    print("Positive lead times:", len(positive))

    if len(valid):
        print("Minimum:", int(valid.min()))
        print("Maximum:", int(valid.max()))
        print("Mean:", round(float(valid.mean()), 2))
        print("Median:", round(float(valid.median()), 2))
        print("25th percentile:", float(valid.quantile(0.25)))
        print("75th percentile:", float(valid.quantile(0.75)))

    print("\nLead-time frequency:")
    print(pd.cut(
        lead,
        bins=[-np.inf, -1, 0, 7, 30, 90, 180, 365, 730, np.inf],
        labels=[
            "Negative", "Zero", "1-7 days", "8-30 days",
            "31-90 days", "91-180 days", "181-365 days",
            "366-730 days", "Over 730 days"
        ]
    ).value_counts(sort=False).to_string())

    date_report["lead_time_days"] = {
        "valid_pairs": int(lead.notna().sum()),
        "negative": negative,
        "zero": zero,
        "minimum": int(valid.min()) if len(valid) else None,
        "maximum": int(valid.max()) if len(valid) else None,
        "mean": round(float(valid.mean()), 2) if len(valid) else None,
        "median": float(valid.median()) if len(valid) else None
    }

    print("\nSample records with longest lead times:")
    sample = df.loc[lead.nlargest(10).index].copy()
    sample["Calculated Lead Time"] = lead.loc[sample.index]
    cols = [c for c in [
        "Row ID", "Order ID", "Order Date", "Ship Date",
        "Ship Mode", "State/Province", "Product Name",
        "Calculated Lead Time"
    ] if c in sample.columns]
    print(sample[cols].to_string(index=False))

print("\n========== CATEGORY INVESTIGATION ==========")

category_report = {}

for col in [
    "Ship Mode", "Country/Region", "Division",
    "Region", "State/Province", "Product Name"
]:
    if col in df.columns:
        counts = df[col].value_counts(dropna=False)
        category_report[col] = {
            str(k): int(v) for k, v in counts.items()
        }
        print(f"\n{col} - unique values: {df[col].nunique(dropna=True)}")
        print(counts.head(30).to_string())

print("\n========== NUMERIC DATA ==========")
numeric = df.select_dtypes(include="number")
if not numeric.empty:
    print(numeric.describe().round(2).to_string())

print("\n========== REPORT GENERATION ==========")

summary = {
    "generated_at": datetime.now().isoformat(timespec="seconds"),
    "dataset_file": source.name,
    "row_count": int(len(df)),
    "column_count": int(len(df.columns)),
    "columns": list(df.columns),
    "missing_values": {str(k): int(v) for k, v in missing.items()},
    "exact_duplicate_rows": int(df.duplicated().sum()),
    "date_analysis": date_report,
    "category_counts": category_report
}

json_path = report_dir / "initial_data_quality_report.json"
text_path = report_dir / "initial_data_quality_report.txt"

json_path.write_text(
    json.dumps(summary, indent=4, default=str),
    encoding="utf-8"
)

with text_path.open("w", encoding="utf-8") as f:
    f.write("NASSAU CANDY - INITIAL DATA QUALITY REPORT\n")
    f.write("=" * 50 + "\n")
    f.write(f"Rows: {len(df)}\n")
    f.write(f"Columns: {len(df.columns)}\n")
    f.write(f"Missing cells: {int(missing.sum())}\n")
    f.write(f"Duplicate rows: {int(df.duplicated().sum())}\n")
    f.write("\nCOLUMN NAMES\n")
    f.write("\n".join(map(str, df.columns)))
    f.write("\n\nDATE ANALYSIS\n")
    f.write(json.dumps(date_report, indent=4, default=str))
    f.write("\n\nCATEGORY COUNTS\n")
    f.write(json.dumps(category_report, indent=4, default=str))

print("Created:", json_path)
print("Created:", text_path)
print("\nDATASET INSPECTION COMPLETED.")
