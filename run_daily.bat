@echo off
cd /d "%~dp0"
python src\scraper.py
git add data/master_prices.csv
git commit -m "Daily data update"
git push