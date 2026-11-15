from pathlib import Path
import subprocess
import sys
import pandas as pd
import streamlit as st

PROJECT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT / "data" / "processed"
CHART_DIR = PROJECT / "outputs" / "charts"
DIAGRAM_DIR = PROJECT / "outputs" / "diagrams"
IMAGE_DIR = PROJECT / "images"
SRC_DIR = PROJECT / "src"
TEST_FILE = PROJECT / "tests" / "validate_project.py"
LOG_DIR = PROJECT / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)

st.set_page_config(
    page_title="Nassau Candy | Analytics Studio",
    page_icon="🍬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- DESIGN ----------------

st.markdown("""
<style>
:root {
    color-scheme: dark;
    --bg: #160d25;
    --panel: #241333;
    --panel2: #30183f;
    --purple: #9b5de5;
    --pink: #f15bb5;
    --mint: #70e1c1;
    --lavender: #d9c5ff;
    --text: #f2eaff;
    --muted: #b9a8cb;
}
html, body, [data-testid="stAppViewContainer"],
[data-testid="stMain"], [data-testid="stHeader"],
[data-testid="stSidebar"], [data-testid="stBottom"],
[data-testid="stVerticalBlock"], [data-testid="stApp"],
.stApp {
    background: var(--bg) !important;
    color: var(--text) !important;
}
[data-testid="stHeader"] {
    background: #160d25 !important;
}
[data-testid="stSidebar"] > div {
    background: #20102f !important;
}
[data-testid="stSidebar"] * {
    color: var(--lavender) !important;
}
[data-testid="stMainBlockContainer"] {
    background: transparent !important;
}
h1, h2, h3, h4, p, label, span, div {
    color: inherit;
}
h1 {
    color: #f7b2e0 !important;
    letter-spacing: -1px;
}
h2, h3 {
    color: #d9b8ff !important;
}
p, label, .stMarkdown {
    color: var(--text) !important;
}
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #321849, #241333) !important;
    border: 1px solid #74449a !important;
    border-radius: 18px !important;
    padding: 18px !important;
    box-shadow: 0 8px 25px #08040f66 !important;
}
[data-testid="stMetricLabel"] {
    color: #d7b8f5 !important;
}
[data-testid="stMetricValue"] {
    color: #ff9ed8 !important;
}
[data-testid="stMetricDelta"] {
    color: #70e1c1 !important;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #241333 !important;
    border: 1px solid #70428d !important;
    border-radius: 18px !important;
}
.stButton > button, .stDownloadButton > button {
    background: linear-gradient(100deg, #8a3fd1, #d94eaa) !important;
    color: #fff0fb !important;
    border: 1px solid #d98be9 !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    transition: all .2s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background: linear-gradient(100deg, #a855e8, #f15bb5) !important;
    transform: translateY(-2px);
    box-shadow: 0 5px 18px #d94eaa55 !important;
}
input, textarea, [data-baseweb="select"],
[data-baseweb="input"], [data-baseweb="textarea"] {
    background: #30183f !important;
    color: #f2eaff !important;
    border-color: #8652a7 !important;
}
[data-baseweb="popover"], [data-baseweb="menu"],
[data-baseweb="select"] > div {
    background: #30183f !important;
    color: #f2eaff !important;
}
[data-baseweb="menu"] * {
    color: #f2eaff !important;
}
[data-testid="stDataFrame"], [data-testid="stTable"] {
    background: #241333 !important;
}
[data-testid="stDataFrame"] * {
    color: #f2eaff !important;
}
[data-testid="stAlert"] {
    background: #321d43 !important;
    color: #f2eaff !important;
    border: 1px solid #8652a7 !important;
}
[data-testid="stExpander"] {
    background: #241333 !important;
    border: 1px solid #70428d !important;
    border-radius: 14px !important;
}
hr {
    border-color: #70428d !important;
}
a {
    color: #ff9ed8 !important;
}
[data-testid="stImage"] img {
    border: 1px solid #70428d;
    border-radius: 14px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HELPERS ----------------

def metric(label, value):
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div></div>',
        unsafe_allow_html=True
    )

def image_files(folder):
    if not folder.exists():
        return []
    valid = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
    return sorted(
        [p for p in folder.rglob("*") if p.is_file() and p.suffix.lower() in valid],
        key=lambda p: str(p).lower()
    )

def show_gallery(files, columns=2):
    if not files:
        st.info("No image files found in this folder.")
        return
    for start in range(0, len(files), columns):
        cols = st.columns(columns)
        for col, path in zip(cols, files[start:start + columns]):
            with col:
                st.image(str(path), use_container_width=True)
                st.caption(path.relative_to(PROJECT).as_posix())

def run_python_script(script, timeout=900):
    if not script.exists():
        return False, f"Script not found: {script}"

    try:
        result = subprocess.run(
            [sys.executable, str(script)],
            cwd=str(PROJECT),
            capture_output=True,
            text=True,
            timeout=timeout
        )
        output = (result.stdout or "")
        errors = (result.stderr or "")
        combined = output
        if errors:
            combined += "\n--- STDERR ---\n" + errors
        if result.returncode == 0:
            return True, combined or "Script completed without console output."
        return False, f"Exit code: {result.returncode}\n{combined}"
    except subprocess.TimeoutExpired:
        return False, f"Script exceeded the {timeout}-second time limit."
    except Exception as exc:
        return False, str(exc)

def section_heading(title, subtitle):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-sub">{subtitle}</div>', unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------

st.sidebar.markdown("## 🍬 Nassau Candy")
st.sidebar.caption("ANALYTICS STUDIO")
page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Overview",
        "Data Explorer",
        "All Graphs",
        "Technical Diagrams",
        "Image Gallery",
        "Financial Analysis",
        "Route Analysis",
        "Run Analysis",
        "Reports & Validation"
    ]
)

st.sidebar.divider()
st.sidebar.markdown("**Project status**")
st.sidebar.progress(0.83)
st.sidebar.caption("Current verified progress: 83%")
st.sidebar.caption("Local project • No repository required")

# ---------------- FILE INVENTORY ----------------

charts = image_files(CHART_DIR)
diagrams = image_files(DIAGRAM_DIR)
photos = image_files(IMAGE_DIR)
csv_files = sorted(DATA_DIR.glob("*.csv")) if DATA_DIR.exists() else []
scripts = sorted(SRC_DIR.glob("*.py")) if SRC_DIR.exists() else []

# ---------------- HERO ----------------

st.markdown("""
<div class="hero">
  <div class="eyebrow">Supply Chain Intelligence · Data Analytics</div>
  <h1>Nassau Candy Analytics Studio</h1>
  <p>Factory distribution · Customer geography · Financial insights · Route exploration</p>
</div>
""", unsafe_allow_html=True)

# ---------------- OVERVIEW ----------------

if page == "Overview":
    section_heading("Project at a glance", "A consolidated view of the available analysis assets.")

    c1, c2, c3, c4 = st.columns(4)
    with c1: metric("PRODUCT RECORDS", "10,194")
    with c2: metric("UNIQUE ORDERS", "8,549")
    with c3: metric("FACTORIES", "5")
    with c4: metric("PRODUCTS", "15")

    c1, c2, c3 = st.columns(3)
    with c1: metric("ANALYTICAL GRAPHS", len(charts))
    with c2: metric("TECHNICAL DIAGRAMS", len(diagrams))
    with c3: metric("PROJECT PHOTOS", len(photos))

    st.markdown("")
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("### Distribution by factory")
    factory_data = pd.DataFrame({
        "Factory": ["Lot's O' Nuts", "Wicked Choccy's", "Secret Factory",
                    "The Other Factory", "Sugar Shack"],
        "Product records": [5692, 4152, 217, 100, 33]
    })
    st.bar_chart(factory_data.set_index("Factory"))
    st.dataframe(factory_data, hide_index=True, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### Featured project visuals")
    featured = charts[:4]
    show_gallery(featured, columns=2)

    st.warning(
        "Data interpretation safeguard: Order Date and Ship Date contain unusual "
        "patterns and cannot reliably establish actual shipping transit times or delays. "
        "Distance estimates are approximate straight-line estimates, not road distances."
    )

# ---------------- DATA EXPLORER ----------------

elif page == "Data Explorer":
    section_heading("Data Explorer", "Inspect the processed datasets generated by the project.")

    if not csv_files:
        st.warning("No processed CSV files found in data/processed.")
    else:
        selected = st.selectbox("Choose a processed dataset", csv_files,
                                format_func=lambda p: p.name)
        try:
            df = pd.read_csv(selected)
            a, b, c = st.columns(3)
            with a: metric("ROWS", f"{len(df):,}")
            with b: metric("COLUMNS", len(df.columns))
            with c: metric("MISSING CELLS", f"{int(df.isna().sum().sum()):,}")

            st.markdown("### Dataset preview")
            st.dataframe(df.head(500), use_container_width=True)

            st.markdown("### Column information")
            info = pd.DataFrame({
                "Column": df.columns,
                "Data type": [str(x) for x in df.dtypes],
                "Missing values": [int(df[c].isna().sum()) for c in df.columns],
                "Unique values": [int(df[c].nunique(dropna=True)) for c in df.columns]
            })
            st.dataframe(info, hide_index=True, use_container_width=True)

            numeric = df.select_dtypes(include="number").columns.tolist()
            if numeric:
                st.markdown("### Explore a numeric field")
                field = st.selectbox("Numeric column", numeric)
                st.bar_chart(df[field].dropna().reset_index(drop=True))
        except Exception as exc:
            st.error(f"Could not read dataset: {exc}")

# ---------------- ALL GRAPHS ----------------

elif page == "All Graphs":
    section_heading("Complete Graph Gallery", f"All {len(charts)} available analytical graphs.")

    if charts:
        search = st.text_input("Search graph by filename")
        filtered = [p for p in charts if search.lower() in p.name.lower()]
        st.caption(f"Showing {len(filtered)} of {len(charts)} graphs")
        show_gallery(filtered, columns=2)
    else:
        st.warning("No graphs found in outputs/charts.")

# ---------------- DIAGRAMS ----------------

elif page == "Technical Diagrams":
    section_heading("Technical Diagrams", f"All {len(diagrams)} project diagrams.")
    show_gallery(diagrams, columns=2)

# ---------------- IMAGE GALLERY ----------------

elif page == "Image Gallery":
    section_heading("Project Image Gallery", f"All {len(photos)} images under the images folder.")

    if photos:
        categories = sorted(set(p.parent.relative_to(IMAGE_DIR).as_posix() for p in photos))
        selected_category = st.selectbox("Image category", ["All categories"] + categories)
        if selected_category == "All categories":
            selected_photos = photos
        else:
            selected_photos = [
                p for p in photos
                if p.parent.relative_to(IMAGE_DIR).as_posix() == selected_category
            ]
        st.caption(f"Showing {len(selected_photos)} images")
        show_gallery(selected_photos, columns=3)
    else:
        st.info("No photographs found under images/.")

# ---------------- FINANCIAL ANALYSIS ----------------

elif page == "Financial Analysis":
    section_heading("Financial Analysis", "Explore available factory and regional financial summaries.")

    candidates = [
        p for p in csv_files
        if "factory_summary" in p.name.lower()
        or "regional_summary" in p.name.lower()
        or "shipping_mode_summary" in p.name.lower()
    ]

    if not candidates:
        st.warning("No matching financial summary CSV files were found.")
    else:
        selected = st.selectbox("Choose summary", candidates,
                                format_func=lambda p: p.name)
        df = pd.read_csv(selected)
        st.dataframe(df, use_container_width=True)

        numeric = df.select_dtypes(include="number").columns.tolist()
        if numeric:
            field = st.selectbox("Choose metric to chart", numeric)
            labels = df.select_dtypes(exclude="number").columns.tolist()
            if labels:
                label = st.selectbox("Choose category", labels)
                plot_df = df[[label, field]].dropna().set_index(label)
                st.bar_chart(plot_df)

    st.info("Financial summaries describe the supplied dataset; they are not independently audited business results.")

# ---------------- ROUTE ANALYSIS ----------------

elif page == "Route Analysis":
    section_heading("Geographical & Route Analysis", "Explore estimated factory-to-state and regional outputs.")

    candidates = [
        p for p in csv_files
        if "distance" in p.name.lower()
        or "route" in p.name.lower()
        or "region" in p.name.lower()
    ]

    if candidates:
        selected = st.selectbox("Choose route dataset", candidates,
                                format_func=lambda p: p.name)
        df = pd.read_csv(selected)
        st.dataframe(df.head(1000), use_container_width=True)
        st.caption(f"{len(df):,} rows · {len(df.columns)} columns")
    else:
        st.warning("No route or distance datasets found.")

    route_charts = [
        p for p in charts
        if any(word in p.name.lower() for word in ["route", "distance", "network", "flow", "region"])
    ]
    st.markdown("### Related route visuals")
    show_gallery(route_charts, columns=2)

    st.warning(
        "Distance outputs use approximate geographical reference coordinates and "
        "straight-line estimates. They do not represent road distances or verified delivery routes."
    )

# ---------------- RUN ANALYSIS ----------------

elif page == "Run Analysis":
    section_heading("Analysis Control Center", "Run project Python scripts manually and inspect their output.")

    st.warning(
        "Scripts are executed only when you press a Run button. "
        "Review a script before running it if you are unsure what it changes."
    )

    if not scripts:
        st.warning("No Python scripts found in src/.")
    else:
        st.markdown(f"### Available scripts ({len(scripts)})")
        for script in scripts:
            with st.container(border=True):
                st.markdown(f"**{script.name}**")
                st.caption(f"Location: {script.relative_to(PROJECT).as_posix()}")

                if st.button(f"▶ Run {script.stem}", key=f"run_{script.name}"):
                    with st.spinner(f"Running {script.name}..."):
                        success, output = run_python_script(script)
                    st.session_state[f"result_{script.name}"] = {
                        "success": success,
                        "output": output
                    }

                result = st.session_state.get(f"result_{script.name}")
                if result:
                    if result["success"]:
                        st.success("Execution completed.")
                    else:
                        st.error("Execution failed. Review the output.")
                    st.code(result["output"][-12000:] or "No output", language="text")

    st.divider()
    st.markdown("### Project validation")
    if st.button("🧪 Run project validation", type="primary"):
        if not TEST_FILE.exists():
            st.error("Validation script not found at tests/validate_project.py.")
        else:
            with st.spinner("Validating project files and datasets..."):
                success, output = run_python_script(TEST_FILE, timeout=300)
            st.session_state["validation_result"] = {
                "success": success,
                "output": output
            }

    validation = st.session_state.get("validation_result")
    if validation:
        if validation["success"]:
            st.success("Validation completed successfully.")
        else:
            st.error("Validation reported a failure.")
        st.code(validation["output"][-12000:], language="text")

# ---------------- REPORTS ----------------

elif page == "Reports & Validation":
    section_heading("Reports & Validation", "Inspect project reports and validation output.")

    report_dir = PROJECT / "outputs" / "reports"
    reports = sorted(report_dir.glob("*")) if report_dir.exists() else []
    if reports:
        chosen = st.selectbox("Select report", reports,
                              format_func=lambda p: p.name)
        if chosen.suffix.lower() in [".json", ".txt", ".md", ".log", ".csv"]:
            try:
                if chosen.suffix.lower() == ".csv":
                    st.dataframe(pd.read_csv(chosen), use_container_width=True)
                else:
                    st.code(chosen.read_text(encoding="utf-8", errors="replace")[:30000])
            except Exception as exc:
                st.error(str(exc))
        else:
            st.info("This report format is not previewed in the app.")
    else:
        st.info("No reports found.")

    st.markdown("### Project inventory")
    inventory = pd.DataFrame([
        {"Asset type": "Processed CSV files", "Count": len(csv_files)},
        {"Asset type": "Analytical graphs", "Count": len(charts)},
        {"Asset type": "Technical diagrams", "Count": len(diagrams)},
        {"Asset type": "Project images", "Count": len(photos)},
        {"Asset type": "Python source scripts", "Count": len(scripts)}
    ])
    st.dataframe(inventory, hide_index=True, use_container_width=True)

# ---------------- FOOTER ----------------

st.divider()
st.markdown(
    "<div style='text-align:center;color:#89839b;font-size:12px;'>"
    "Nassau Candy Analytics Studio · Local project dashboard · "
    "Exploratory analysis with documented data limitations"
    "</div>",
    unsafe_allow_html=True
)
