import pandas as pd
import streamlit as st

def calculate_risk_scores(result):
    # Ensure 'result' is a DataFrame
    if not isinstance(result, pd.DataFrame):
        raise ValueError("Result should be a pandas DataFrame.")

    # Check for required columns
    required_columns = [
        'beta', '52WeekChange', 'dayHigh', 'dayLow', 'averageVolume',
        'currentRatio', 'quickRatio', 'volume', 'debtToEquity', 'totalDebt',
        'totalStockholdersEquity', 'profitMargins', 'grossMargins', 'ebitdaMargins',
        'returnOnAssets', 'returnOnEquity', 'forwardPE', 'priceToBook', 
        'priceToSalesTrailing12Months', 'trailingPE', 'payoutRatio', 
        'trailingAnnualDividendYield', 'dividendHistory', 'operatingCashflow',
        'freeCashflow', 'revenueGrowth', 'bookValue', 'previousBookValue', 
        'enterpriseValue', 'marketCap', 'totalCash', 'totalLiabilities', 
        'industry_forwardPE', 'industry_trailingPE', 'industry_debtToEquity'
    ]

    missing_columns = [col for col in required_columns if col not in result.columns]
    if missing_columns:
        raise ValueError(f"Missing columns in the DataFrame: {', '.join(missing_columns)}")

    # Market Risk Metrics
    beta = result['beta'].values[0] if not result['beta'].isna().values[0] else 0
    beta_score = 1 if beta < 0.5 else 2 if beta < 0.9 else 3 if beta <= 1.5 else 4

    week_change = result['52WeekChange'].values[0] if not result['52WeekChange'].isna().values[0] else 0
    week_change_score = 1 if week_change > 0.20 else 2 if week_change > 0.00 else 3 if week_change > -0.10 else 4

    day_high = result['dayHigh'].values[0] if not result['dayHigh'].isna().values[0] else 0
    day_low = result['dayLow'].values[0] if not result['dayLow'].isna().values[0] else 0
    average_volume = result['averageVolume'].values[0] if not result['averageVolume'].isna().values[0] else 0
    price_volatility = day_high - day_low
    volatility_score = 1 if average_volume > 0 and price_volatility < average_volume else 2 if price_volatility <= 2 * average_volume else 3

    # Liquidity Risk Metrics
    current_ratio = result['currentRatio'].values[0] if not result['currentRatio'].isna().values[0] else 0
    current_ratio_score = 1 if current_ratio > 3 else 2 if current_ratio >= 2 else 3 if current_ratio >= 1 else 4

    quick_ratio = result['quickRatio'].values[0] if not result['quickRatio'].isna().values[0] else 0
    quick_ratio_score = 1 if quick_ratio > 1.5 else 2 if quick_ratio >= 1 else 3 if quick_ratio >= 0.5 else 4

    volume = result['volume'].values[0] if not result['volume'].isna().values[0] else 0
    volume_vs_avg_volume = volume / average_volume if average_volume > 0 else 0
    volume_score = 1 if volume_vs_avg_volume > 3 else 2 if volume_vs_avg_volume >= 2 else 3 if volume_vs_avg_volume >= 1 else 4

    # Leverage Risk Metrics
    debt_to_equity = result['debtToEquity'].values[0] if not result['debtToEquity'].isna().values[0] else 0
    debt_to_equity_score = 1 if debt_to_equity < 0.3 else 2 if debt_to_equity <= 0.6 else 3 if debt_to_equity <= 1.0 else 4

    total_debt = result['totalDebt'].values[0] if not result['totalDebt'].isna().values[0] else 0
    equity = result['totalStockholdersEquity'].values[0] if not result['totalStockholdersEquity'].isna().values[0] else 0
    total_debt_ratio = total_debt / equity if equity > 0 else 0
    total_debt_score = 1 if total_debt_ratio <= 0.20 else 2 if total_debt_ratio <= 0.50 else 3 if total_debt_ratio <= 0.70 else 4

    # Profitability Risk Metrics
    profit_margin = result['profitMargins'].values[0] if not result['profitMargins'].isna().values[0] else 0
    profit_margin_score = 1 if profit_margin > 0.20 else 2 if profit_margin >= 0.10 else 3 if profit_margin >= 0.05 else 4

    gross_margin = result['grossMargins'].values[0] if not result['grossMargins'].isna().values[0] else 0
    gross_margin_score = 1 if gross_margin > 0.50 else 2 if gross_margin >= 0.30 else 3 if gross_margin >= 0.20 else 4

    ebitda_margin = result['ebitdaMargins'].values[0] if not result['ebitdaMargins'].isna().values[0] else 0
    ebitda_margin_score = 1 if ebitda_margin > 0.30 else 2 if ebitda_margin >= 0.20 else 3 if ebitda_margin >= 0.10 else 4

    roa = result['returnOnAssets'].values[0] if not result['returnOnAssets'].isna().values[0] else 0
    roa_score = 1 if roa > 0.10 else 2 if roa >= 0.05 else 3 if roa >= 0.02 else 4

    roe = result['returnOnEquity'].values[0] if not result['returnOnEquity'].isna().values[0] else 0
    roe_score = 1 if roe > 0.15 else 2 if roe >= 0.10 else 3 if roe >= 0.05 else 4

    # Valuation Risk Metrics
    pe_ratio = result['forwardPE'].values[0] if not result['forwardPE'].isna().values[0] else 0
    pe_ratio_score = 1 if pe_ratio < 10 else 2 if pe_ratio <= 20 else 3 if pe_ratio <= 30 else 4

    price_to_book = result['priceToBook'].values[0] if not result['priceToBook'].isna().values[0] else 0
    price_to_book_score = 1 if price_to_book < 1 else 2 if price_to_book <= 2 else 3 if price_to_book <= 4 else 4

    price_to_sales = result['priceToSalesTrailing12Months'].values[0] if not result['priceToSalesTrailing12Months'].isna().values[0] else 0
    price_to_sales_score = 1 if price_to_sales < 1 else 2 if price_to_sales <= 2 else 3 if price_to_sales <= 4 else 4

    trailing_pe = result['trailingPE'].values[0] if not result['trailingPE'].isna().values[0] else 0
    trailing_pe_score = 1 if trailing_pe < 10 else 2 if trailing_pe <= 20 else 3 if trailing_pe <= 30 else 4

    # Dividend Risk Metrics
    dividend_payout_ratio = result['payoutRatio'].values[0] if not result['payoutRatio'].isna().values[0] else 0
    dividend_payout_ratio_score = 1 if dividend_payout_ratio < 0.30 else 2 if dividend_payout_ratio <= 0.50 else 3 if dividend_payout_ratio <= 0.70 else 4

    dividend_yield = result['trailingAnnualDividendYield'].values[0] if not result['trailingAnnualDividendYield'].isna().values[0] else 0
    dividend_yield_score = 1 if dividend_yield > 0.06 else 2 if dividend_yield >= 0.04 else 3 if dividend_yield >= 0.02 else 4

    dividend_history = result['dividendHistory'].values[0] if not result['dividendHistory'].isna().values[0] else 0
    dividend_history_score = 1 if dividend_history > 10 else 2 if dividend_history >= 5 else 3 if dividend_history >= 1 else 4

    # Operational Risk Metrics
    operating_cash_flow = result['operatingCashflow'].values[0] if not result['operatingCashflow'].isna().values[0] else 0
    free_cash_flow = result['freeCashflow'].values[0] if not result['freeCashflow'].isna().values[0] else 0
    revenue_growth = result['revenueGrowth'].values[0] if not result['revenueGrowth'].isna().values[0] else 0
    operating_cash_flow_score = 1 if operating_cash_flow > 10000000 else 2 if operating_cash_flow >= 5000000 else 3 if operating_cash_flow >= 1000000 else 4
    free_cash_flow_score = 1 if free_cash_flow > 10000000 else 2 if free_cash_flow >= 5000000 else 3 if free_cash_flow >= 1000000 else 4
    revenue_growth_score = 1 if revenue_growth > 0.20 else 2 if revenue_growth >= 0.10 else 3 if revenue_growth >= 0.05 else 4

    # Financial Health Metrics
    book_value = result['bookValue'].values[0] if not result['bookValue'].isna().values[0] else 0
    previous_book_value = result['previousBookValue'].values[0] if not result['previousBookValue'].isna().values[0] else 0
    enterprise_value = result['enterpriseValue'].values[0] if not result['enterpriseValue'].isna().values[0] else 0
    cash_liquidity = result['totalCash'].values[0] if not result['totalCash'].isna().values[0] else 0

    book_value_score = 1 if book_value > 10000000 else 2 if book_value >= 5000000 else 3 if book_value >= 1000000 else 4
    enterprise_value_score = 1 if enterprise_value < marketCap else 2 if enterprise_value <= 2 * marketCap else 3 if enterprise_value <= 3 * marketCap else 4
    cash_liquidity_score = 1 if cash_liquidity > 10000000 else 2 if cash_liquidity >= 5000000 else 3 if cash_liquidity >= 1000000 else 4

    # Sector/Industry Risk Metrics
    industry_forward_pe = result['industry_forwardPE'].values[0] if not result['industry_forwardPE'].isna().values[0] else 0
    industry_trailing_pe = result['industry_trailingPE'].values[0] if not result['industry_trailingPE'].isna().values[0] else 0
    industry_debt_to_equity = result['industry_debtToEquity'].values[0] if not result['industry_debtToEquity'].isna().values[0] else 0

    sector_industry_scores = {
        'Industry Forward PE': 1 if industry_forward_pe < 15 else 2 if industry_forward_pe <= 25 else 3 if industry_forward_pe <= 35 else 4,
        'Industry Trailing PE': 1 if industry_trailing_pe < 15 else 2 if industry_trailing_pe <= 25 else 3 if industry_trailing_pe <= 35 else 4,
        'Industry Debt-to-Equity': 1 if industry_debt_to_equity < 0.3 else 2 if industry_debt_to_equity <= 0.6 else 3 if industry_debt_to_equity <= 1.0 else 4
    }

    return {
        'Market Risk': beta_score + week_change_score + volatility_score,
        'Liquidity Risk': current_ratio_score + quick_ratio_score + volume_score,
        'Leverage Risk': debt_to_equity_score + total_debt_score,
        'Profitability Risk': profit_margin_score + gross_margin_score + ebitda_margin_score + roa_score + roe_score,
        'Valuation Risk': pe_ratio_score + price_to_book_score + price_to_sales_score + trailing_pe_score,
        'Dividend Risk': dividend_payout_ratio_score + dividend_yield_score + dividend_history_score,
        'Operational Risk': operating_cash_flow_score + free_cash_flow_score + revenue_growth_score,
        'Financial Health': book_value_score + enterprise_value_score + cash_liquidity_score,
        'Sector/Industry Risk': sum(sector_industry_scores.values())
    }

# Main Streamlit app
st.title('Company Risk Assessment')

def load_data():
    # Load your data here
    return pd.read_csv('your_data_file.csv')

data = load_data()
st.write("### Available Companies")
company_list = data['symbol'].unique()
selected_company = st.selectbox("Select a company", company_list)

if selected_company:
    st.write(f"### Data for {selected_company}")
    result = data[data['symbol'] == selected_company]
    if result.empty:
        st.write("No data available for the selected company.")
    else:
        st.write(result)

        try:
            risk_scores = calculate_risk_scores(result)
            st.write("### Risk Scores")
            st.write(risk_scores)

            # Displaying risk profile meter
            st.write("### Risk Profile Meter")
            total_risk_score = sum(risk_scores.values())
            st.progress(total_risk_score / 100)  # Assuming a max risk score of 100
        except Exception as e:
            st.error(f"An error occurred while calculating risk scores: {e}")
