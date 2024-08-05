import streamlit as st
import pandas as pd

# Load data from Excel file
@st.cache_data
def load_data(file_path):
    return pd.read_excel(file_path)

# Calculate risk metrics
def calculate_risk_metrics(stock_data):
    risk_scores = {}

    # Ensure all required columns are present in the data
    required_columns = [
        'beta', '52WeekChange', 'dayHigh', 'dayLow', 'averageVolume', 
        'currentRatio', 'quickRatio', 'volume', 'debtToEquity', 
        'totalDebt', 'sharesOutstanding', 'bookValue', 'profitMargins', 
        'grossMargins', 'ebitdaMargins', 'returnOnAssets', 'returnOnEquity', 
        'trailingPE', 'priceToBook', 'priceToSalesTrailing12Months'
    ]
    for col in required_columns:
        if col not in stock_data:
            raise KeyError(f"Column '{col}' is missing in the data")

    # Market Risk Metrics
    beta = stock_data['beta']
    if beta < 0.5:
        risk_scores['Beta'] = 1
    elif 0.5 <= beta < 0.9:
        risk_scores['Beta'] = 2
    elif 0.9 <= beta < 1.5:
        risk_scores['Beta'] = 3
    else:
        risk_scores['Beta'] = 4

    change_52_week = stock_data['52WeekChange']
    if change_52_week > 0.2:
        risk_scores['52-Week Change'] = 1
    elif 0 <= change_52_week <= 0.2:
        risk_scores['52-Week Change'] = 2
    elif -0.1 <= change_52_week < 0:
        risk_scores['52-Week Change'] = 3
    else:
        risk_scores['52-Week Change'] = 4

    price_volatility = stock_data['dayHigh'] - stock_data['dayLow']
    avg_volume = stock_data['averageVolume']
    if price_volatility < avg_volume:
        risk_scores['Price Volatility'] = 1
    elif avg_volume <= price_volatility < 2 * avg_volume:
        risk_scores['Price Volatility'] = 2
    else:
        risk_scores['Price Volatility'] = 3

    # Liquidity Risk Metrics
    current_ratio = stock_data['currentRatio']
    if current_ratio > 3:
        risk_scores['Current Ratio'] = 1
    elif 2 <= current_ratio <= 3:
        risk_scores['Current Ratio'] = 2
    elif 1 <= current_ratio < 2:
        risk_scores['Current Ratio'] = 3
    else:
        risk_scores['Current Ratio'] = 4

    quick_ratio = stock_data['quickRatio']
    if quick_ratio > 1.5:
        risk_scores['Quick Ratio'] = 1
    elif 1 <= quick_ratio <= 1.5:
        risk_scores['Quick Ratio'] = 2
    elif 0.5 <= quick_ratio < 1:
        risk_scores['Quick Ratio'] = 3
    else:
        risk_scores['Quick Ratio'] = 4

    volume = stock_data['volume']
    if volume > 3 * avg_volume:
        risk_scores['Volume vs. Average Volume'] = 1
    elif 2 * avg_volume <= volume < 3 * avg_volume:
        risk_scores['Volume vs. Average Volume'] = 2
    elif avg_volume <= volume < 2 * avg_volume:
        risk_scores['Volume vs. Average Volume'] = 3
    else:
        risk_scores['Volume vs. Average Volume'] = 4

    # Leverage Risk Metrics
    debt_to_equity = stock_data['debtToEquity']
    if debt_to_equity < 0.3:
        risk_scores['Debt-to-Equity Ratio'] = 1
    elif 0.3 <= debt_to_equity < 0.6:
        risk_scores['Debt-to-Equity Ratio'] = 2
    elif 0.6 <= debt_to_equity < 1.0:
        risk_scores['Debt-to-Equity Ratio'] = 3
    else:
        risk_scores['Debt-to-Equity Ratio'] = 4

    total_debt = stock_data['totalDebt']
    total_equity = stock_data['sharesOutstanding'] * stock_data['bookValue']
    debt_ratio = total_debt / total_equity
    if debt_ratio <= 0.2:
        risk_scores['Total Debt'] = 1
    elif 0.2 < debt_ratio <= 0.5:
        risk_scores['Total Debt'] = 2
    elif 0.5 < debt_ratio <= 0.7:
        risk_scores['Total Debt'] = 3
    else:
        risk_scores['Total Debt'] = 4

    # Profitability Risk Metrics
    profit_margins = stock_data['profitMargins']
    if profit_margins > 0.2:
        risk_scores['Profit Margins'] = 1
    elif 0.1 <= profit_margins <= 0.2:
        risk_scores['Profit Margins'] = 2
    elif 0.05 <= profit_margins < 0.1:
        risk_scores['Profit Margins'] = 3
    else:
        risk_scores['Profit Margins'] = 4

    gross_margins = stock_data['grossMargins']
    if gross_margins > 0.5:
        risk_scores['Gross Margins'] = 1
    elif 0.3 <= gross_margins <= 0.5:
        risk_scores['Gross Margins'] = 2
    elif 0.2 <= gross_margins < 0.3:
        risk_scores['Gross Margins'] = 3
    else:
        risk_scores['Gross Margins'] = 4

    ebitda_margins = stock_data['ebitdaMargins']
    if ebitda_margins > 0.3:
        risk_scores['EBITDA Margins'] = 1
    elif 0.2 <= ebitda_margins <= 0.3:
        risk_scores['EBITDA Margins'] = 2
    elif 0.1 <= ebitda_margins < 0.2:
        risk_scores['EBITDA Margins'] = 3
    else:
        risk_scores['EBITDA Margins'] = 4

    roa = stock_data['returnOnAssets']
    if roa > 0.1:
        risk_scores['Return on Assets (ROA)'] = 1
    elif 0.05 <= roa <= 0.1:
        risk_scores['Return on Assets (ROA)'] = 2
    elif 0.02 <= roa < 0.05:
        risk_scores['Return on Assets (ROA)'] = 3
    else:
        risk_scores['Return on Assets (ROA)'] = 4

    roe = stock_data['returnOnEquity']
    if roe > 0.15:
        risk_scores['Return on Equity (ROE)'] = 1
    elif 0.1 <= roe <= 0.15:
        risk_scores['Return on Equity (ROE)'] = 2
    elif 0.05 <= roe < 0.1:
        risk_scores['Return on Equity (ROE)'] = 3
    else:
        risk_scores['Return on Equity (ROE)'] = 4

    # Valuation Risk Metrics
    pe_ratio = stock_data['trailingPE']
    if pe_ratio < 10:
        risk_scores['Price-to-Earnings Ratio (P/E)'] = 1
    elif 10 <= pe_ratio < 20:
        risk_scores['Price-to-Earnings Ratio (P/E)'] = 2
    elif 20 <= pe_ratio < 30:
        risk_scores['Price-to-Earnings Ratio (P/E)'] = 3
    else:
        risk_scores['Price-to-Earnings Ratio (P/E)'] = 4

    pb_ratio = stock_data['priceToBook']
    if pb_ratio < 1:
        risk_scores['Price-to-Book Ratio'] = 1
    elif 1 <= pb_ratio < 2:
        risk_scores['Price-to-Book Ratio'] = 2
    elif 2 <= pb_ratio < 4:
        risk_scores['Price-to-Book Ratio'] = 3
    else:
        risk_scores['Price-to-Book Ratio'] = 4

    ps_ratio = stock_data['priceToSalesTrailing12Months']
    if ps_ratio < 1:
        risk_scores['Price-to-Sales Ratio'] = 1
    elif 1 <= ps_ratio < 2:
        risk_scores['Price-to-Sales Ratio'] = 2
    elif 2 <= ps_ratio < 4:
        risk_scores['Price-to-Sales Ratio'] = 3
    else:
        risk_scores['Price-to-Sales Ratio'] = 4

    total_score = sum(risk_scores.values())
    return risk_scores, total_score

