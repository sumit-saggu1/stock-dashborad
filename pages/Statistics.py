import streamlit as st
import yfinance as yf
import pandas as pd



with st.sidebar:
    st.header("Statistics Controls")
    ticker = st.text_input("Stock Ticker", value="MSFT", max_chars=5)
    period = st.selectbox("Period", ["1d", "5d", "7d", "1mo", "3mo", "6mo", "1y"], index=3)
    interval = st.selectbox("Interval", ["1d", "1wk", "1mo"], index=0)
    st.info("Tip: Use a longer period for more robust statistics.")
st.markdown(f"<h2 style='color:#26a69a;'>{ticker} Summary Statistics</h2>", unsafe_allow_html=True)
@st.cache_data
def load_data(ticker, period, interval):
    return yf.Ticker(ticker).history(period=period, interval=interval)

data = load_data(ticker, period, interval)

with st.container():
    if not data.empty:
        st.dataframe(data.describe(), use_container_width=True)
    else:
        st.warning("No data available for selected ticker/period.")
