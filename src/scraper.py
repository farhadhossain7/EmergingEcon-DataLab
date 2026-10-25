"""Daily price scraper (Playwright) with retries.
Reads config/sources.json and appends to data/master_prices.csv."""
import json, re, logging, datetime as dt
from pathlib import Path
import pandas as pd
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
CSV = ROOT / "data" / "master_prices.csv"
COLS = ["date", "source", "item", "category", "unit", "price"]
TAKA = "\u09f3"
MAX_TRIES = 3
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(),
                              logging.FileHandler(ROOT / "scraper.log", encoding="utf-8")])

def find_price(lines, marker):
    """Find the product name, then the number that follows the taka symbol."""
    for i, line in enumerate(lines):
        if marker.lower() in line.lower():
            for j in range(i + 1, min(i + 8, len(lines))):
                if TAKA in lines[j]:
                    nums = re.findall(r"\d[\d,]*\.?\d*", lines[j])
                    if not nums and j + 1 < len(lines):
                        nums = re.findall(r"\d[\d,]*\.?\d*", lines[j + 1])
                    if nums:
                        return float(nums[0].replace(",", ""))
    return None

def main():
    basket = json.loads((ROOT / "config" / "basket.json").read_text(encoding="utf-8"))["items"]
    sources = json.loads((ROOT / "config" / "sources.json").read_text(encoding="utf-8"))["sources"]
    today, rows = dt.date.today().isoformat(), []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for s in sources:
            if not s.get("enabled", True):
                continue
            price = None
            for attempt in range(1, MAX_TRIES + 1):
                page = None
                try:
                    page = browser.new_page(viewport={"width": 1280, "height": 900})
                    page.route("**/*.{png,jpg,jpeg,gif,webp,svg}", lambda route: route.abort())
                    page.goto(s["url"], timeout=60000, wait_until="domcontentloaded")
                    page.wait_for_selector("text=" + s["marker"], timeout=45000)
                    page.wait_for_timeout(2000)
                    lines = [l.strip() for l in page.inner_text("body").split("\n") if l.strip()]
                    price = find_price(lines, s["marker"])
                    if price is not None:
                        break
                    logging.warning("Attempt %d: no price found for %s", attempt, s["item"])
                except Exception as e:
                    logging.warning("Attempt %d failed for %s: %s", attempt, s["item"],
                                    str(e).splitlines()[0])
                finally:
                    if page:
                        page.close()
            if price is None:
                logging.error("Gave up on %s %s after %d tries", s["name"], s["item"], MAX_TRIES)
                continue
            info = basket[s["item"]]
            per_unit = round(price / s.get("pack_size", 1), 2)
            rows.append([today, s["name"], s["item"], info["category"], info["unit"], per_unit])
            logging.info("OK %s %s: pack price %s -> %s per %s", s["name"], s["item"],
                         price, per_unit, info["unit"])
        browser.close()
    if rows:
        new = pd.DataFrame(rows, columns=COLS)
        old = pd.read_csv(CSV) if CSV.exists() and CSV.stat().st_size > 0 else pd.DataFrame(columns=COLS)
        out = pd.concat([old, new]).drop_duplicates(["date", "source", "item"], keep="last")
        out.to_csv(CSV, index=False)
        logging.info("Saved %d new rows (total %d)", len(new), len(out))
    else:
        logging.warning("No rows collected today.")

if __name__ == "__main__":
    main()