import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd

st.markdown("<h2 style='color:#26a69a;'>Intraday Candlestick Chart</h2>", unsafe_allow_html=True)

with st.sidebar:
    st.header("Intraday Controls")
    ticker = st.text_input("Stock Ticker", value="MSFT", max_chars=5)
    period = st.selectbox("Period", ["5d", "7d", "15d","30d"], index=0)
    interval = "5m"
    st.info("Tip: Intraday data is only available for recent dates.")

@st.cache_data
def load_data(ticker, period, interval):
    return yf.Ticker(ticker).history(period=period, interval=interval)

data = load_data(ticker, period, interval)

with st.container():
    if not data.empty:
        available_dates = sorted(set(data.index.date))
        selected_date = st.sidebar.selectbox("Select Date", options=[str(d) for d in available_dates])
        mask = data.index.date == pd.to_datetime(selected_date).date()
        day_data = data.loc[mask]
        if not day_data.empty:
            fig = go.Figure(data=[go.Candlestick(
                x=day_data.index,
                open=day_data['Open'],
                high=day_data['High'],
                low=day_data['Low'],
                close=day_data['Close'],
                name='Intraday Candlestick',
                increasing_line_color="#017b1b",   
                decreasing_line_color="#97011f",   
                increasing_fillcolor='#1de9b6',    
                decreasing_fillcolor='#ff8a80'     
            )])
            fig.update_layout(
                xaxis_title="Time",
                yaxis_title="Price",
                xaxis_rangeslider_visible=False,
                height=500,
                xaxis=dict(fixedrange=True),
                yaxis=dict(fixedrange=True),
                plot_bgcolor="#f9f9f9",
                font=dict(family="Segoe UI, Arial", size=13, color="black"),
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No intraday data for selected date.")
    else:
        st.info("No intraday data available for selected ticker/period.")