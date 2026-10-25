import streamlit as st, plotly.express as px
from src.analysis import load_prices, load_basket, laspeyres

st.set_page_config(page_title="EmergingEcon-DataLab", layout="wide")
st.title("EmergingEcon-DataLab")
st.caption("Open-access micro-inflation tracker for essential goods (Laspeyres Price Index, base = 100)")

try:
    df = load_prices()
    idx, wide = laspeyres(df, load_basket())
except Exception:
    st.warning("No data yet. Run the scraper (or src/make_demo_data.py for a demo).")
    st.stop()

last = idx.iloc[-1]
c1, c2, c3 = st.columns(3)
c1.metric("Price Index (base=100)", f"{last['index']:.1f}", f"{last['index'] - 100:+.1f} vs base")
c2.metric("Basket cost (BDT)", f"{last['basket_cost']:,.0f}")
wk = last["weekly_change_pct"]
c3.metric("7-day change", "n/a" if wk != wk else f"{wk:+.2f}%")

st.subheader("Price Index over time")
st.plotly_chart(px.line(idx.reset_index(), x="date", y="index"), use_container_width=True)

st.subheader("Price trend by commodity")
chosen = st.multiselect("Items", list(wide.columns), default=list(wide.columns))
st.plotly_chart(px.line(wide[chosen].reset_index().melt("date"), x="date", y="value", color="item"),
                use_container_width=True)

st.download_button("Download full dataset (CSV)", df.to_csv(index=False), "emergingecon_prices.csv")
