import streamlit as st
import pandas as pd

# Load data
df = pd.read_excel('all_stocks_data.xlsx')

# Function to calculate risk score
def calculate_risk_score(row):
    # Market Risk
    market_risk = 0
    if row['Beta'] > 1.5:
        market_risk += 5
    elif 1 < row['Beta'] <= 1.5:
        market_risk += 3
    else:
        market_risk += 1
    
    if row['Volatility (%)'] > 30:
        market_risk += 5
    elif 15 < row['Volatility (%)'] <= 30:
        market_risk += 3
    else:
        market_risk += 1

    # Liquidity Risk
    liquidity_risk = 0
    if row['Volume'] < 100000:
        liquidity_risk += 5
    elif 100000 <= row['Volume'] < 1000000:
        liquidity_risk += 3
    else:
        liquidity_risk += 1
    
    if row['Volume'] < row['Average Volume'] or row['Volume'] < row['Average Volume 10 days']:
        liquidity_risk += 5
    else:
        liquidity_risk += 1

    # Leverage Risk
    leverage_risk = 0
    if row['Debt to Equity'] > 2:
        leverage_risk += 5
    elif 1 < row['Debt to Equity'] <= 2:
        leverage_risk += 3
    else:
        leverage_risk += 1
    
    if row['Interest Coverage'] < 1.5:
        leverage_risk += 5
    elif 1.5 <= row['Interest Coverage'] < 3:
        leverage_risk += 3
    else:
        leverage_risk += 1

    # Profitability Risk
    profitability_risk = 0
    if row['Profit Margins'] < 5:
        profitability_risk += 5
    elif 5 <= row['Profit Margins'] < 10:
        profitability_risk += 3
    else:
        profitability_risk += 1
    
    if row['ROE'] < 10:
        profitability_risk += 5
    elif 10 <= row['ROE'] < 20:
        profitability_risk += 3
    else:
        profitability_risk += 1

    # Valuation Risk
    valuation_risk = 0
    if row['P/E Ratio'] > 25:
        valuation_risk += 5
    elif 15 < row['P/E Ratio'] <= 25:
        valuation_risk += 3
    else:
        valuation_risk += 1
    
    if row['P/B Ratio'] > 3:
        valuation_risk += 5
    elif 1 < row['P/B Ratio'] <= 3:
        valuation_risk += 3
    else:
        valuation_risk += 1

    # Dividend Risk
    dividend_risk = 0
    if row['Dividend Yield'] < 2:
        dividend_risk += 5
    elif 2 <= row['Dividend Yield'] < 4:
        dividend_risk += 3
    else:
        dividend_risk += 1
    
    if row['Payout Ratio'] > 70:
        dividend_risk += 5
    elif 50 < row['Payout Ratio'] <= 70:
        dividend_risk += 3
    else:
        dividend_risk += 1

    # Operational Risk
    operational_risk = 0
    if row['Revenue Growth'] < 5:
        operational_risk += 5
    elif 5 <= row['Revenue Growth'] < 10:
        operational_risk += 3
    else:
        operational_risk += 1
    
    if row['EPS Growth'] < 5:
        operational_risk += 5
    elif 5 <= row['EPS Growth'] < 10:
        operational_risk += 3
    else:
        operational_risk += 1

    # Financial Health Metrics
    financial_health_risk = 0
    if row['Debt to Equity'] > 2:
        financial_health_risk += 5
    elif 1 < row['Debt to Equity'] <= 2:
        financial_health_risk += 3
    else:
        financial_health_risk += 1
    
    if row['Current Ratio'] < 1:
        financial_health_risk += 5
    elif 1 <= row['Current Ratio'] < 2:
        financial_health_risk += 3
    else:
        financial_health_risk += 1

    # Sector and Industry Risk Metrics
    sector_industry_risk = 0
    if row['Industry Growth'] < 5:
        sector_industry_risk += 5
    elif 5 <= row['Industry Growth'] < 10:
        sector_industry_risk += 3
    else:
        sector_industry_risk += 1
    
    if row['Industry PE'] > 25:
        sector_industry_risk += 5
    elif 15 < row['Industry PE'] <= 25:
        sector_industry_risk += 3
    else:
        sector_industry_risk += 1

    # Calculate total risk score
    total_risk = (market_risk + liquidity_risk + leverage_risk + profitability_risk + valuation_risk + 
                  dividend_risk + operational_risk + financial_health_risk + sector_industry_risk)
    
    return total_risk

# Calculate risk scores for each stock
df['Risk Score'] = df.apply(calculate_risk_score, axis=1)

# Streamlit App
st.title('Stock Risk Meter Dashboard')

# Stock Selection
selected_stock = st.selectbox('Select a Stock', df['Symbol'])

# Display Risk Meter
stock_data = df[df['Symbol'] == selected_stock].iloc[0]
risk_score = stock_data['Risk Score']

st.subheader(f'Risk Score for {selected_stock}: {risk_score}')
st.progress(risk_score / 45)  # Assuming maximum score is 45 (adjust accordingly based on weighting)

# Additional Visualizations
st.write('---')
st.write('### Risk Category Breakdown')
st.write(f'Market Risk: {market_risk}')
st.write(f'Liquidity Risk: {liquidity_risk}')
st.write(f'Leverage Risk: {leverage_risk}')
st.write(f'Profitability Risk: {profitability_risk}')
st.write(f'Valuation Risk: {valuation_risk}')
st.write(f'Dividend Risk: {dividend_risk}')
st.write(f'Operational Risk: {operational_risk}')
st.write(f'Financial Health Risk: {financial_health_risk}')
st.write(f'Sector & Industry Risk: {sector_industry_risk}')
