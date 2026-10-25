import streamlit as st, plotly.express as px
from src.analysis import load_prices, load_basket, laspeyres

st.set_page_config(page_title="EmergingEcon-DataLab", layout="wide")
st.title("EmergingEcon-DataLab")
st.caption("Open-access micro-inflation tracker for essential goods in Bangladesh "
           "(Laspeyres Price Index, first day = 100)")

try:
    df = load_prices()
    idx, wide = laspeyres(df, load_basket())
except Exception:
    st.warning("No data yet. Run the scraper first.")
    st.stop()

days = len(idx)
last = idx.iloc[-1]
c1, c2, c3, c4 = st.columns(4)
c1.metric("Price Index (first day = 100)", f"{last['index']:.1f}", f"{last['index'] - 100:+.1f} vs first day")
c2.metric("Basket cost (BDT)", f"{last['basket_cost']:,.0f}")
wk = last["weekly_change_pct"]
c3.metric("7-day change", "needs 8+ days" if wk != wk else f"{wk:+.2f}%")
c4.metric("Days of data", days)

if days < 2:
    st.info("Only 1 day of data so far, so each chart shows a single dot. "
            "Trend lines appear from the second day as the daily scraper keeps running.")

idx_plot = idx.reset_index()
idx_plot["date"] = idx_plot["date"].dt.strftime("%d %b %Y")
st.subheader("Price Index over time")
fig1 = px.line(idx_plot, x="date", y="index", markers=True)
fig1.update_xaxes(type="category", title="date")
st.plotly_chart(fig1, width="stretch")

st.subheader("Price trend by commodity")
st.caption("Units: rice, lentils, onion, flour in BDT per kg; soybean oil per litre; eggs per dozen.")
chosen = st.multiselect("Items", list(wide.columns), default=list(wide.columns))
long = wide[chosen].reset_index().melt("date", var_name="item", value_name="price")
long["date"] = long["date"].dt.strftime("%d %b %Y")
fig2 = px.line(long, x="date", y="price", color="item", markers=True)
fig2.update_xaxes(type="category", title="date")
st.plotly_chart(fig2, width="stretch")

with st.expander("Data and limitations"):
    st.write("Source: Chaldal (Dhaka). Prices are what a customer pays, so discounts are included. "
             "Missing items are carried forward. Not a replacement for official CPI.")
st.download_button("Download full dataset (CSV)", df.to_csv(index=False), "emergingecon_prices.csv")