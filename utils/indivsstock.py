import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Streamlit UI Title
st.title("BSE Sensex vs Other Indices")

# Select date range
start_date = st.date_input("Start Date", value=pd.to_datetime("2023-01-01"))
end_date = st.date_input("End Date", value=pd.to_datetime("2024-03-08"))

# Define tickers
ticker_bse = "^BSESN"      # BSE Sensex
ticker_nse = "^NSEI"       # NSE Nifty 50
ticker_stock = "ITC.NS"    # Individual Stock (ITC)

# Fetch data
data = yf.download(ticker_bse, start=start_date, end=end_date)["Close"]
data1 = yf.download(ticker_nse, start=start_date, end=end_date)["Close"]
data2 = yf.download(ticker_stock, start=start_date, end=end_date)["Close"]

# Combine data into a single DataFrame
df = pd.concat([data, data1, data2], axis=1)
df.columns = ["Sensex", "Nifty 50", "Stock"]  # Rename columns
df = df.dropna()  # Drop rows with missing values


# Create Matplotlib figure and axes
fig, ax1 = plt.subplots(figsize=(10, 5))

# First Y-Axis (Sensex)
ax1.plot(df.index, df["Sensex"], label="Sensex (BSE)", color="blue")
ax1.set_ylabel("Sensex Value", color="blue")
ax1.tick_params(axis='y', labelcolor="blue")
ax1.grid(True)

# Second Y-Axis (Nifty 50)
ax2 = ax1.twinx()
ax2.plot(df.index, df["Nifty 50"], label="Nifty 50 (NSE)", color="red")
ax2.set_ylabel("Nifty 50 Value", color="red")
ax2.tick_params(axis='y', labelcolor="red")

# Third Y-Axis (Stock)
ax3 = ax1.twinx()
ax3.spines['right'].set_position(('outward', 60))  # Offset third axis
ax3.plot(df.index, df["Stock"], label="Stock (ITC)", color="green")
ax3.set_ylabel("Stock Price", color="green")
ax3.tick_params(axis='y', labelcolor="green")

# Title and Legend
ax1.set_xlabel("Date")
ax1.set_title("BSE Sensex vs NSE Indices & Stock")
fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9))

# Display the plot in Streamlit
st.pyplot(fig)
