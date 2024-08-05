import streamlit as st
import pandas as pd

# Load data from Excel
@st.cache_data
def load_data():
    file_path = 'all_stocks_data.xlsx'
    return pd.read_excel(file_path)

df = load_data()

# Function to calculate risk metrics
def calculate_risk_metrics(stock_data):
    risk_scores = {
        'Market Risk': 0,
        'Liquidity Risk': 0,
        'Leverage Risk': 0,
        'Profitability Risk': 0,
        'Valuation Risk': 0,
        'Dividend Risk': 0,
        'Operational Risk': 0,
        'Financial Health': 0,
        'Sector & Industry Risk': 0,
        'Valuation vs Industry Metrics': 0
    }

    # Market Risk Metrics
    beta = stock_data['beta']
    week_change = stock_data['52WeekChange']
    volatility = stock_data['dayHigh'] - stock_data['dayLow']
    avg_volume = stock_data['averageVolume']

    risk_scores['Market Risk'] += 1 if beta < 0.5 else (2 if beta < 0.9 else (3 if beta < 1.5 else 4))
    risk_scores['Market Risk'] += 1 if week_change > 20 else (2 if week_change > 0 else (3 if week_change > -10 else 4))
    risk_scores['Market Risk'] += 1 if volatility < avg_volume else (2 if volatility < 2 * avg_volume else 3)

    # Liquidity Risk Metrics
    current_ratio = stock_data['currentRatio']
    quick_ratio = stock_data['quickRatio']
    volume = stock_data['volume']

    risk_scores['Liquidity Risk'] += 1 if current_ratio > 3 else (2 if current_ratio > 2 else (3 if current_ratio > 1 else 4))
    risk_scores['Liquidity Risk'] += 1 if quick_ratio > 1.5 else (2 if quick_ratio > 1 else (3 if quick_ratio > 0.5 else 4))
    risk_scores['Liquidity Risk'] += 1 if volume > 3 * avg_volume else (2 if volume > 2 * avg_volume else (3 if volume > avg_volume else 4))

    # Leverage Risk Metrics
    debt_to_equity = stock_data['debtToEquity']
    total_debt = stock_data['totalDebt']
    book_value = stock_data['bookValue']

    risk_scores['Leverage Risk'] += 1 if debt_to_equity < 0.3 else (2 if debt_to_equity < 0.6 else (3 if debt_to_equity < 1.0 else 4))
    equity = stock_data['bookValue'] * stock_data['sharesOutstanding'] - stock_data['totalDebt']
    risk_scores['Leverage Risk'] += 1 if total_debt <= 0.2 * equity else (2 if total_debt <= 0.5 * equity else (3 if total_debt <= 0.7 * equity else 4))

    # Profitability Risk Metrics
    profit_margin = stock_data['profitMargins']
    gross_margin = stock_data['grossMargins']
    ebitda_margin = stock_data['ebitdaMargins']
    roa = stock_data['returnOnAssets']
    roe = stock_data['returnOnEquity']

    risk_scores['Profitability Risk'] += 1 if profit_margin > 20 else (2 if profit_margin > 10 else (3 if profit_margin > 5 else 4))
    risk_scores['Profitability Risk'] += 1 if gross_margin > 50 else (2 if gross_margin > 30 else (3 if gross_margin > 20 else 4))
    risk_scores['Profitability Risk'] += 1 if ebitda_margin > 30 else (2 if ebitda_margin > 20 else (3 if ebitda_margin > 10 else 4))
    risk_scores['Profitability Risk'] += 1 if roa > 10 else (2 if roa > 5 else (3 if roa > 2 else 4))
    risk_scores['Profitability Risk'] += 1 if roe > 15 else (2 if roe > 10 else (3 if roe > 5 else 4))

    # Valuation Risk Metrics
    pe_ratio = stock_data['forwardPE']
    price_to_book = stock_data['priceToBook']
    price_to_sales = stock_data['priceToSalesTrailing12Months']
    trailing_pe = stock_data['trailingPE']

    risk_scores['Valuation Risk'] += 1 if pe_ratio < 10 else (2 if pe_ratio < 20 else (3 if pe_ratio < 30 else 4))
    risk_scores['Valuation Risk'] += 1 if price_to_book < 1 else (2 if price_to_book < 2 else (3 if price_to_book < 4 else 4))
    risk_scores['Valuation Risk'] += 1 if price_to_sales < 1 else (2 if price_to_sales < 2 else (3 if price_to_sales < 4 else 4))
    risk_scores['Valuation Risk'] += 1 if trailing_pe < 10 else (2 if trailing_pe < 20 else (3 if trailing_pe < 30 else 4))

    # Dividend Risk Metrics
    payout_ratio = stock_data['payoutRatio']
    dividend_yield = stock_data['fiveYearAvgDividendYield']
    dividend_history = 'Stable'  # Assume stable for simplicity

    risk_scores['Dividend Risk'] += 1 if payout_ratio < 0.3 else (2 if payout_ratio < 0.5 else (3 if payout_ratio < 0.7 else 4))
    risk_scores['Dividend Risk'] += 1 if dividend_yield > 0.06 else (2 if dividend_yield > 0.04 else (3 if dividend_yield > 0.02 else 4))
    risk_scores['Dividend Risk'] += 1 if dividend_history == 'Stable' else (2 if dividend_history == 'Mixed' else (3 if dividend_history == 'Irregular' else 4))

    # Operational Risk Metrics
    operating_cashflow = stock_data['operatingCashflow']
    free_cashflow = stock_data['freeCashflow']
    revenue_growth = stock_data['revenueGrowth']

    risk_scores['Operational Risk'] += 1 if operating_cashflow > 0 and operating_cashflow > free_cashflow else (2 if operating_cashflow > 0 else (3 if operating_cashflow == 0 else 4))
    risk_scores['Operational Risk'] += 1 if free_cashflow > 0 and free_cashflow > operating_cashflow else (2 if free_cashflow > 0 else (3 if free_cashflow < 0 else 4))
    risk_scores['Operational Risk'] += 1 if revenue_growth > 0.15 else (2 if revenue_growth > 0.1 else (3 if revenue_growth > 0.05 else 4))

    # Financial Health Metrics
    book_value = stock_data['bookValue']
    enterprise_value = stock_data['enterpriseValue']
    total_cash = stock_data['totalCash']

    risk_scores['Financial Health'] += 1 if book_value > stock_data['bookValue'] else (2 if book_value == stock_data['bookValue'] else (3 if book_value < stock_data['bookValue'] else 4))
    risk_scores['Financial Health'] += 1 if enterprise_value >= stock_data['marketCap'] else (2 if enterprise_value < 1.1 * stock_data['marketCap'] else (3 if enterprise_value > 1.5 * stock_data['marketCap'] else 4))
    risk_scores['Financial Health'] += 1 if total_cash > 0.3 * stock_data['totalLiabilities'] else (2 if total_cash > 0.15 * stock_data['totalLiabilities'] else (3 if total_cash > 0.05 * stock_data['totalLiabilities'] else 4))

    # Sector & Industry Risk Metrics
    industry_avg_debt_to_equity = stock_data['industry_debtToEquity']
    sector_avg_debt_to_equity = stock_data['industry_debtToEquity']

    risk_scores['Sector & Industry Risk'] += 1 if debt_to_equity < industry_avg_debt_to_equity else (2 if debt_to_equity == industry_avg_debt_to_equity else (3 if debt_to_equity > industry_avg_debt_to_equity else 4))

    # Valuation vs Industry Metrics
    industry_forward_pe = stock_data['industry_forwardPE']
    industry_trailing_pe = stock_data['industry_trailingPE']
    industry_avg_debt_to_equity = stock_data['industry_debtToEquity']

    risk_scores['Valuation vs Industry Metrics'] += 1 if pe_ratio < industry_forward_pe else (2 if pe_ratio == industry_forward_pe else (3 if pe_ratio > industry_forward_pe else 4))
    risk_scores['Valuation vs Industry Metrics'] += 1 if pe_ratio < industry_trailing_pe else (2 if pe_ratio == industry_trailing_pe else (3 if pe_ratio > industry_trailing_pe else 4))
    risk_scores['Valuation vs Industry Metrics'] += 1 if debt_to_equity < industry_avg_debt_to_equity else (2 if debt_to_equity == industry_avg_debt_to_equity else (3 if debt_to_equity > industry_avg_debt_to_equity else 4))

    return risk_scores

# Streamlit app
st.title('Stock Risk Assessment')

# Select stock
stock_symbol = st.selectbox('Select Stock Symbol', df['symbol'].unique())
stock_data = df[df['symbol'] == stock_symbol].iloc[0]

# Calculate risk metrics
risk_scores = calculate_risk_metrics(stock_data)

# Display results
st.subheader(f'Risk Metrics for {stock_symbol}')

for metric, score in risk_scores.items():
    st.write(f'{metric}: {score}')

    # Risk meter bar
    bar_color = 'green' if score <= 3 else 'orange' if score <= 6 else 'red'
    st.progress((10 - score) * 10, text=f'{metric}: {score}', color=bar_color)
