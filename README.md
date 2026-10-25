# EmergingEcon-DataLab
Open-access micro-inflation tracker for essential goods in Bangladesh.
Daily prices are collected, turned into a Laspeyres Price Index, and shared as an open dataset.

**Live dashboard:** PASTE-STREAMLIT-LINK-HERE
**Kaggle dataset:** PASTE-KAGGLE-LINK-HERE

## How it works
`scraper.py` (daily via GitHub Actions) -> `data/master_prices.csv` -> `analysis.py` (index) -> `app.py` (dashboard)

## Index formula
I_t = sum(p_t * q_0) / sum(p_0 * q_0) * 100, where q_0 is a fixed basket (config/basket.json).

## Run locally
```
pip install -r requirements.txt
python src/scraper.py
streamlit run app.py
```

## Data dictionary
date, source (website), item, category, unit, price (BDT per unit)

## Limitations
Small basket, few sources; not a replacement for official CPI.
