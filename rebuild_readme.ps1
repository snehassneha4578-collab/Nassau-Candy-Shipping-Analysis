$ErrorActionPreference = "Stop"

$root = $PSScriptRoot
Set-Location $root

Write-Host "===== STEP 3.2.13: README REBUILD ====="
Write-Host "Step progress: 0% | Overall progress: 83%"

# 1. Preserve existing README
if (Test-Path ".\README.md") {
    $stamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $backup = ".\README_before_rebuild_$stamp.md"
    Copy-Item ".\README.md" $backup
    Write-Host "[PASS] Backup created: $backup"
}

# 2. Build README content
$lines = @(
"# Factory-to-Customer Shipping Route Efficiency Analysis",
"",
"## Project Overview",
"",
"This project explores factory assignments, customer geography, shipping modes, product distribution, financial patterns, and estimated factory-to-state distances using the Nassau Candy Distributor dataset.",
"",
"## Dataset Overview",
"",
"| Metric | Value |",
"|---|---:|",
"| Product-level records | 10,194 |",
"| Unique orders | 8,549 |",
"| Products | 15 |",
"| Mapped factories | 5 |",
"| Unmapped product records | 0 |",
"| Multi-factory orders | 0 |",
"",
"Product-level records must not be interpreted as unique shipments.",
"",
"## Technology Stack",
"",
"- Python",
"- Pandas",
"- NumPy",
"- Matplotlib",
"- Seaborn",
"- Plotly",
"- Streamlit",
"",
"## Project Workflow",
"",
"1. Dataset inspection and preservation.",
"2. Data cleaning and validation.",
"3. Product-to-factory mapping.",
"4. Geographic distribution analysis.",
"5. Shipping-mode analysis.",
"6. Financial analysis.",
"7. Approximate distance estimation.",
"8. Date-quality investigation.",
"9. Visualization and reporting.",
"",
"## Factory Distribution",
"",
"| Factory | Product records |",
"|---|---:|",
"| Lot's O' Nuts | 5,692 |",
"| Wicked Choccy's | 4,152 |",
"| Secret Factory | 217 |",
"| The Other Factory | 100 |",
"| Sugar Shack | 33 |",
"",
"## Date Quality Investigation",
"",
"| Metric | Observed value |",
"|---|---|",
"| Order Date range | 2024-01-02 to 2025-12-31 |",
"| Ship Date range | 2026-06-30 to 2030-06-28 |",
"| Mean calculated lead time | 1,320.84 days |",
"| Median calculated lead time | 1,274 days |",
"| Lead times above 730 days | All records |",
"",
"The cause of these unusual date patterns is unknown. These dates cannot establish actual shipping delays, transit time, or delivery performance.",
"",
"## Geographic and Route Methodology",
"",
"Factory coordinates and approximate state-centroid coordinates are used to estimate straight-line distances. These are not road distances, actual vehicle routes, or verified customer delivery distances.",
"",
"## Data Visualizations",
""
)

# 3. Include every chart
$chartFiles = Get-ChildItem ".\outputs\charts" -Filter "*.png" -File -ErrorAction SilentlyContinue | Sort-Object Name

foreach ($file in $chartFiles) {
    $relative = "outputs/charts/" + $file.Name
    $heading = [IO.Path]::GetFileNameWithoutExtension($file.Name) -replace '^\d+_', '' -replace '_', ' '
    $lines += "### $heading"
    $lines += ""
    $lines += "![$heading]($relative)"
    $lines += ""
}

# 4. Include diagrams
$lines += "## Project Diagrams"
$lines += ""

$diagramFiles = Get-ChildItem ".\outputs\diagrams" -Filter "*.png" -File -ErrorAction SilentlyContinue | Sort-Object Name

foreach ($file in $diagramFiles) {
    $relative = "outputs/diagrams/" + $file.Name
    $heading = [IO.Path]::GetFileNameWithoutExtension($file.Name) -replace '_', ' '
    $lines += "### $heading"
    $lines += ""
    $lines += "![$heading]($relative)"
    $lines += ""
}

# 5. Remaining documentation
$lines += @(
"## Interactive Streamlit Dashboard",
"",
"Run locally:",
"",
"    pip install -r dashboard/requirements.txt",
"    streamlit run dashboard/app.py",
"",
"## Project Validation",
"",
"Run:",
"",
"    python tests/validate_project.py",
"",
"## Limitations",
"",
"- Product records are not shipment records.",
"- Customer delivery coordinates are unavailable.",
"- Distance estimates are approximate straight-line measurements.",
"- Date anomalies require source-system verification.",
"- Illustrative images do not verify actual company facilities.",
"- Actual delivery performance cannot be established from this dataset.",
"",
"## Future Improvements",
"",
"- Obtain verified customer coordinates.",
"- Integrate road-network routing.",
"- Validate dates against source-system records.",
"- Obtain shipment-level tracking information.",
"- Extend dashboard functionality and automated testing.",
"",
"## Conclusion",
"",
"This project provides an exploratory analysis of factory distribution, customer geography, shipping modes, financial patterns, and approximate geographic relationships in the supplied dataset.",
"",
"**Domain:** Data Analytics | Supply Chain Analytics | Business Intelligence"
)

# 6. Write to temporary file and verify before replacement
$temp = ".\README.generated.tmp"
$lines | Set-Content -Path $temp -Encoding UTF8

if ((Get-Item $temp).Length -lt 1000) {
    throw "Generated README is unexpectedly small."
}

Move-Item -Path $temp -Destination ".\README.md" -Force

Write-Host "[PASS] README generated."
Write-Host "Chart images included: $($chartFiles.Count)"
Write-Host "Diagram images included: $($diagramFiles.Count)"
Write-Host "README size: $((Get-Item .\README.md).Length) bytes"

if ($chartFiles.Count -ge 20 -and $diagramFiles.Count -ge 4) {
    Write-Host "[PASS] Chart and diagram count checks passed."
    Write-Host "Step progress: 100% | Overall progress: 83%"
} else {
    Write-Host "[WARNING] Some expected images may be missing."
    Write-Host "Step progress: incomplete | Overall progress: 83%"
}