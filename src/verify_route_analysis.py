import pandas as pd
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "data" / "processed"
original = pd.read_csv(
    Path(__file__).resolve().parents[1] /
    "data" / "original" / "Nassau Candy Distributor.csv"
)

region = pd.read_csv(p / "factory_to_region_routes.csv")
state = pd.read_csv(p / "factory_to_state_routes.csv")
factory = pd.read_csv(p / "factory_summary.csv")

assert int(region["Record_Count"].sum()) == len(original)
assert int(state["Record_Count"].sum()) == len(original)
assert int(factory["Record_Count"].sum()) == len(original)

assert int(region["Unique_Order_Count"].sum()) >= 0
assert int(state["Unique_Order_Count"].sum()) >= 0
assert factory["Factory"].nunique() == 5

print("PASS: Region route records reconcile to original rows.")
print("PASS: State route records reconcile to original rows.")
print("PASS: Factory totals reconcile to original rows.")
print("PASS: All five mapped factories are represented.")
print("Original rows:", len(original))
print("Region route combinations:", len(region))
print("State route combinations:", len(state))
print("Factory groups:", len(factory))
