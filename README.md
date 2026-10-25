# EmergingEcon-DataLab
Open-access micro-inflation tracker for essential goods in Bangladesh.

**Live dashboard:** https://emergingecon-datalab.streamlit.app
**Kaggle dataset:** coming soon

## What it does
Every day a Python scraper (Playwright) reads the price of six staple goods
(rice, soybean oil, lentils, onion, flour, eggs) from Chaldal, converts each
to a price per kg / litre / dozen, and stores it in `data/master_prices.csv`.
`src/analysis.py` turns these prices into a Laspeyres Price Index (base day = 100).

## Index formula
I_t = sum(p_t * q_0) / sum(p_0 * q_0) * 100
where q_0 is a fixed basket of quantities (`config/basket.json`).

## Data dictionary
| column | meaning |
|---|---|
| date | day of collection (YYYY-MM-DD) |
| source | website the price came from |
| item | basket item |
| category | Grains, Oil, Pulses, Veg, Protein |
| unit | kg, litre or dozen |
| price | price in BDT per unit |

## Limitations (please read)
- One source (Chaldal, Dhaka delivery area). Prices differ by area and shop.
- Prices are what a customer pays, so temporary discounts are included.
- Basket quantities are illustrative assumptions, not from a household survey.
- The scraper runs on my own computer (Chaldal blocks cloud servers), so days
  are missed when the computer is off. Missing items are carried forward.
- This is a learning and research tool, not a replacement for official CPI.

## Run locally
    pip install -r requirements.txt
    python -m playwright install chromium
    python src/scraper.py
    streamlit run app.py

## License
MIT