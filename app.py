import streamlit as st
import pandas as pd

# Load data from the Excel file
@st.cache_data
def load_data():
    df = pd.read_excel("all_stocks_data.xlsx", engine='openpyxl')
    return df

data = load_data()

# Title of the app
st.title("Stock Risk Metrics Dashboard")

# Select stock
stock_options = data['symbol'].unique()
selected_stock = st.selectbox('Select a stock:', stock_options)

# Filter data for the selected stock
stock_data = data[data['symbol'] == selected_stock]

# Functions to calculate risk metrics
def market_risk(stock_data):
    beta = stock_data['beta'].values[0]
    fifty_two_week_range = (stock_data['fiftyTwoWeekHigh'].values[0] - stock_data['fiftyTwoWeekLow'].values[0]) / stock_data['fiftyTwoWeekLow'].values[0]
    return beta, fifty_two_week_range

def liquidity_risk(stock_data):
    current_volume = stock_data['regularMarketVolume'].values[0]
    avg_volume = stock_data['averageVolume'].values[0]
    bid_ask_spread = stock_data['ask'].values[0] - stock_data['bid'].values[0]
    return current_volume, avg_volume, bid_ask_spread

def leverage_risk(stock_data):
    debt_to_equity = stock_data['debtToEquity'].values[0]
    total_debt = stock_data['totalDebt'].values[0]
    return debt_to_equity, total_debt

def profitability_risk(stock_data):
    profit_margin = stock_data['profitMargins'].values[0]
    roa = stock_data['returnOnAssets'].values[0]
    return profit_margin, roa

def valuation_risk(stock_data):
    pe_ratio = stock_data['trailingPE'].values[0]
    price_to_sales = stock_data['priceToSalesTrailing12Months'].values[0]
    return pe_ratio, price_to_sales

def dividend_risk(stock_data):
    payout_ratio = stock_data['payoutRatio'].values[0]
    dividend_yield = stock_data['trailingAnnualDividendYield'].values[0]
    return payout_ratio, dividend_yield

def operational_risk(stock_data):
    operating_margin = stock_data['operatingMargins'].values[0]
    roe = stock_data['returnOnEquity'].values[0]
    return operating_margin, roe

def financial_health_risk(stock_data):
    quick_ratio = stock_data['quickRatio'].values[0]
    current_ratio = stock_data['currentRatio'].values[0]
    return quick_ratio, current_ratio

def sector_industry_risk(stock_data):
    sector_pe = stock_data['industry_forwardPE'].values[0]
    industry_debt_to_equity = stock_data['industry_debtToEquity'].values[0]
    return sector_pe, industry_debt_to_equity

def valuation_vs_industry_risk(stock_data):
    pe_vs_industry = stock_data['trailingPE'].values[0] / stock_data['industry_trailingPE'].values[0]
    return pe_vs_industry

# Display risk metrics in the dashboard view
st.subheader("Market Risk")
beta, fifty_two_week_range = market_risk(stock_data)
st.write(f"Beta: {beta}")
st.write(f"52-Week Range: {fifty_two_week_range:.2%}")

st.subheader("Liquidity Risk")
current_volume, avg_volume, bid_ask_spread = liquidity_risk(stock_data)
st.write(f"Current Volume: {current_volume}")
st.write(f"Average Volume: {avg_volume}")
st.write(f"Bid-Ask Spread: {bid_ask_spread}")

st.subheader("Leverage Risk")
debt_to_equity, total_debt = leverage_risk(stock_data)
st.write(f"Debt to Equity Ratio: {debt_to_equity}")
st.write(f"Total Debt: {total_debt}")

st.subheader("Profitability Risk")
profit_margin, roa = profitability_risk(stock_data)
st.write(f"Profit Margin: {profit_margin:.2%}")
st.write(f"Return on Assets (ROA): {roa:.2%}")

st.subheader("Valuation Risk")
pe_ratio, price_to_sales = valuation_risk(stock_data)
st.write(f"P/E Ratio: {pe_ratio}")
st.write(f"Price to Sales Ratio: {price_to_sales}")

st.subheader("Dividend Risk")
payout_ratio, dividend_yield = dividend_risk(stock_data)
st.write(f"Payout Ratio: {payout_ratio:.2%}")
st.write(f"Dividend Yield: {dividend_yield:.2%}")

st.subheader("Operational Risk")
operating_margin, roe = operational_risk(stock_data)
st.write(f"Operating Margin: {operating_margin:.2%}")
st.write(f"Return on Equity (ROE): {roe:.2%}")

st.subheader("Financial Health Metrics")
quick_ratio, current_ratio = financial_health_risk(stock_data)
st.write(f"Quick Ratio: {quick_ratio}")
st.write(f"Current Ratio: {current_ratio}")

st.subheader("Sector and Industry Risk Metrics")
sector_pe, industry_debt_to_equity = sector_industry_risk(stock_data)
st.write(f"Sector P/E: {sector_pe}")
st.write(f"Industry Debt to Equity Ratio: {industry_debt_to_equity}")

st.subheader("Valuation vs. Industry Metrics")
pe_vs_industry = valuation_vs_industry_risk(stock_data)
st.write(f"P/E vs Industry: {pe_vs_industry:.2f}")
