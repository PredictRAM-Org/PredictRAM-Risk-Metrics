import pandas as pd
import streamlit as st

# Load the stock data from Excel
file_path = 'all_stocks_data.xlsx'  # Update this path as needed
stock_data = pd.read_excel(file_path)

# Print column names to verify
print("Column Names:", stock_data.columns.tolist())

def calculate_risk_metrics(stock):
    metrics = {}

    # Market Risk Metrics
    beta = stock.get('beta', None)
    if beta is not None:
        if beta < 0.5:
            metrics['Beta'] = (1, 'Low Risk')
        elif 0.5 <= beta < 0.9:
            metrics['Beta'] = (2, 'Moderate Risk')
        elif 0.9 <= beta < 1.5:
            metrics['Beta'] = (3, 'High Risk')
        else:
            metrics['Beta'] = (4, 'Very High Risk')

    change_52_week = stock.get('52_Week_Change', None)
    if change_52_week is not None:
        if change_52_week > 20:
            metrics['52-Week Change'] = (1, 'High Positive Performance')
        elif 0 <= change_52_week <= 20:
            metrics['52-Week Change'] = (2, 'Positive Performance')
        elif -10 <= change_52_week < 0:
            metrics['52-Week Change'] = (3, 'Negative Performance')
        else:
            metrics['52-Week Change'] = (4, 'High Negative Performance')

    day_high = stock.get('Day_High', None)
    day_low = stock.get('Day_Low', None)
    avg_volume = stock.get('Average_Volume', None)
    if day_high is not None and day_low is not None and avg_volume is not None:
        volatility = day_high - day_low
        if volatility < avg_volume:
            metrics['Price Volatility'] = (1, 'Low Volatility')
        elif avg_volume <= volatility < 2 * avg_volume:
            metrics['Price Volatility'] = (2, 'Moderate Volatility')
        else:
            metrics['Price Volatility'] = (3, 'High Volatility')

    # Liquidity Risk Metrics
    current_ratio = stock.get('Current_Ratio', None)
    if current_ratio is not None:
        if current_ratio > 3:
            metrics['Current Ratio'] = (1, 'Excellent Liquidity')
        elif 2 <= current_ratio <= 3:
            metrics['Current Ratio'] = (2, 'Good Liquidity')
        elif 1 <= current_ratio < 2:
            metrics['Current Ratio'] = (3, 'Adequate Liquidity')
        else:
            metrics['Current Ratio'] = (4, 'Poor Liquidity')

    quick_ratio = stock.get('Quick_Ratio', None)
    if quick_ratio is not None:
        if quick_ratio > 1.5:
            metrics['Quick Ratio'] = (1, 'Excellent Liquidity')
        elif 1 <= quick_ratio <= 1.5:
            metrics['Quick Ratio'] = (2, 'Good Liquidity')
        elif 0.5 <= quick_ratio < 1:
            metrics['Quick Ratio'] = (3, 'Adequate Liquidity')
        else:
            metrics['Quick Ratio'] = (4, 'Poor Liquidity')

    volume = stock.get('Volume', None)
    if volume is not None and avg_volume is not None:
        if volume > 3 * avg_volume:
            metrics['Volume vs. Average Volume'] = (1, 'High Liquidity')
        elif 2 * avg_volume <= volume <= 3 * avg_volume:
            metrics['Volume vs. Average Volume'] = (2, 'Good Liquidity')
        elif avg_volume <= volume < 2 * avg_volume:
            metrics['Volume vs. Average Volume'] = (3, 'Moderate Liquidity')
        else:
            metrics['Volume vs. Average Volume'] = (4, 'Low Liquidity')

    # Leverage Risk Metrics
    debt_to_equity = stock.get('Debt_to_Equity', None)
    if debt_to_equity is not None:
        if debt_to_equity < 0.3:
            metrics['Debt-to-Equity Ratio'] = (1, 'Low Leverage')
        elif 0.3 <= debt_to_equity < 0.6:
            metrics['Debt-to-Equity Ratio'] = (2, 'Moderate Leverage')
        elif 0.6 <= debt_to_equity < 1.0:
            metrics['Debt-to-Equity Ratio'] = (3, 'High Leverage')
        else:
            metrics['Debt-to-Equity Ratio'] = (4, 'Very High Leverage')

    total_debt = stock.get('Total_Debt', None)
    equity = stock.get('Equity', None)
    if total_debt is not None and equity is not None:
        debt_to_equity_ratio = total_debt / equity
        if debt_to_equity_ratio <= 0.2:
            metrics['Total Debt'] = (1, 'Low Risk')
        elif 0.2 < debt_to_equity_ratio <= 0.5:
            metrics['Total Debt'] = (2, 'Moderate Risk')
        elif 0.5 < debt_to_equity_ratio <= 0.7:
            metrics['Total Debt'] = (3, 'High Risk')
        else:
            metrics['Total Debt'] = (4, 'Very High Risk')

    # Profitability Risk Metrics
    profit_margin = stock.get('Profit_Margin', None)
    if profit_margin is not None:
        if profit_margin > 20:
            metrics['Profit Margin'] = (1, 'High Profitability')
        elif 10 <= profit_margin <= 20:
            metrics['Profit Margin'] = (2, 'Good Profitability')
        elif 5 <= profit_margin < 10:
            metrics['Profit Margin'] = (3, 'Moderate Profitability')
        else:
            metrics['Profit Margin'] = (4, 'Low Profitability')

    gross_margin = stock.get('Gross_Margin', None)
    if gross_margin is not None:
        if gross_margin > 50:
            metrics['Gross Margin'] = (1, 'High Margins')
        elif 30 <= gross_margin <= 50:
            metrics['Gross Margin'] = (2, 'Good Margins')
        elif 20 <= gross_margin < 30:
            metrics['Gross Margin'] = (3, 'Moderate Margins')
        else:
            metrics['Gross Margin'] = (4, 'Low Margins')

    ebitda_margin = stock.get('EBITDA_Margin', None)
    if ebitda_margin is not None:
        if ebitda_margin > 30:
            metrics['EBITDA Margin'] = (1, 'High Margins')
        elif 20 <= ebitda_margin <= 30:
            metrics['EBITDA Margin'] = (2, 'Good Margins')
        elif 10 <= ebitda_margin < 20:
            metrics['EBITDA Margin'] = (3, 'Moderate Margins')
        else:
            metrics['EBITDA Margin'] = (4, 'Low Margins')

    roa = stock.get('ROA', None)
    if roa is not None:
        if roa > 10:
            metrics['Return on Assets (ROA)'] = (1, 'High Return')
        elif 5 <= roa <= 10:
            metrics['Return on Assets (ROA)'] = (2, 'Good Return')
        elif 2 <= roa < 5:
            metrics['Return on Assets (ROA)'] = (3, 'Moderate Return')
        else:
            metrics['Return on Assets (ROA)'] = (4, 'Low Return')

    roe = stock.get('ROE', None)
    if roe is not None:
        if roe > 15:
            metrics['Return on Equity (ROE)'] = (1, 'High Return')
        elif 10 <= roe <= 15:
            metrics['Return on Equity (ROE)'] = (2, 'Good Return')
        elif 5 <= roe < 10:
            metrics['Return on Equity (ROE)'] = (3, 'Moderate Return')
        else:
            metrics['Return on Equity (ROE)'] = (4, 'Low Return')

    # Valuation Risk Metrics
    pe_ratio = stock.get('P_E_Ratio', None)
    if pe_ratio is not None:
        if pe_ratio < 10:
            metrics['Price-to-Earnings Ratio (P/E)'] = (1, 'Undervalued')
        elif 10 <= pe_ratio < 20:
            metrics['Price-to-Earnings Ratio (P/E)'] = (2, 'Fairly Valued')
        elif 20 <= pe_ratio < 30:
            metrics['Price-to-Earnings Ratio (P/E)'] = (3, 'Overvalued')
        else:
            metrics['Price-to-Earnings Ratio (P/E)'] = (4, 'Highly Overvalued')

    price_to_book = stock.get('Price_to_Book', None)
    if price_to_book is not None:
        if price_to_book < 1:
            metrics['Price-to-Book Ratio'] = (1, 'Undervalued')
        elif 1 <= price_to_book < 2:
            metrics['Price-to-Book Ratio'] = (2, 'Fairly Valued')
        elif 2 <= price_to_book < 4:
            metrics['Price-to-Book Ratio'] = (3, 'Overvalued')
        else:
            metrics['Price-to-Book Ratio'] = (4, 'Highly Overvalued')

    price_to_sales = stock.get('Price_to_Sales', None)
    if price_to_sales is not None:
        if price_to_sales < 1:
            metrics['Price-to-Sales Ratio'] = (1, 'Undervalued')
        elif 1 <= price_to_sales < 2:
            metrics['Price-to-Sales Ratio'] = (2, 'Fairly Valued')
        elif 2 <= price_to_sales < 4:
            metrics['Price-to-Sales Ratio'] = (3, 'Overvalued')
        else:
            metrics['Price-to-Sales Ratio'] = (4, 'Highly Overvalued')

    trailing_pe = stock.get('Trailing_PE', None)
    if trailing_pe is not None:
        if trailing_pe < 10:
            metrics['Trailing PE'] = (1, 'Undervalued')
        elif 10 <= trailing_pe < 20:
            metrics['Trailing PE'] = (2, 'Fairly Valued')
        elif 20 <= trailing_pe < 30:
            metrics['Trailing PE'] = (3, 'Overvalued')
        else:
            metrics['Trailing PE'] = (4, 'Highly Overvalued')

    # Dividend Risk Metrics
    dividend_payout_ratio = stock.get('Dividend_Payout_Ratio', None)
    if dividend_payout_ratio is not None:
        if dividend_payout_ratio < 30:
            metrics['Dividend Payout Ratio'] = (1, 'Low Risk')
        elif 30 <= dividend_payout_ratio < 50:
            metrics['Dividend Payout Ratio'] = (2, 'Moderate Risk')
        elif 50 <= dividend_payout_ratio < 70:
            metrics['Dividend Payout Ratio'] = (3, 'High Risk')
        else:
            metrics['Dividend Payout Ratio'] = (4, 'Very High Risk')

    trailing_dividend_yield = stock.get('Trailing_Annual_Dividend_Yield', None)
    if trailing_dividend_yield is not None:
        if trailing_dividend_yield > 6:
            metrics['Trailing Annual Dividend Yield'] = (1, 'High Yield')
        elif 4 <= trailing_dividend_yield <= 6:
            metrics['Trailing Annual Dividend Yield'] = (2, 'Moderate Yield')
        elif 2 <= trailing_dividend_yield < 4:
            metrics['Trailing Annual Dividend Yield'] = (3, 'Low Yield')
        else:
            metrics['Trailing Annual Dividend Yield'] = (4, 'Very Low Yield')

    dividend_history = stock.get('Dividend_History', None)
    if dividend_history is not None:
        if dividend_history == 'Stable or Increasing':
            metrics['Dividend History'] = (1, 'Low Risk')
        elif dividend_history == 'Mixed':
            metrics['Dividend History'] = (2, 'Moderate Risk')
        elif dividend_history == 'Irregular':
            metrics['Dividend History'] = (3, 'High Risk')
        else:
            metrics['Dividend History'] = (4, 'Very High Risk')

    # Operational Risk Metrics
    operating_cash_flow = stock.get('Operating_Cash_Flow', None)
    if operating_cash_flow is not None:
        if operating_cash_flow > 0 and stock.get('Operating_Cash_Flow_Growth', 0) > 0:
            metrics['Operating Cash Flow'] = (1, 'Low Risk')
        elif operating_cash_flow > 0:
            metrics['Operating Cash Flow'] = (2, 'Moderate Risk')
        elif operating_cash_flow <= 0 and stock.get('Operating_Cash_Flow_Growth', 0) < 0:
            metrics['Operating Cash Flow'] = (3, 'High Risk')
        else:
            metrics['Operating Cash Flow'] = (4, 'Very High Risk')

    free_cash_flow = stock.get('Free_Cash_Flow', None)
    if free_cash_flow is not None:
        if free_cash_flow > 0 and stock.get('Free_Cash_Flow_Growth', 0) > 0:
            metrics['Free Cash Flow'] = (1, 'Low Risk')
        elif free_cash_flow > 0:
            metrics['Free Cash Flow'] = (2, 'Moderate Risk')
        elif free_cash_flow < 0 and stock.get('Free_Cash_Flow_Growth', 0) < 0:
            metrics['Free Cash Flow'] = (3, 'High Risk')
        else:
            metrics['Free Cash Flow'] = (4, 'Very High Risk')

    revenue_growth = stock.get('Revenue_Growth', None)
    if revenue_growth is not None:
        if revenue_growth > 15:
            metrics['Revenue Growth'] = (1, 'High Growth')
        elif 10 <= revenue_growth <= 15:
            metrics['Revenue Growth'] = (2, 'Good Growth')
        elif 5 <= revenue_growth < 10:
            metrics['Revenue Growth'] = (3, 'Moderate Growth')
        else:
            metrics['Revenue Growth'] = (4, 'Low Growth')

    # Financial Health Metrics
    book_value = stock.get('Book_Value', None)
    if book_value is not None:
        if book_value > stock.get('Book_Value_Prior', 0):
            metrics['Book Value'] = (1, 'Low Risk')
        elif book_value == stock.get('Book_Value_Prior', 0):
            metrics['Book Value'] = (2, 'Moderate Risk')
        elif book_value < stock.get('Book_Value_Prior', 0):
            metrics['Book Value'] = (3, 'High Risk')
        else:
            metrics['Book Value'] = (4, 'Very High Risk')

    enterprise_value = stock.get('Enterprise_Value', None)
    market_cap = stock.get('Market_Cap', None)
    if enterprise_value is not None and market_cap is not None:
        if enterprise_value < market_cap * 1.1:
            metrics['Enterprise Value'] = (1, 'Low Risk')
        elif enterprise_value < market_cap * 1.3:
            metrics['Enterprise Value'] = (2, 'Moderate Risk')
        elif enterprise_value < market_cap * 1.5:
            metrics['Enterprise Value'] = (3, 'High Risk')
        else:
            metrics['Enterprise Value'] = (4, 'Very High Risk')

    total_cash = stock.get('Total_Cash', None)
    total_liabilities = stock.get('Total_Liabilities', None)
    if total_cash is not None and total_liabilities is not None:
        cash_ratio = total_cash / total_liabilities
        if cash_ratio > 0.3:
            metrics['Total Cash'] = (1, 'High Liquidity')
        elif 0.15 <= cash_ratio <= 0.3:
            metrics['Total Cash'] = (2, 'Good Liquidity')
        elif 0.05 <= cash_ratio < 0.15:
            metrics['Total Cash'] = (3, 'Moderate Liquidity')
        else:
            metrics['Total Cash'] = (4, 'Low Liquidity')

    # Sector and Industry Risk Metrics
    industry_avg = stock.get('Industry_Average', None)
    revenue_per_share = stock.get('Revenue_Per_Share', None)
    if industry_avg is not None and revenue_per_share is not None:
        if revenue_per_share > industry_avg:
            metrics['Revenue Per Share'] = (1, 'High Performance')
        elif revenue_per_share == industry_avg:
            metrics['Revenue Per Share'] = (2, 'Moderate Performance')
        else:
            metrics['Revenue Per Share'] = (3, 'Low Performance')

    # Valuation vs. Industry Metrics
    industry_forward_pe = stock.get('Industry_Forward_PE', None)
    if industry_forward_pe is not None:
        if pe_ratio < industry_forward_pe:
            metrics['Industry Forward PE'] = (1, 'Undervalued')
        elif pe_ratio == industry_forward_pe:
            metrics['Industry Forward PE'] = (2, 'Fairly Valued')
        else:
            metrics['Industry Forward PE'] = (3, 'Overvalued')

    industry_trailing_pe = stock.get('Industry_Trailing_PE', None)
    if industry_trailing_pe is not None:
        if pe_ratio < industry_trailing_pe:
            metrics['Industry Trailing PE'] = (1, 'Undervalued')
        elif pe_ratio == industry_trailing_pe:
            metrics['Industry Trailing PE'] = (2, 'Fairly Valued')
        else:
            metrics['Industry Trailing PE'] = (3, 'Overvalued')

    industry_debt_to_equity = stock.get('Industry_Debt_to_Equity', None)
    if industry_debt_to_equity is not None:
        if debt_to_equity < industry_debt_to_equity:
            metrics['Industry Debt-to-Equity'] = (1, 'Low Risk')
        elif debt_to_equity == industry_debt_to_equity:
            metrics['Industry Debt-to-Equity'] = (2, 'Moderate Risk')
        else:
            metrics['Industry Debt-to-Equity'] = (3, 'High Risk')

    return metrics

