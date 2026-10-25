"""Laspeyres Price Index: I_t = sum(p_t * q_0) / sum(p_0 * q_0) * 100
q_0 = fixed base-period basket quantities (config/basket.json)."""
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

def load_prices(path=None):
    return pd.read_csv(path or ROOT / "data" / "master_prices.csv", parse_dates=["date"])

def load_basket():
    return json.loads((ROOT / "config" / "basket.json").read_text(encoding="utf-8"))["items"]

def daily_item_prices(df):
    """Average price per item per day across sources -> wide table (date x item)."""
    wide = df.groupby(["date", "item"])["price"].mean().unstack("item").sort_index()
    return wide.ffill()

def laspeyres(df, basket):
    wide = daily_item_prices(df)
    items = [i for i in basket if i in wide.columns]
    wide = wide[items].dropna()  # only days where the full basket is priced
    q0 = pd.Series({i: basket[i]["base_quantity"] for i in items})
    cost = (wide * q0).sum(axis=1)
    out = pd.DataFrame({"basket_cost": cost, "index": cost / cost.iloc[0] * 100})
    out["weekly_change_pct"] = out["basket_cost"].pct_change(7) * 100
    return out, wide

if __name__ == "__main__":
    idx, _ = laspeyres(load_prices(), load_basket())
    print(idx.tail())
