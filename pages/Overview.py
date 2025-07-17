import streamlit as st

st.markdown("<h2 style='color:#26a69a;'>Overview</h2>", unsafe_allow_html=True)
st.markdown("""
This dashboard provides:
- **Candlestick charts** for price and volume
- **Intraday analysis** for minute-level data
- **Summary statistics** for selected stocks

Use the sidebar to select a stock ticker and time period.  
Navigate to other pages for charts and statistics.
""")