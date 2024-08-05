import pandas as pd

def calculate_market_risk_scores(data):
    market_risk_scores = {}
    
    # Beta Scoring
    if data['Beta'] < 0.5:
        market_risk_scores['Beta'] = 1
    elif 0.5 <= data['Beta'] < 1.0:
        market_risk_scores['Beta'] = 2
    elif 1.0 <= data['Beta'] < 1.5:
        market_risk_scores['Beta'] = 3
    else:
        market_risk_scores['Beta'] = 4

    # 52-Week Change Scoring
    if data['52WeekChange'] > 0.2:
        market_risk_scores['52WeekChange'] = 1
    elif 0 <= data['52WeekChange'] <= 0.2:
        market_risk_scores['52WeekChange'] = 2
    elif -0.1 <= data['52WeekChange'] < 0:
        market_risk_scores['52WeekChange'] = 3
    else:
        market_risk_scores['52WeekChange'] = 4

    # Price Volatility Scoring
    price_range = data['DayHigh'] - data['DayLow']
    if price_range < data['AvgVolume']:
        market_risk_scores['PriceVolatility'] = 1
    elif data['AvgVolume'] <= price_range < 2 * data['AvgVolume']:
        market_risk_scores['PriceVolatility'] = 2
    else:
        market_risk_scores['PriceVolatility'] = 3

    return market_risk_scores

def calculate_liquidity_risk_scores(data):
    liquidity_risk_scores = {}
    
    # Current Ratio Scoring
    if data['CurrentRatio'] > 3:
        liquidity_risk_scores['CurrentRatio'] = 1
    elif 2 <= data['CurrentRatio'] <= 3:
        liquidity_risk_scores['CurrentRatio'] = 2
    elif 1 <= data['CurrentRatio'] < 2:
        liquidity_risk_scores['CurrentRatio'] = 3
    else:
        liquidity_risk_scores['CurrentRatio'] = 4

    # Quick Ratio Scoring
    if data['QuickRatio'] > 1.5:
        liquidity_risk_scores['QuickRatio'] = 1
    elif 1 <= data['QuickRatio'] <= 1.5:
        liquidity_risk_scores['QuickRatio'] = 2
    elif 0.5 <= data['QuickRatio'] < 1:
        liquidity_risk_scores['QuickRatio'] = 3
    else:
        liquidity_risk_scores['QuickRatio'] = 4

    # Volume vs. Average Volume Scoring
    if data['Volume'] > 3 * data['AvgVolume']:
        liquidity_risk_scores['VolumeVsAvgVolume'] = 1
    elif 2 * data['AvgVolume'] <= data['Volume'] <= 3 * data['AvgVolume']:
        liquidity_risk_scores['VolumeVsAvgVolume'] = 2
    elif data['AvgVolume'] <= data['Volume'] < 2 * data['AvgVolume']:
        liquidity_risk_scores['VolumeVsAvgVolume'] = 3
    else:
        liquidity_risk_scores['VolumeVsAvgVolume'] = 4

    return liquidity_risk_scores

def calculate_leverage_risk_scores(data):
    leverage_risk_scores = {}

    # Debt-to-Equity Ratio Scoring
    if data['DebtToEquity'] < 0.3:
        leverage_risk_scores['DebtToEquity'] = 1
    elif 0.3 <= data['DebtToEquity'] < 0.6:
        leverage_risk_scores['DebtToEquity'] = 2
    elif 0.6 <= data['DebtToEquity'] < 1.0:
        leverage_risk_scores['DebtToEquity'] = 3
    else:
        leverage_risk_scores['DebtToEquity'] = 4

    # Total Debt Scoring
    total_debt_to_equity = data['TotalDebt'] / data['Equity']
    if total_debt_to_equity <= 0.2:
        leverage_risk_scores['TotalDebt'] = 1
    elif 0.2 < total_debt_to_equity <= 0.5:
        leverage_risk_scores['TotalDebt'] = 2
    elif 0.5 < total_debt_to_equity <= 0.7:
        leverage_risk_scores['TotalDebt'] = 3
    else:
        leverage_risk_scores['TotalDebt'] = 4

    return leverage_risk_scores

