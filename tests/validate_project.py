from pathlib import Path
import hashlib
import json
import pandas as pd

PROJECT = Path(__file__).resolve().parents[1]

def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def main():
    checks = []

    required = [
        "README.md",
        "executive_summary/EXECUTIVE_SUMMARY.md",
        "research_paper/RESEARCH_PAPER.md",
        "dashboard/app.py",
        "dashboard/requirements.txt",
    ]

    for relative in required:
        exists = (PROJECT / relative).is_file()
        checks.append({
            "check": f"Required file: {relative}",
            "passed": exists
        })

    processed = PROJECT / "data" / "processed"
    csv_files = sorted(processed.glob("*.csv")) if processed.exists() else []

    checks.append({
        "check": "Processed CSV files available",
        "passed": len(csv_files) > 0,
        "count": len(csv_files)
    })

    for csv_path in csv_files:
        try:
            frame = pd.read_csv(csv_path)
            valid = len(frame.columns) > 0
            checks.append({
                "check": f"CSV readable: {csv_path.name}",
                "passed": valid,
                "rows": len(frame),
                "columns": len(frame.columns),
                "sha256": sha256(csv_path)
            })
        except Exception as error:
            checks.append({
                "check": f"CSV readable: {csv_path.name}",
                "passed": False,
                "error": str(error)
            })

    charts = list((PROJECT / "outputs" / "charts").glob("*.png")) \
        if (PROJECT / "outputs" / "charts").exists() else []

    diagrams = list((PROJECT / "outputs" / "diagrams").glob("*.png")) \
        if (PROJECT / "outputs" / "diagrams").exists() else []

    checks.append({
        "check": "Chart images available",
        "passed": len(charts) > 0,
        "count": len(charts)
    })

    checks.append({
        "check": "Technical diagrams available",
        "passed": len(diagrams) > 0,
        "count": len(diagrams)
    })

    report = {
        "project": "Nassau Candy Shipping Analysis",
        "checks_passed": sum(item["passed"] for item in checks),
        "checks_total": len(checks),
        "all_passed": all(item["passed"] for item in checks),
        "results": checks
    }

    output = PROJECT / "outputs" / "reports" / "final_validation_report.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(json.dumps(report, indent=2))

    if not report["all_passed"]:
        raise SystemExit("VALIDATION FAILED. Review the report.")

    print("\nVALIDATION PASSED")

if __name__ == "__main__":
    main()
