"""Creates SYNTHETIC demo data so you can test the dashboard before real scraping works.
NEVER publish this as real data. Run: python src/make_demo_data.py"""
from pathlib import Path
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parent.parent
start = {"Rice": 62, "Soybean Oil": 180, "Lentils": 130, "Onion": 70, "Flour": 58, "Eggs": 140}
cat = {"Rice": "Grains", "Soybean Oil": "Oil", "Lentils": "Pulses", "Onion": "Veg", "Flour": "Grains", "Eggs": "Protein"}
unit = {"Rice": "kg", "Soybean Oil": "litre", "Lentils": "kg", "Onion": "kg", "Flour": "kg", "Eggs": "dozen"}
rng = np.random.default_rng(1)
rows = []
for src in ["DEMO-A", "DEMO-B"]:
    for item, p in start.items():
        price = p
        for d in pd.date_range(end=pd.Timestamp.today().normalize(), periods=60):
            price *= 1 + rng.normal(0.001, 0.01)
            rows.append([d.date(), src, item, cat[item], unit[item], round(price, 2)])
pd.DataFrame(rows, columns=["date", "source", "item", "category", "unit", "price"]).to_csv(
    ROOT / "data" / "master_prices.csv", index=False)
print("Demo data written (SYNTHETIC).")
