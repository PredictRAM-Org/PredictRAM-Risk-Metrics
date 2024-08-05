import streamlit as st
import pandas as pd
import ast

# Load data from the Excel file
@st.cache_data
def load_data():
    return pd.read_excel('all_stocks_data.xlsx')

def calculate_risk_score(value, criteria, risk_mapping):
    """
    Calculate risk score based on value and criteria provided.
    
    Args:
        value (float or int): The value to score.
        criteria (dict): Risk criteria mapping values to scores.
        risk_mapping (list): List of tuples with ranges and corresponding scores.
    
    Returns:
        int: Risk score.
    """
    for range_limit, score in risk_mapping:
        if value <= range_limit:
            return score
    return max(risk_mapping, key=lambda x: x[1])[1]

def compute_risk_scores(result):
    scores = {}

    # Market Risk Metrics
    beta = result['beta'].values[0]
    fifty_two_week_change = result['52WeekChange'].values[0]
    price_high = result['dayHigh'].values[0] if 'dayHigh' in result.columns else None
    price_low = result['dayLow'].values[0] if 'dayLow' in result.columns else None
    average_volume = result['averageVolume'].values[0]
    
    scores['Beta'] = calculate_risk_score(
        beta, 
        ['Beta < 0.5', 'Beta 0.5 - 0.9', 'Beta 1.0 - 1.5', 'Beta > 1.5'],
        [(0.5, 1), (0.9, 2), (1.5, 3), (float('inf'), 4)]
    )
    scores['52-Week Change'] = calculate_risk_score(
        fifty_two_week_change, 
        ['52-Week Change > 20%', '52-Week Change 0% - 20%', '52-Week Change -10% - 0%', '52-Week Change < -10%'],
        [(0.2, 1), (0.0, 2), (-0.1, 3), (float('-inf'), 4)]
    )
    if price_high is not None and price_low is not None:
        price_volatility = (price_high - price_low) / average_volume
        scores['Price Volatility'] = calculate_risk_score(
            price_volatility, 
            ['Low Volatility', 'Moderate Volatility', 'High Volatility'],
            [(1, 1), (2, 2), (float('inf'), 3)]
        )

    # Liquidity Risk Metrics
    current_ratio = result['currentRatio'].values[0]
    quick_ratio = result['quickRatio'].values[0]
    volume = result['volume'].values[0]
    
    scores['Current Ratio'] = calculate_risk_score(
        current_ratio, 
        ['Current Ratio > 3', 'Current Ratio 2 - 3', 'Current Ratio 1 - 2', 'Current Ratio < 1'],
        [(3, 1), (2, 2), (1, 3), (float('-inf'), 4)]
    )
    scores['Quick Ratio'] = calculate_risk_score(
        quick_ratio, 
        ['Quick Ratio > 1.5', 'Quick Ratio 1 - 1.5', 'Quick Ratio 0.5 - 1', 'Quick Ratio < 0.5'],
        [(1.5, 1), (1.0, 2), (0.5, 3), (float('-inf'), 4)]
    )
    if average_volume > 0:
        volume_vs_avg_volume = volume / average_volume
        scores['Volume vs. Average Volume'] = calculate_risk_score(
            volume_vs_avg_volume, 
            ['Volume > 3 * Average Volume', 'Volume 2 - 3 * Average Volume', 'Volume 1 - 2 * Average Volume', 'Volume < 1 * Average Volume'],
            [(3, 1), (2, 2), (1, 3), (float('-inf'), 4)]
        )

    # Leverage Risk Metrics
    debt_to_equity = result['debtToEquity'].values[0]
    total_debt = result['totalDebt'].values[0]
    equity = result['totalEquity'].values[0]
    
    scores['Debt-to-Equity Ratio'] = calculate_risk_score(
        debt_to_equity, 
        ['Debt-to-Equity < 0.3', 'Debt-to-Equity 0.3 - 0.6', 'Debt-to-Equity 0.6 - 1.0', 'Debt-to-Equity > 1.0'],
        [(0.3, 1), (0.6, 2), (1.0, 3), (float('inf'), 4)]
    )
    if equity > 0:
        total_debt_ratio = total_debt / equity
        scores['Total Debt'] = calculate_risk_score(
            total_debt_ratio, 
            ['Total Debt ≤ 20% of Equity', 'Total Debt 20% - 50% of Equity', 'Total Debt 50% - 70% of Equity', 'Total Debt > 70% of Equity'],
            [(0.2, 1), (0.5, 2), (0.7, 3), (float('inf'), 4)]
        )

    # Profitability Risk Metrics
    profit_margins = result['profitMargins'].values[0]
    gross_margins = result['grossMargins'].values[0]
    ebitda_margins = result['ebitdaMargins'].values[0]
    return_on_assets = result['returnOnAssets'].values[0]
    return_on_equity = result['returnOnEquity'].values[0]
    
    scores['Profit Margins'] = calculate_risk_score(
        profit_margins, 
        ['Profit Margin > 20%', 'Profit Margin 10% - 20%', 'Profit Margin 5% - 10%', 'Profit Margin < 5%'],
        [(0.2, 1), (0.1, 2), (0.05, 3), (float('-inf'), 4)]
    )
    scores['Gross Margins'] = calculate_risk_score(
        gross_margins, 
        ['Gross Margin > 50%', 'Gross Margin 30% - 50%', 'Gross Margin 20% - 30%', 'Gross Margin < 20%'],
        [(0.5, 1), (0.3, 2), (0.2, 3), (float('-inf'), 4)]
    )
    scores['EBITDA Margins'] = calculate_risk_score(
        ebitda_margins, 
        ['EBITDA Margin > 30%', 'EBITDA Margin 20% - 30%', 'EBITDA Margin 10% - 20%', 'EBITDA Margin < 10%'],
        [(0.3, 1), (0.2, 2), (0.1, 3), (float('-inf'), 4)]
    )
    scores['Return on Assets'] = calculate_risk_score(
        return_on_assets, 
        ['ROA > 10%', 'ROA 5% - 10%', 'ROA 2% - 5%', 'ROA < 2%'],
        [(0.1, 1), (0.05, 2), (0.02, 3), (float('-inf'), 4)]
    )
    scores['Return on Equity'] = calculate_risk_score(
        return_on_equity, 
        ['ROE > 15%', 'ROE 10% - 15%', 'ROE 5% - 10%', 'ROE < 5%'],
        [(0.15, 1), (0.1, 2), (0.05, 3), (float('-inf'), 4)]
    )

    # Valuation Risk Metrics
    pe_ratio = result['forwardPE'].values[0]
    pe_ratio_score = 1 if pe_ratio < 10 else 2 if pe_ratio <= 20 else 3 if pe_ratio <= 30 else 4

    price_to_book = result['priceToBook'].values[0]
    price_to_book_score = 1 if price_to_book < 1 else 2 if price_to_book <= 2 else 3 if price_to_book <= 4 else 4

    price_to_sales = result['priceToSalesTrailing12Months'].values[0]
    price_to_sales_score = 1 if price_to_sales < 1 else 2 if price_to_sales <= 2 else 3 if price_to_sales <= 4 else 4

    trailing_pe = result['trailingPE'].values[0]
    trailing_pe_score = 1 if trailing_pe < 10 else 2 if trailing_pe <= 20 else 3 if trailing_pe <= 30 else 4

    # Dividend Risk Metrics
    dividend_payout_ratio = result['payoutRatio'].values[0]
    dividend_payout_ratio_score = 1 if dividend_payout_ratio < 0.30 else 2 if dividend_payout_ratio <= 0.50 else 3 if dividend_payout_ratio <= 0.70 else 4

    dividend_yield = result['trailingAnnualDividendYield'].values[0]
    dividend_yield_score = 1 if dividend_yield > 0.06 else 2 if dividend_yield >= 0.04 else 3 if dividend_yield >= 0.02 else 4

    dividend_history = result['dividendHistory'].values[0]  # Assuming you have this information
    dividend_history_score = 1 if dividend_history == 'Stable or Increasing' else 2 if dividend_history == 'Mixed' else 3 if dividend_history == 'Irregular' else 4

    # Operational Risk Metrics
    operating_cash_flow = result['operatingCashflow'].values[0]
    operating_cash_flow_score = 1 if operating_cash_flow > 0 else 2 if operating_cash_flow >= -1000000 else 3 if operating_cash_flow >= -5000000 else 4

    free_cash_flow = result['freeCashflow'].values[0]
    free_cash_flow_score = 1 if free_cash_flow > 0 else 2 if free_cash_flow >= -1000000 else 3 if free_cash_flow >= -5000000 else 4

    revenue_growth = result['revenueGrowth'].values[0]
    revenue_growth_score = 1 if revenue_growth > 0.15 else 2 if revenue_growth >= 0.10 else 3 if revenue_growth >= 0.05 else 4

    # Financial Health Metrics
    book_value = result['bookValue'].values[0]
    previous_book_value = result['previousBookValue'].values[0]  # Assuming you have this information
    book_value_score = 1 if book_value > previous_book_value else 2 if book_value == previous_book_value else 3 if book_value < previous_book_value else 4

    enterprise_value = result['enterpriseValue'].values[0]
    market_cap = result['marketCap'].values[0]
    enterprise_value_score = 1 if enterprise_value <= market_cap * 1.1 else 2 if enterprise_value <= market_cap * 1.2 else 3 if enterprise_value > market_cap * 1.5 else 4

    total_cash = result['totalCash'].values[0]
    total_liabilities = result['totalLiabilities'].values[0]  # Assuming you have this information
    cash_liquidity_score = 1 if total_cash / total_liabilities > 0.30 else 2 if total_cash / total_liabilities > 0.15 else 3 if total_cash / total_liabilities > 0.05 else 4

    # Sector and Industry Risk Metrics
    industry_forward_pe = result['industry_forwardPE'].values[0]
    industry_trailing_pe = result['industry_trailingPE'].values[0]
    industry_debt_to_equity = result['industry_debtToEquity'].values[0]
    industry_average_metrics = {
        'forwardPE': industry_forward_pe,
        'trailingPE': industry_trailing_pe,
        'debtToEquity': industry_debt_to_equity
    }

    company_vs_industry = {
        'forwardPE': pe_ratio,
        'trailingPE': trailing_pe,
        'debtToEquity': debt_to_equity
    }

    sector_industry_scores = {}
    for metric, industry_value in industry_average_metrics.items():
        company_value = company_vs_industry.get(metric, None)
        if company_value is not None:
            if company_value < industry_value:
                sector_industry_scores[metric] = 1
            elif company_value == industry_value:
                sector_industry_scores[metric] = 2
            else:
                sector_industry_scores[metric] = 3

    # Aggregating Scores
    total_score = (beta_score + week_change_score + volatility_score +
                   current_ratio_score + quick_ratio_score + volume_score +
                   debt_to_equity_score + total_debt_score +
                   profit_margin_score + gross_margin_score + ebitda_margin_score +
                   roa_score + roe_score +
                   pe_ratio_score + price_to_book_score + price_to_sales_score + trailing_pe_score +
                   dividend_payout_ratio_score + dividend_yield_score + dividend_history_score +
                   operating_cash_flow_score + free_cash_flow_score + revenue_growth_score +
                   book_value_score + enterprise_value_score + cash_liquidity_score +
                   sum(sector_industry_scores.values()))

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

data = load_data()
st.write("### Available Companies")
company_list = data['symbol'].unique()
selected_company = st.selectbox("Select a company", company_list)

if selected_company:
    st.write(f"### Data for {selected_company}")
    result = data[data['symbol'] == selected_company]
    st.write(result)

    risk_scores = calculate_risk_scores(result)

    st.write("### Risk Scores")
    st.write(risk_scores)

    # Displaying risk profile meter
    st.write("### Risk Profile Meter")
    total_risk_score = sum(risk_scores.values())
    st.progress(total_risk_score / 100)  # Assuming a max risk score of 100
