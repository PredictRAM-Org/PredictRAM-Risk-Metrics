import streamlit as st
import pandas as pd

# Function to calculate risk score
def calculate_risk_score(data):
    # Initialize an empty dictionary to store risk scores
    risk_scores = {}

    # Market Risk Metrics
    beta = data.get('beta', 0)
    week_change = data.get('52_week_change', 0)
    day_high = data.get('day_high', 0)
    day_low = data.get('day_low', 0)
    avg_volume = data.get('average_volume', 1)  # Avoid division by zero
    
    if beta < 0.5:
        risk_scores['Beta'] = 1
    elif 0.5 <= beta < 0.9:
        risk_scores['Beta'] = 2
    elif 0.9 <= beta < 1.5:
        risk_scores['Beta'] = 3
    else:
        risk_scores['Beta'] = 4

    if week_change > 20:
        risk_scores['52-Week Change'] = 1
    elif 0 <= week_change <= 20:
        risk_scores['52-Week Change'] = 2
    elif -10 <= week_change < 0:
        risk_scores['52-Week Change'] = 3
    else:
        risk_scores['52-Week Change'] = 4

    volatility = day_high - day_low
    if volatility < avg_volume:
        risk_scores['Price Volatility'] = 1
    elif avg_volume <= volatility < 2 * avg_volume:
        risk_scores['Price Volatility'] = 2
    else:
        risk_scores['Price Volatility'] = 3

    # Liquidity Risk Metrics
    current_ratio = data.get('current_ratio', 0)
    quick_ratio = data.get('quick_ratio', 0)
    volume = data.get('volume', 0)

    if current_ratio > 3:
        risk_scores['Current Ratio'] = 1
    elif 2 <= current_ratio <= 3:
        risk_scores['Current Ratio'] = 2
    elif 1 <= current_ratio < 2:
        risk_scores['Current Ratio'] = 3
    else:
        risk_scores['Current Ratio'] = 4

    if quick_ratio > 1.5:
        risk_scores['Quick Ratio'] = 1
    elif 1 <= quick_ratio <= 1.5:
        risk_scores['Quick Ratio'] = 2
    elif 0.5 <= quick_ratio < 1:
        risk_scores['Quick Ratio'] = 3
    else:
        risk_scores['Quick Ratio'] = 4

    if volume > 3 * avg_volume:
        risk_scores['Volume vs. Average Volume'] = 1
    elif 2 * avg_volume <= volume <= 3 * avg_volume:
        risk_scores['Volume vs. Average Volume'] = 2
    elif avg_volume <= volume < 2 * avg_volume:
        risk_scores['Volume vs. Average Volume'] = 3
    else:
        risk_scores['Volume vs. Average Volume'] = 4

    # Leverage Risk Metrics
    debt_to_equity = data.get('debt_to_equity', 0)
    total_debt = data.get('total_debt', 0)
    equity = data.get('equity', 1)  # Avoid division by zero

    if debt_to_equity < 0.3:
        risk_scores['Debt-to-Equity Ratio'] = 1
    elif 0.3 <= debt_to_equity < 0.6:
        risk_scores['Debt-to-Equity Ratio'] = 2
    elif 0.6 <= debt_to_equity < 1:
        risk_scores['Debt-to-Equity Ratio'] = 3
    else:
        risk_scores['Debt-to-Equity Ratio'] = 4

    total_debt_ratio = total_debt / equity
    if total_debt_ratio <= 0.2:
        risk_scores['Total Debt'] = 1
    elif 0.2 < total_debt_ratio <= 0.5:
        risk_scores['Total Debt'] = 2
    elif 0.5 < total_debt_ratio <= 0.7:
        risk_scores['Total Debt'] = 3
    else:
        risk_scores['Total Debt'] = 4

    # Profitability Risk Metrics
    profit_margin = data.get('profit_margin', 0)
    gross_margin = data.get('gross_margin', 0)
    ebitda_margin = data.get('ebitda_margin', 0)
    roa = data.get('roa', 0)
    roe = data.get('roe', 0)

    if profit_margin > 20:
        risk_scores['Profit Margins'] = 1
    elif 10 <= profit_margin <= 20:
        risk_scores['Profit Margins'] = 2
    elif 5 <= profit_margin < 10:
        risk_scores['Profit Margins'] = 3
    else:
        risk_scores['Profit Margins'] = 4

    if gross_margin > 50:
        risk_scores['Gross Margins'] = 1
    elif 30 <= gross_margin <= 50:
        risk_scores['Gross Margins'] = 2
    elif 20 <= gross_margin < 30:
        risk_scores['Gross Margins'] = 3
    else:
        risk_scores['Gross Margins'] = 4

    if ebitda_margin > 30:
        risk_scores['EBITDA Margins'] = 1
    elif 20 <= ebitda_margin <= 30:
        risk_scores['EBITDA Margins'] = 2
    elif 10 <= ebitda_margin < 20:
        risk_scores['EBITDA Margins'] = 3
    else:
        risk_scores['EBITDA Margins'] = 4

    if roa > 10:
        risk_scores['Return on Assets'] = 1
    elif 5 <= roa <= 10:
        risk_scores['Return on Assets'] = 2
    elif 2 <= roa < 5:
        risk_scores['Return on Assets'] = 3
    else:
        risk_scores['Return on Assets'] = 4

    if roe > 15:
        risk_scores['Return on Equity'] = 1
    elif 10 <= roe <= 15:
        risk_scores['Return on Equity'] = 2
    elif 5 <= roe < 10:
        risk_scores['Return on Equity'] = 3
    else:
        risk_scores['Return on Equity'] = 4

    # Valuation Risk Metrics
    pe_ratio = data.get('pe_ratio', 0)
    pb_ratio = data.get('pb_ratio', 0)
    ps_ratio = data.get('ps_ratio', 0)
    trailing_pe = data.get('trailing_pe', 0)

    if pe_ratio < 10:
        risk_scores['Price-to-Earnings Ratio'] = 1
    elif 10 <= pe_ratio < 20:
        risk_scores['Price-to-Earnings Ratio'] = 2
    elif 20 <= pe_ratio < 30:
        risk_scores['Price-to-Earnings Ratio'] = 3
    else:
        risk_scores['Price-to-Earnings Ratio'] = 4

    if pb_ratio < 1:
        risk_scores['Price-to-Book Ratio'] = 1
    elif 1 <= pb_ratio < 2:
        risk_scores['Price-to-Book Ratio'] = 2
    elif 2 <= pb_ratio < 4:
        risk_scores['Price-to-Book Ratio'] = 3
    else:
        risk_scores['Price-to-Book Ratio'] = 4

    if ps_ratio < 1:
        risk_scores['Price-to-Sales Ratio'] = 1
    elif 1 <= ps_ratio < 2:
        risk_scores['Price-to-Sales Ratio'] = 2
    elif 2 <= ps_ratio < 4:
        risk_scores['Price-to-Sales Ratio'] = 3
    else:
        risk_scores['Price-to-Sales Ratio'] = 4

    if trailing_pe < 10:
        risk_scores['Trailing PE'] = 1
    elif 10 <= trailing_pe < 20:
        risk_scores['Trailing PE'] = 2
    elif 20 <= trailing_pe < 30:
        risk_scores['Trailing PE'] = 3
    else:
        risk_scores['Trailing PE'] = 4

       # Dividend Risk Metrics
    dividend_payout_ratio = data.get('dividend_payout_ratio', 0)
    trailing_annual_dividend_yield = data.get('trailing_annual_dividend_yield', 0)
    dividend_history = data.get('dividend_history', 'Stable')

    if dividend_payout_ratio < 30:
        risk_scores['Dividend Payout Ratio'] = 1
    elif 30 <= dividend_payout_ratio < 50:
        risk_scores['Dividend Payout Ratio'] = 2
    elif 50 <= dividend_payout_ratio < 70:
        risk_scores['Dividend Payout Ratio'] = 3
    else:
        risk_scores['Dividend Payout Ratio'] = 4

    if trailing_annual_dividend_yield > 5:
        risk_scores['Dividend Yield'] = 1
    elif 3 <= trailing_annual_dividend_yield <= 5:
        risk_scores['Dividend Yield'] = 2
    elif 1 <= trailing_annual_dividend_yield < 3:
        risk_scores['Dividend Yield'] = 3
    else:
        risk_scores['Dividend Yield'] = 4

    if dividend_history == 'Stable':
        risk_scores['Dividend History'] = 1
    elif dividend_history == 'Growing':
        risk_scores['Dividend History'] = 2
    elif dividend_history == 'Variable':
        risk_scores['Dividend History'] = 3
    else:
        risk_scores['Dividend History'] = 4

    # Operational Risk Metrics
    operating_margin = data.get('operating_margin', 0)
    revenue_growth = data.get('revenue_growth', 0)

    if operating_margin > 20:
        risk_scores['Operating Margin'] = 1
    elif 10 <= operating_margin <= 20:
        risk_scores['Operating Margin'] = 2
    elif 5 <= operating_margin < 10:
        risk_scores['Operating Margin'] = 3
    else:
        risk_scores['Operating Margin'] = 4

    if revenue_growth > 15:
        risk_scores['Revenue Growth'] = 1
    elif 5 <= revenue_growth <= 15:
        risk_scores['Revenue Growth'] = 2
    elif 0 <= revenue_growth < 5:
        risk_scores['Revenue Growth'] = 3
    else:
        risk_scores['Revenue Growth'] = 4

    return risk_scores

