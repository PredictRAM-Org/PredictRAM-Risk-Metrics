import streamlit as st
import pandas as pd
import numpy as np

# Load data
def load_data(file_path):
    return pd.read_excel(file_path)

# Calculate risk metrics
def calculate_risk_metrics(stock_info):
    # Initialize risk scores
    risk_scores = {}

    # Market Risk Metrics
    if stock_info['beta'] < 0.5:
        risk_scores['Beta'] = 1
    elif 0.5 <= stock_info['beta'] < 0.9:
        risk_scores['Beta'] = 2
    elif 1.0 <= stock_info['beta'] < 1.5:
        risk_scores['Beta'] = 3
    else:
        risk_scores['Beta'] = 4

    if stock_info['52WeekChange'] > 0.2:
        risk_scores['52-Week Change'] = 1
    elif 0.0 <= stock_info['52WeekChange'] <= 0.2:
        risk_scores['52-Week Change'] = 2
    elif -0.1 <= stock_info['52WeekChange'] < 0.0:
        risk_scores['52-Week Change'] = 3
    else:
        risk_scores['52-Week Change'] = 4

    price_volatility = stock_info['dayHigh'] - stock_info['dayLow']
    average_volume = stock_info['volume'] / stock_info['avgVolume']
    if price_volatility < 1 * average_volume:
        risk_scores['Price Volatility'] = 1
    elif 1 <= price_volatility < 2 * average_volume:
        risk_scores['Price Volatility'] = 2
    else:
        risk_scores['Price Volatility'] = 3

    # Liquidity Risk Metrics
    if stock_info['currentRatio'] > 3:
        risk_scores['Current Ratio'] = 1
    elif 2 <= stock_info['currentRatio'] <= 3:
        risk_scores['Current Ratio'] = 2
    elif 1 <= stock_info['currentRatio'] < 2:
        risk_scores['Current Ratio'] = 3
    else:
        risk_scores['Current Ratio'] = 4

    if stock_info['quickRatio'] > 1.5:
        risk_scores['Quick Ratio'] = 1
    elif 1 <= stock_info['quickRatio'] <= 1.5:
        risk_scores['Quick Ratio'] = 2
    elif 0.5 <= stock_info['quickRatio'] < 1:
        risk_scores['Quick Ratio'] = 3
    else:
        risk_scores['Quick Ratio'] = 4

    if stock_info['volume'] > 3 * stock_info['avgVolume']:
        risk_scores['Volume vs. Average Volume'] = 1
    elif 2 <= stock_info['volume'] <= 3 * stock_info['avgVolume']:
        risk_scores['Volume vs. Average Volume'] = 2
    elif 1 <= stock_info['volume'] < 2 * stock_info['avgVolume']:
        risk_scores['Volume vs. Average Volume'] = 3
    else:
        risk_scores['Volume vs. Average Volume'] = 4

    # Leverage Risk Metrics
    if stock_info['debtToEquity'] < 0.3:
        risk_scores['Debt-to-Equity Ratio'] = 1
    elif 0.3 <= stock_info['debtToEquity'] < 0.6:
        risk_scores['Debt-to-Equity Ratio'] = 2
    elif 0.6 <= stock_info['debtToEquity'] < 1.0:
        risk_scores['Debt-to-Equity Ratio'] = 3
    else:
        risk_scores['Debt-to-Equity Ratio'] = 4

    if stock_info['totalDebt'] / stock_info['equity'] <= 0.2:
        risk_scores['Total Debt'] = 1
    elif 0.2 < stock_info['totalDebt'] / stock_info['equity'] <= 0.5:
        risk_scores['Total Debt'] = 2
    elif 0.5 < stock_info['totalDebt'] / stock_info['equity'] <= 0.7:
        risk_scores['Total Debt'] = 3
    else:
        risk_scores['Total Debt'] = 4

    # Profitability Risk Metrics
    if stock_info['profitMargins'] > 0.20:
        risk_scores['Profit Margins'] = 1
    elif 0.10 <= stock_info['profitMargins'] <= 0.20:
        risk_scores['Profit Margins'] = 2
    elif 0.05 <= stock_info['profitMargins'] < 0.10:
        risk_scores['Profit Margins'] = 3
    else:
        risk_scores['Profit Margins'] = 4

    if stock_info['grossMargins'] > 0.50:
        risk_scores['Gross Margins'] = 1
    elif 0.30 <= stock_info['grossMargins'] <= 0.50:
        risk_scores['Gross Margins'] = 2
    elif 0.20 <= stock_info['grossMargins'] < 0.30:
        risk_scores['Gross Margins'] = 3
    else:
        risk_scores['Gross Margins'] = 4

    if stock_info['ebitdaMargins'] > 0.30:
        risk_scores['EBITDA Margins'] = 1
    elif 0.20 <= stock_info['ebitdaMargins'] <= 0.30:
        risk_scores['EBITDA Margins'] = 2
    elif 0.10 <= stock_info['ebitdaMargins'] < 0.20:
        risk_scores['EBITDA Margins'] = 3
    else:
        risk_scores['EBITDA Margins'] = 4

    if stock_info['returnOnAssets'] > 0.10:
        risk_scores['Return on Assets (ROA)'] = 1
    elif 0.05 <= stock_info['returnOnAssets'] <= 0.10:
        risk_scores['Return on Assets (ROA)'] = 2
    elif 0.02 <= stock_info['returnOnAssets'] < 0.05:
        risk_scores['Return on Assets (ROA)'] = 3
    else:
        risk_scores['Return on Assets (ROA)'] = 4

    if stock_info['returnOnEquity'] > 0.15:
        risk_scores['Return on Equity (ROE)'] = 1
    elif 0.10 <= stock_info['returnOnEquity'] <= 0.15:
        risk_scores['Return on Equity (ROE)'] = 2
    elif 0.05 <= stock_info['returnOnEquity'] < 0.10:
        risk_scores['Return on Equity (ROE)'] = 3
    else:
        risk_scores['Return on Equity (ROE)'] = 4

    # Valuation Risk Metrics
    if stock_info['trailingPE'] < 10:
        risk_scores['Price-to-Earnings Ratio (P/E)'] = 1
    elif 10 <= stock_info['trailingPE'] < 20:
        risk_scores['Price-to-Earnings Ratio (P/E)'] = 2
    elif 20 <= stock_info['trailingPE'] < 30:
        risk_scores['Price-to-Earnings Ratio (P/E)'] = 3
    else:
        risk_scores['Price-to-Earnings Ratio (P/E)'] = 4

    if stock_info['priceToBook'] < 1:
        risk_scores['Price-to-Book Ratio'] = 1
    elif 1 <= stock_info['priceToBook'] < 2:
        risk_scores['Price-to-Book Ratio'] = 2
    elif 2 <= stock_info['priceToBook'] < 4:
        risk_scores['Price-to-Book Ratio'] = 3
    else:
        risk_scores['Price-to-Book Ratio'] = 4

    if stock_info['priceToSalesTrailing12Months'] < 1:
        risk_scores['Price-to-Sales Ratio'] = 1
    elif 1 <= stock_info['priceToSalesTrailing12Months'] < 2:
        risk_scores['Price-to-Sales Ratio'] = 2
    elif 2 <= stock_info['priceToSalesTrailing12Months'] < 4:
        risk_scores['Price-to-Sales Ratio'] = 3
    else:
        risk_scores['Price-to-Sales Ratio'] = 4

    # Total Risk Score
    total_score = sum(risk_scores.values())

    return risk_scores, total_score

# Function to create risk meter bars
def display_risk_meter(title, score, max_score=4):
    st.subheader(title)
    bar_color = '#FF0000' if score == max_score else '#FFFF00' if score > max_score / 2 else '#00FF00'
    st.write(f"Score: {score}/{max_score}")
    st.progress(score / max_score, bar_color=bar_color)

# Load data
stock_data = load_data('all_stocks_data.xlsx')

st.title('Stock Risk Assessment')

# Allow the user to search and select a stock symbol
stock_symbol = st.selectbox('Select Stock Symbol', stock_data['Symbol'].unique())

# Filter stock data based on the selected symbol
stock_info = stock_data[stock_data['Symbol'] == stock_symbol].iloc[0]

# Calculate risk metrics
risk_scores, total_score = calculate_risk_metrics(stock_info)

# Display risk metrics
for metric, score in risk_scores.items():
    display_risk_meter(metric, score)

# Display total risk score
st.subheader('Total Risk Score')
st.write(f"Total Score: {total_score}/{len(risk_scores) * 4}")

# Display stock information
st.subheader('Stock Information')
st.write(stock_info)