def calculate_profitability_risk_scores(data):
    profitability_risk_scores = {}

    # Profit Margins Scoring
    if data['ProfitMargin'] > 0.2:
        profitability_risk_scores['ProfitMargin'] = 1
    elif 0.1 <= data['ProfitMargin'] <= 0.2:
        profitability_risk_scores['ProfitMargin'] = 2
    elif 0.05 <= data['ProfitMargin'] < 0.1:
        profitability_risk_scores['ProfitMargin'] = 3
    else:
        profitability_risk_scores['ProfitMargin'] = 4

    # Gross Margins Scoring
    if data['GrossMargin'] > 0.5:
        profitability_risk_scores['GrossMargin'] = 1
    elif 0.3 <= data['GrossMargin'] <= 0.5:
        profitability_risk_scores['GrossMargin'] = 2
    elif 0.2 <= data['GrossMargin'] < 0.3:
        profitability_risk_scores['GrossMargin'] = 3
    else:
        profitability_risk_scores['GrossMargin'] = 4

    # EBITDA Margins Scoring
    if data['EBITDAMargin'] > 0.3:
        profitability_risk_scores['EBITDAMargin'] = 1
    elif 0.2 <= data['EBITDAMargin'] <= 0.3:
        profitability_risk_scores['EBITDAMargin'] = 2
    elif 0.1 <= data['EBITDAMargin'] < 0.2:
        profitability_risk_scores['EBITDAMargin'] = 3
    else:
        profitability_risk_scores['EBITDAMargin'] = 4

    # Return on Assets (ROA) Scoring
    if data['ROA'] > 0.1:
        profitability_risk_scores['ROA'] = 1
    elif 0.05 <= data['ROA'] <= 0.1:
        profitability_risk_scores['ROA'] = 2
    elif 0.02 <= data['ROA'] < 0.05:
        profitability_risk_scores['ROA'] = 3
    else:
        profitability_risk_scores['ROA'] = 4

    # Return on Equity (ROE) Scoring
    if data['ROE'] > 0.15:
        profitability_risk_scores['ROE'] = 1
    elif 0.1 <= data['ROE'] <= 0.15:
        profitability_risk_scores['ROE'] = 2
    elif 0.05 <= data['ROE'] < 0.1:
        profitability_risk_scores['ROE'] = 3
    else:
        profitability_risk_scores['ROE'] = 4

    return profitability_risk_scores

def calculate_valuation_risk_scores(data):
    valuation_risk_scores = {}

    # Price-to-Earnings Ratio (P/E) Scoring
    if data['PE'] < 10:
        valuation_risk_scores['PE'] = 1
    elif 10 <= data['PE'] < 20:
        valuation_risk_scores['PE'] = 2
    elif 20 <= data['PE'] < 30:
        valuation_risk_scores['PE'] = 3
    else:
        valuation_risk_scores['PE'] = 4

    # Price-to-Book Ratio Scoring
    if data['PriceToBook'] < 1:
        valuation_risk_scores['PriceToBook'] = 1
    elif 1 <= data['PriceToBook'] < 2:
        valuation_risk_scores['PriceToBook'] = 2
    elif 2 <= data['PriceToBook'] < 4:
        valuation_risk_scores['PriceToBook'] = 3
    else:
        valuation_risk_scores['PriceToBook'] = 4

    # Price-to-Sales Ratio Scoring
    if data['PriceToSales'] < 1:
        valuation_risk_scores['PriceToSales'] = 1
    elif 1 <= data['PriceToSales'] < 2:
        valuation_risk_scores['PriceToSales'] = 2
    elif 2 <= data['PriceToSales'] < 4:
        valuation_risk_scores['PriceToSales'] = 3
    else:
        valuation_risk_scores['PriceToSales'] = 4

    # Trailing PE Scoring
    if data['TrailingPE'] < 10:
        valuation_risk_scores['TrailingPE'] = 1
    elif 10 <= data['TrailingPE'] < 20:
        valuation_risk_scores['TrailingPE'] = 2
    elif 20 <= data['TrailingPE'] < 30:
        valuation_risk_scores['TrailingPE'] = 3
    else:
        valuation_risk_scores['TrailingPE'] = 4

    return valuation_risk_scores