def risk_meter(score):
    if score == 1:
        return "🔴"  # Red for High Risk
    elif score == 2:
        return "🟠"  # Orange for Moderate Risk
    elif score == 3:
        return "🟡"  # Yellow for Low Risk
    else:
        return "🟢"  # Green for Very Low Risk

def display_risk_meters(metrics):
    for metric, (score, description) in metrics.items():
        print(f"{metric}: {description} {risk_meter(score)}")

# Example usage
stock = {
    'Beta': 1.2,
    '52_Week_Change': 12,
    'Price_to_Earnings': 18,
    'Price_to_Book': 2.5,
    'Price_to_Sales': 1.8,
    'Trailing_PE': 22,
    'Dividend_Payout_Ratio': 35,
    'Trailing_Annual_Dividend_Yield': 4.5,
    'Dividend_History': 'Mixed',
    'Operating_Cash_Flow': 150000,
    'Operating_Cash_Flow_Growth': 10,
    'Free_Cash_Flow': 120000,
    'Free_Cash_Flow_Growth': 8,
    'Revenue_Growth': 12,
    'Book_Value': 500000,
    'Book_Value_Prior': 450000,
    'Enterprise_Value': 1200000,
    'Market_Cap': 1100000,
    'Total_Cash': 350000,
    'Total_Liabilities': 1000000,
    'Industry_Average': 1000,
    'Revenue_Per_Share': 1200,
    'Industry_Forward_PE': 17,
    'Industry_Trailing_PE': 20,
    'Industry_Debt_to_Equity': 0.6
}

metrics = calculate_risk_metrics(stock)
display_risk_meters(metrics)