# Load stock data (example)
@st.cache
def load_stock_data(file_path):
    return pd.read_excel(file_path)

# Define Streamlit app
def main():
    st.title("Comprehensive Risk Meter Dashboard")

    # Load data
    data_file = st.file_uploader("Upload Stock Data", type=['xlsx'])
    if data_file:
        data = load_stock_data(data_file)
        for index, row in data.iterrows():
            st.header(f"Stock: {row['symbol']}")
            risk_scores = calculate_risk_score(row)
            
            # Display risk scores
            st.write("### Risk Scores")
            st.write(pd.DataFrame(risk_scores.items(), columns=['Metric', 'Score']))
            
            # Display risk descriptions
            st.write("### Risk Descriptions")
            for metric, score in risk_scores.items():
                description = ""
                if metric == 'Beta':
                    description = "1: Low risk - stable stock; 4: High risk - volatile stock."
                elif metric == '52-Week Change':
                    description = "1: Significant growth; 4: Significant decline."
                elif metric == 'Price Volatility':
                    description = "1: Low volatility; 3: High volatility."
                elif metric == 'Current Ratio':
                    description = "1: Strong liquidity; 4: Weak liquidity."
                elif metric == 'Quick Ratio':
                    description = "1: Strong short-term liquidity; 4: Weak short-term liquidity."
                elif metric == 'Volume vs. Average Volume':
                    description = "1: High trading volume; 4: Low trading volume."
                elif metric == 'Debt-to-Equity Ratio':
                    description = "1: Low leverage; 4: High leverage."
                elif metric == 'Total Debt':
                    description = "1: Low debt; 4: High debt."
                elif metric == 'Profit Margins':
                    description = "1: High profitability; 4: Low profitability."
                elif metric == 'Gross Margins':
                    description = "1: High gross margins; 4: Low gross margins."
                elif metric == 'EBITDA Margins':
                    description = "1: High EBITDA margins; 4: Low EBITDA margins."
                elif metric == 'Return on Assets':
                    description = "1: High efficiency; 4: Low efficiency."
                elif metric == 'Return on Equity':
                    description = "1: High returns; 4: Low returns."
                elif metric == 'Price-to-Earnings Ratio':
                    description = "1: Undervalued; 4: Overvalued."
                elif metric == 'Price-to-Book Ratio':
                    description = "1: Undervalued; 4: Overvalued."
                elif metric == 'Price-to-Sales Ratio':
                    description = "1: Undervalued; 4: Overvalued."
                elif metric == 'Trailing PE':
                    description = "1: Undervalued; 4: Overvalued."
                elif metric == 'Dividend Payout Ratio':
                    description = "1: Low payout ratio; 4: High payout ratio."
                elif metric == 'Dividend Yield':
                    description = "1: High yield; 4: Low yield."
                elif metric == 'Dividend History':
                    description = "1: Stable history; 4: Unstable history."
                elif metric == 'Operating Margin':
                    description = "1: High margin; 4: Low margin."
                elif metric == 'Revenue Growth':
                    description = "1: High growth; 4: Low growth."

                st.write(f"{metric}: {description} (Score: {score})")

if __name__ == "__main__":
    main()