# Load stock data
stock_data = load_data('all_stocks_data.xlsx')

st.title('Stock Risk Assessment')

# Allow the user to select a stock symbol
stock_symbol = st.selectbox('Select a stock symbol', stock_data['symbol'].unique(), index=0)

# Filter data for the selected stock
stock_info = stock_data[stock_data['symbol'] == stock_symbol].squeeze()

# Calculate risk metrics
risk_scores, total_score = calculate_risk_metrics(stock_info)

# Display risk metrics
st.header(f"Risk Meter for {stock_symbol}")
st.subheader("Market Risk Metrics")
st.write(f"**Beta**: {stock_info['beta']} (score: {risk_scores['Beta']})")
st.write(f"**52-Week Change**: {stock_info['52WeekChange']} (score: {risk_scores['52-Week Change']})")
st.write(f"**Price Volatility**: {stock_info['dayHigh'] - stock_info['dayLow']} (score: {risk_scores['Price Volatility']})")

st.subheader("Liquidity Risk Metrics")
st.write(f"**Current Ratio**: {stock_info['currentRatio']} (score: {risk_scores['Current Ratio']})")
st.write(f"**Quick Ratio**: {stock_info['quickRatio']} (score: {risk_scores['Quick Ratio']})")
st.write(f"**Volume vs. Average Volume**: {stock_info['volume']} (score: {risk_scores['Volume vs. Average Volume']})")

st.subheader("Leverage Risk Metrics")
st.write(f"**Debt-to-Equity Ratio**: {stock_info['debtToEquity']} (score: {risk_scores['Debt-to-Equity Ratio']})")
st.write(f"**Total Debt**: {stock_info['totalDebt']} (score: {risk_scores['Total Debt']})")

st.subheader("Profitability Risk Metrics")
st.write(f"**Profit Margins**: {stock_info['profitMargins']} (score: {risk_scores['Profit Margins']})")
st.write(f"**Gross Margins**: {stock_info['grossMargins']} (score: {risk_scores['Gross Margins']})")
st.write(f"**EBITDA Margins**: {stock_info['ebitdaMargins']} (score: {risk_scores['EBITDA Margins']})")
st.write(f"**Return on Assets (ROA)**: {stock_info['returnOnAssets']} (score: {risk_scores['Return on Assets (ROA)']})")
st.write(f"**Return on Equity (ROE)**: {stock_info['returnOnEquity']} (score: {risk_scores['Return on Equity (ROE)']})")

st.subheader("Valuation Risk Metrics")
st.write(f"**Price-to-Earnings Ratio (P/E)**: {stock_info['trailingPE']} (score: {risk_scores['Price-to-Earnings Ratio (P/E)']})")
st.write(f"**Price-to-Book Ratio**: {stock_info['priceToBook']} (score: {risk_scores['Price-to-Book Ratio']})")
st.write(f"**Price-to-Sales Ratio**: {stock_info['priceToSalesTrailing12Months']} (score: {risk_scores['Price-to-Sales Ratio']})")

st.header(f"Total Risk Score for {stock_symbol}: {total_score}")

st.markdown(
    """
    ### Risk Level:
    - **Score 14-28**: Low Risk
    - **Score 29-42**: Medium Risk
    - **Score 43-56**: High Risk
    - **Score 57-70**: Very High Risk
    """
)
