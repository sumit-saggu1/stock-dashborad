import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
from plotly.subplots import make_subplots

with st.sidebar:
    st.header("Chart Controls")
    ticker = st.text_input("Stock Ticker", value="MSFT", max_chars=5, help="Enter a valid stock symbol")
    period = st.selectbox("Period", ["1d", "5d", "7d", "1mo", "3mo", "6mo", "1y"], index=3)
    interval = st.selectbox("Interval", ["1d", "1wk", "1mo"], index=0)
    st.info("Tip: Use a short period for more detailed candles.")

@st.cache_data
def load_data(ticker, period, interval):
    return yf.Ticker(ticker).history(period=period, interval=interval)

data = load_data(ticker, period, interval)
def get_live_price(ticker):
    ticker_obj = yf.Ticker(ticker)
    info = ticker_obj.fast_info
    price = info.get("last_price", None)
    currency = info.get("currency", "USD")
    return price, currency

with st.container():
    if not data.empty:
        currency = get_live_price(ticker)
        st.markdown(f"<h2 style='color:#26a69a;'>{ticker} Candlestick Chart</h2>", unsafe_allow_html=True)

        fig = make_subplots(
            rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02,
            row_heights=[0.7, 0.3]
        )
        fig.add_trace(go.Candlestick(
            x=data.index, open=data['Open'], high=data['High'],
            low=data['Low'], close=data['Close'], name='Candlestick',
            increasing_line_color="#03631B", decreasing_line_color="#930301"
        ), row=1, col=1)
        fig.add_trace(go.Bar(
            x=data.index, y=data['Volume'], name='Volume', opacity=0.5,
            marker_color="#009c8f"
        ), row=2, col=1)
        fig.update_layout(
            height=600,
            xaxis=dict(
                fixedrange=True,
                tickfont=dict(color="white", size=12, family="Segoe UI, Arial"),
                showline=True,
                linecolor="#333",
                showgrid=True,
                gridcolor="#e0e0e0"
            ),
            xaxis2=dict(  # Set the x-axis title for the bottom subplot
                title="Date",

                tickfont=dict(color="white", size=12, family="Segoe UI, Arial"),
                showline=True,
                linecolor="#333",
                showgrid=True,
                gridcolor="#e0e0e0"
            ),
            yaxis=dict(fixedrange=True),
            yaxis2=dict(fixedrange=True),
            showlegend=False,
            yaxis_title=f"Price ({currency[1]})",
            plot_bgcolor="#f9f9f9",
            font=dict(family="Segoe UI, Arial", size=13, color="black"),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.warning("No data available for selected ticker/period.")