def calculate_dividend_risk_scores(data):
    dividend_risk_scores = {}

    # Dividend Yield Scoring
    if data['DividendYield'] > 0.05:
        dividend_risk_scores['DividendYield'] = 1
    elif 0.03 <= data['DividendYield'] <= 0.05:
        dividend_risk_scores['DividendYield'] = 2
    elif 0.01 <= data['DividendYield'] < 0.03:
        dividend_risk_scores['DividendYield'] = 3
    else:
        dividend_risk_scores['DividendYield'] = 4

    # Payout Ratio Scoring
    if data['PayoutRatio'] < 0.3:
        dividend_risk_scores['PayoutRatio'] = 1
    elif 0.3 <= data['PayoutRatio'] < 0.5:
        dividend_risk_scores['PayoutRatio'] = 2
    elif 0.5 <= data['PayoutRatio'] < 0.75:
        dividend_risk_scores['PayoutRatio'] = 3
    else:
        dividend_risk_scores['PayoutRatio'] = 4

    # Ex-Dividend Date Scoring
    if pd.to_datetime(data['ExDividendDate']) < pd.to_datetime('today'):
        dividend_risk_scores['ExDividendDate'] = 1
    else:
        dividend_risk_scores['ExDividendDate'] = 4

    return dividend_risk_scores

def calculate_operational_risk_scores(data):
    operational_risk_scores = {}

    # Net Income Growth Scoring
    if data['NetIncomeGrowth'] > 0.15:
        operational_risk_scores['NetIncomeGrowth'] = 1
    elif 0.05 <= data['NetIncomeGrowth'] <= 0.15:
        operational_risk_scores['NetIncomeGrowth'] = 2
    elif 0 <= data['NetIncomeGrowth'] < 0.05:
        operational_risk_scores['NetIncomeGrowth'] = 3
    else:
        operational_risk_scores['NetIncomeGrowth'] = 4

    # Revenue Growth Scoring
    if data['RevenueGrowth'] > 0.15:
        operational_risk_scores['RevenueGrowth'] = 1
    elif 0.05 <= data['RevenueGrowth'] <= 0.15:
        operational_risk_scores['RevenueGrowth'] = 2
    elif 0 <= data['RevenueGrowth'] < 0.05:
        operational_risk_scores['RevenueGrowth'] = 3
    else:
        operational_risk_scores['RevenueGrowth'] = 4

    # Operating Expense Growth Scoring
    if data['OperatingExpenseGrowth'] < 0.05:
        operational_risk_scores['OperatingExpenseGrowth'] = 1
    elif 0.05 <= data['OperatingExpenseGrowth'] <= 0.1:
        operational_risk_scores['OperatingExpenseGrowth'] = 2
    elif 0.1 <= data['OperatingExpenseGrowth'] < 0.15:
        operational_risk_scores['OperatingExpenseGrowth'] = 3
    else:
        operational_risk_scores['OperatingExpenseGrowth'] = 4

    return operational_risk_scores

def calculate_financial_health_scores(data):
    financial_health_scores = {}

    # Debt Service Coverage Ratio (DSCR) Scoring
    if data['DSCR'] > 2:
        financial_health_scores['DSCR'] = 1
    elif 1.5 <= data['DSCR'] <= 2:
        financial_health_scores['DSCR'] = 2
    elif 1 <= data['DSCR'] < 1.5:
        financial_health_scores['DSCR'] = 3
    else:
        financial_health_scores['DSCR'] = 4

    # Interest Coverage Ratio Scoring
    if data['InterestCoverage'] > 4:
        financial_health_scores['InterestCoverage'] = 1
    elif 3 <= data['InterestCoverage'] <= 4:
        financial_health_scores['InterestCoverage'] = 2
    elif 2 <= data['InterestCoverage'] < 3:
        financial_health_scores['InterestCoverage'] = 3
    else:
        financial_health_scores['InterestCoverage'] = 4

    return financial_health_scores

