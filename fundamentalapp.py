
import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def get_stock_data(symbol, start_date, end_date):
    stock_data = yf.download(symbol, start=start_date, end=end_date)
    return stock_data

def plot_technical_analysis(stock_data):
    plt.figure(figsize=(10, 6))
    plt.plot(stock_data['Close'], label="Close Price")
    plt.plot(stock_data['Close'].rolling(window=20).mean(), label="20-day SMA")
    plt.plot(stock_data['Close'].rolling(window=50).mean(), label="50-day SMA")
    plt.title("Technical Analysis")
    plt.legend()
    st.pyplot(plt)

def display_fundamental_data(stock):
    st.subheader("Fundamental Analysis")
    st.write(f"**Market Cap:** {stock.info['marketCap']}")
    st.write(f"**P/E Ratio:** {stock.info['trailingPE']}")
    st.write(f"**EPS:** {stock.info['trailingEps']}")
    st.write(f"**Dividend Yield:** {stock.info['dividendYield']}")

st.title("Stock Analysis App")
st.sidebar.header("Input Options")

# User Inputs
stock_symbol = st.sidebar.text_input("Enter Stock Symbol (BSE/NSE):", "RELIANCE.BO")
start_date = st.sidebar.date_input("Start Date", value=pd.Timestamp("2022-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.Timestamp.today())

if st.sidebar.button("Get Analysis"):
    try:
        # Fetch stock data
        stock_data = get_stock_data(stock_symbol, start_date, end_date)
        stock = yf.Ticker(stock_symbol)

        # Display stock data
        st.subheader(f"Stock Data: {stock_symbol}")
        st.line_chart(stock_data['Close'])

        # Display fundamental data
        display_fundamental_data(stock)

        # Technical analysis
        st.subheader("Technical Analysis")
        plot_technical_analysis(stock_data)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
