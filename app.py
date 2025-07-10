import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd
from plotly.subplots import make_subplots

st.title("📈 Stock Analysis Dashboard")

# Sidebar for user input
ticker = st.sidebar.text_input("Enter Stock Ticker", value="MSFT", max_chars=5)
period = st.sidebar.selectbox("Select Period", ["1d", "5d", "7d", "15d", "45d", "59d", "1y", "2y", "5y"],index=5)
# Only show minute intervals for short periods
if period in ["1d", "5d", "7d"]:
    interval = st.sidebar.selectbox("Select Interval", ["30m","1h", "1d" ],index=1   )
else:
    interval = st.sidebar.selectbox("Select Interval", ["1d", "1wk", "1mo"], index=0)

# Fetch data
@st.cache_data
def load_data(ticker, period, interval):
    data = yf.Ticker(ticker).history(period=period, interval=interval)
    return data

@st.cache_data
def get_live_price(ticker):
    ticker_obj = yf.Ticker(ticker)
    info = ticker_obj.fast_info
    price = info.get("last_price", None)
    currency = info.get("currency", "USD")
    return price, currency

data = load_data(ticker, period, interval)

# Show current status and live price at the top
if ticker and data is not None and not data.empty:
    currency = get_live_price(ticker)
    st.subheader(f"{ticker} Price Data")
    st.dataframe(data.tail())

    # Plot closing price
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close'))
    fig.update_layout(
        title=f"{ticker} Closing Price",
        xaxis_title="Date",
        yaxis_title=f"Price ({currency[1]})",
        xaxis=dict(fixedrange=True),  # Lock x-axis: disables zoom, pan, and selection
        yaxis=dict(fixedrange=True)   # Lock y-axis: disables zoom, pan, and selection
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Moving Average
    window = st.sidebar.slider("Moving Average Window", 2, 30, 5)
    data['MA'] = data['Close'].rolling(window=window).mean()
    fig_ma = go.Figure()
    fig_ma.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close'))
    fig_ma.add_trace(go.Scatter(x=data.index, y=data['MA'], mode='lines', name=f'MA{window}'))
    fig_ma.update_layout(
        title=f"{ticker} Closing Price & {window}-Day Moving Average",
        xaxis_title="Date",
        yaxis_title=f"Price ({currency[1]})",
        xaxis=dict(fixedrange=True),  # Lock x-axis: disables zoom, pan, and selection
        yaxis=dict(fixedrange=True)   # Lock y-axis: disables zoom, pan, and selection
    )
    st.plotly_chart(fig_ma, use_container_width=True, config={"displayModeBar": False})

    # --- Candlestick Chart with Volume and Enhanced Layout ---
    st.subheader(f"📊 {ticker.upper()} Candlestick Chart with Volume")

    fig_candle = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.02,
        row_heights=[0.7, 0.3],
        subplot_titles=(f"{ticker.upper()} Price Movement", "Volume Traded"),
        specs=[[{"secondary_y": False}], [{"secondary_y": False}]]
    )

    # Candlestick trace
    fig_candle.add_trace(
        go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='Candlestick',
            increasing_line_color='#26a69a',
            decreasing_line_color="#a50f0f",
            increasing_fillcolor='#b2dfdb',
            decreasing_fillcolor='#ffcdd2',
            showlegend=False
        ),
        row=1, col=1
    )

    # Volume trace
    fig_candle.add_trace(
        go.Bar(
            x=data.index,
            y=data['Volume'],
            marker_color=['#26a69a' if o < c else '#ef5350' for o, c in zip(data['Open'], data['Close'])],
            name='Volume',
            opacity=0.5,
            showlegend=False
        ),
        row=2, col=1
    )

    fig_candle.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1d", step="day", stepmode="backward"),
                    dict(count=5, label="5d", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date",
            showline=True, linewidth=1, linecolor='gray'
        ),
        yaxis=dict(
            title=dict(text=f"Price ({currency[1]})", font=dict(color='black')),
            showline=True, linewidth=1, linecolor='gray',
            tickfont=dict(color='black'),
            fixedrange=True  # Lock the y-axis: disables zoom, pan, and selection
        ),
        yaxis2=dict(
            title=dict(text="Volume", font=dict(color='black')),
            showline=True, linewidth=1, linecolor='gray',
            tickfont=dict(color='black'),
            fixedrange=True  # Lock the y-axis2 as well
        ),
        hovermode="x unified",
        plot_bgcolor="#f9f9f9",
        paper_bgcolor="#f9f9f9",
        font=dict(family="Segoe UI, Arial", size=13, color="black"),
        height=650,
        margin=dict(t=60, b=40, l=10, r=10),
        title=dict(
            text=f"{ticker.upper()} Candlestick Chart with Volume",
            x=0.5,
            font=dict(size=22, color="#333", family="Segoe UI, Arial")
        )
    )

    st.plotly_chart(fig_candle, use_container_width=True, config={"displayModeBar": False})

    # Basic stats
    st.subheader("Summary Statistics")
    st.write(data.describe())

    # Add this after loading data and before plotting charts
    if not data.empty and interval == "1d":
        # If user wants intraday, fetch 1h data for the selected period
        intraday_data = yf.Ticker(ticker).history(period=period, interval="5m")
        if not intraday_data.empty:
            # Let user pick a date from available intraday data
            available_dates = pd.to_datetime(intraday_data.index.date).unique()
            selected_date = st.sidebar.selectbox(
                "Select Date for Intraday Candlestick",
                options=available_dates.astype(str)
            )
            # Filter intraday data for the selected date
            mask = pd.to_datetime(intraday_data.index.date) == pd.to_datetime(selected_date)
            day_data = intraday_data.loc[mask]
            if not day_data.empty:
                st.subheader(f"{ticker} Intraday Candlestick Chart for {selected_date}")
                fig_intraday = go.Figure(data=[go.Candlestick(
                    x=day_data.index,
                    open=day_data['Open'],
                    high=day_data['High'],
                    low=day_data['Low'],
                    close=day_data['Close'],
                    name='Intraday Candlestick'
                )])
                fig_intraday.update_layout(
                    xaxis_title="Time",
                    yaxis_title=f"Price ({currency[1]})",
                    xaxis_rangeslider_visible=False,
                    height=500,
                    xaxis=dict(fixedrange=True),  # Lock x-axis: disables zoom, pan, and selection
                    yaxis=dict(fixedrange=True)   # Lock y-axis: disables zoom, pan, and selection
                )
                st.plotly_chart(fig_intraday, use_container_width=True, config={"displayModeBar": False})
            else:
                st.info("No intraday data available for the selected date.")