def calculate_sector_industry_risk_scores(data):
    sector_industry_risk_scores = {}

    # Sector/Industry Beta Scoring
    if data['IndustryBeta'] < 0.8:
        sector_industry_risk_scores['IndustryBeta'] = 1
    elif 0.8 <= data['IndustryBeta'] < 1.0:
        sector_industry_risk_scores['IndustryBeta'] = 2
    elif 1.0 <= data['IndustryBeta'] < 1.2:
        sector_industry_risk_scores['IndustryBeta'] = 3
    else:
        sector_industry_risk_scores['IndustryBeta'] = 4

    # Sector/Industry Growth Scoring
    if data['IndustryGrowth'] > 0.1:
        sector_industry_risk_scores['IndustryGrowth'] = 1
    elif 0.05 <= data['IndustryGrowth'] <= 0.1:
        sector_industry_risk_scores['IndustryGrowth'] = 2
    elif 0 <= data['IndustryGrowth'] < 0.05:
        sector_industry_risk_scores['IndustryGrowth'] = 3
    else:
        sector_industry_risk_scores['IndustryGrowth'] = 4

    return sector_industry_risk_scores

def calculate_total_risk_score(market_risk, liquidity_risk, leverage_risk, profitability_risk, valuation_risk, dividend_risk, operational_risk, financial_health, sector_industry_risk):
    # Combine scores and average them
    total_score = sum([sum(market_risk.values()), sum(liquidity_risk.values()), sum(leverage_risk.values()),
                       sum(profitability_risk.values()), sum(valuation_risk.values()), sum(dividend_risk.values()),
                       sum(operational_risk.values()), sum(financial_health.values()), sum(sector_industry_risk.values())])
    
    total_params = len(market_risk) + len(liquidity_risk) + len(leverage_risk) + len(profitability_risk) + \
                   len(valuation_risk) + len(dividend_risk) + len(operational_risk) + len(financial_health) + \
                   len(sector_industry_risk)
    
    return total_score / total_params

# Sample usage with hypothetical stock data
sample_stock_data = {
    'Beta': 1.2,
    '52WeekChange': 0.1,
    'DayHigh': 150,
    'DayLow': 145,
    'AvgVolume': 1000000,
    'CurrentRatio': 2.5,
    'QuickRatio': 1.5,
    'Volume': 1200000,
    'DebtToEquity': 0.5,
    'TotalDebt': 50000000,
    'Equity': 100000000,
    'ProfitMargin': 0.18,
    'GrossMargin': 0.45,
    'EBITDAMargin': 0.28,
    'ROA': 0.08,
    'ROE': 0.12,
    'PE': 15,
    'PriceToBook': 2,
    'PriceToSales': 1.5,
    'TrailingPE': 18,
    'DividendYield': 0.04,
    'PayoutRatio': 0.4,
    'ExDividendDate': '2024-05-01',
    'NetIncomeGrowth': 0.08,
    'RevenueGrowth': 0.12,
    'OperatingExpenseGrowth': 0.08,
    'DSCR': 2.5,
    'InterestCoverage': 3.5,
    'IndustryBeta': 0.9,
    'IndustryGrowth': 0.08
}

# Calculating individual risk scores
market_risk_scores = calculate_market_risk_scores(sample_stock_data)
liquidity_risk_scores = calculate_liquidity_risk_scores(sample_stock_data)
leverage_risk_scores = calculate_leverage_risk_scores(sample_stock_data)
profitability_risk_scores = calculate_profitability_risk_scores(sample_stock_data)
valuation_risk_scores = calculate_valuation_risk_scores(sample_stock_data)
dividend_risk_scores = calculate_dividend_risk_scores(sample_stock_data)
operational_risk_scores = calculate_operational_risk_scores(sample_stock_data)
financial_health_scores = calculate_financial_health_scores(sample_stock_data)
sector_industry_risk_scores = calculate_sector_industry_risk_scores(sample_stock_data)

# Calculate total risk score
total_risk_score = calculate_total_risk_score(market_risk_scores, liquidity_risk_scores, leverage_risk_scores, 
                                              profitability_risk_scores, valuation_risk_scores, dividend_risk_scores, 
                                              operational_risk_scores, financial_health_scores, sector_industry_risk_scores)

print(f"Total Risk Score: {total_risk_score}")
