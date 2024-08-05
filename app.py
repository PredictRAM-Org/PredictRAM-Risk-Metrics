import pandas as pd
import streamlit as st

# Load the stock data from Excel
file_path = 'all_stocks_data.xlsx'  # Update this path as needed
stock_data = pd.read_excel(file_path)

# Function to calculate risk metrics and generate risk scores
def calculate_risk_metrics(stock):
    metrics = {}
    
    # Market Risk Metrics
    beta = stock['beta']
    if beta < 0.5:
        metrics['Beta'] = (1, 'Low Risk')
    elif 0.5 <= beta < 0.9:
        metrics['Beta'] = (2, 'Moderate Risk')
    elif 0.9 <= beta < 1.5:
        metrics['Beta'] = (3, 'High Risk')
    else:
        metrics['Beta'] = (4, 'Very High Risk')
    
    # 52-Week Change
    change_52_week = stock['52_Week_Change']
    if change_52_week > 20:
        metrics['52-Week Change'] = (1, 'High Positive Performance')
    elif 0 <= change_52_week <= 20:
        metrics['52-Week Change'] = (2, 'Positive Performance')
    elif -10 <= change_52_week < 0:
        metrics['52-Week Change'] = (3, 'Negative Performance')
    else:
        metrics['52-Week Change'] = (4, 'High Negative Performance')
    
    # Price Volatility
    day_high = stock['Day_High']
    day_low = stock['Day_Low']
    avg_volume = stock['Average_Volume']
    if (day_high - day_low) < avg_volume:
        metrics['Price Volatility'] = (1, 'Low Volatility')
    elif avg_volume <= (day_high - day_low) < 2 * avg_volume:
        metrics['Price Volatility'] = (2, 'Moderate Volatility')
    else:
        metrics['Price Volatility'] = (3, 'High Volatility')
    
    # Liquidity Risk Metrics
    current_ratio = stock['Current_Ratio']
    if current_ratio > 3:
        metrics['Current Ratio'] = (1, 'Excellent Liquidity')
    elif 2 <= current_ratio <= 3:
        metrics['Current Ratio'] = (2, 'Good Liquidity')
    elif 1 <= current_ratio < 2:
        metrics['Current Ratio'] = (3, 'Adequate Liquidity')
    else:
        metrics['Current Ratio'] = (4, 'Poor Liquidity')
    
    # Quick Ratio
    quick_ratio = stock['Quick_Ratio']
    if quick_ratio > 1.5:
        metrics['Quick Ratio'] = (1, 'Excellent Liquidity')
    elif 1 <= quick_ratio <= 1.5:
        metrics['Quick Ratio'] = (2, 'Good Liquidity')
    elif 0.5 <= quick_ratio < 1:
        metrics['Quick Ratio'] = (3, 'Adequate Liquidity')
    else:
        metrics['Quick Ratio'] = (4, 'Poor Liquidity')
    
    # Volume vs. Average Volume
    volume = stock['Volume']
    if volume > 3 * stock['Average_Volume']:
        metrics['Volume vs. Average Volume'] = (1, 'High Liquidity')
    elif 2 * stock['Average_Volume'] <= volume <= 3 * stock['Average_Volume']:
        metrics['Volume vs. Average Volume'] = (2, 'Good Liquidity')
    elif stock['Average_Volume'] <= volume < 2 * stock['Average_Volume']:
        metrics['Volume vs. Average Volume'] = (3, 'Moderate Liquidity')
    else:
        metrics['Volume vs. Average Volume'] = (4, 'Low Liquidity')
    
    # Add more metrics as needed...

    return metrics

# Streamlit app
st.title('Stock Risk Metrics Dashboard')

# Select stock symbol
stock_symbol = st.selectbox('Select Stock Symbol', stock_data['symbol'].unique())

# Filter the stock data based on the selected symbol
stock_info = stock_data[stock_data['symbol'] == stock_symbol].iloc[0]

# Calculate risk metrics for the selected stock
risk_metrics = calculate_risk_metrics(stock_info)

# Display risk scores and descriptions
for metric, (score, description) in risk_metrics.items():
    st.write(f"**{metric}:** Score {score} - {description}")

    # Display a risk meter bar
    bar_color = '#00FF00' if score == 1 else '#FFFF00' if score == 2 else '#FF8000' if score == 3 else '#FF0000'
    st.markdown(
        f"""
        <div style="background-color:{bar_color}; width: {score * 20}%; height: 20px; border-radius: 5px;"></div>
        """, unsafe_allow_html=True
    )
