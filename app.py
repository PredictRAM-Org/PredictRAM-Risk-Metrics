import yfinance as yf
import streamlit as st

def fetch_stock_data(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info
    return info

def calculate_market_risk(info):
    beta = info.get('beta', 0)
    week_change = info.get('52WeekChange', 0)
    day_high = info.get('dayHigh', 0)
    day_low = info.get('dayLow', 0)
    average_volume = info.get('averageVolume', 1)
    
    # Beta Score
    if beta < 0.5:
        beta_score = 1
    elif 0.5 <= beta < 0.9:
        beta_score = 2
    elif 0.9 <= beta < 1.5:
        beta_score = 3
    else:
        beta_score = 4

    # 52-Week Change Score
    if week_change > 0.2:
        change_score = 1
    elif 0 <= week_change <= 0.2:
        change_score = 2
    elif -0.1 <= week_change < 0:
        change_score = 3
    else:
        change_score = 4

    # Price Volatility Score
    volatility = day_high - day_low
    if volatility < average_volume:
        volatility_score = 1
    elif average_volume <= volatility < 2 * average_volume:
        volatility_score = 2
    else:
        volatility_score = 3

    return beta_score, change_score, volatility_score

def calculate_liquidity_risk(info):
    current_ratio = info.get('currentRatio', 0)
    quick_ratio = info.get('quickRatio', 0)
    volume = info.get('volume', 0)
    average_volume = info.get('averageVolume', 1)
    
    # Current Ratio Score
    if current_ratio > 3:
        current_ratio_score = 1
    elif 2 <= current_ratio <= 3:
        current_ratio_score = 2
    elif 1 <= current_ratio < 2:
        current_ratio_score = 3
    else:
        current_ratio_score = 4

    # Quick Ratio Score
    if quick_ratio > 1.5:
        quick_ratio_score = 1
    elif 1 <= quick_ratio <= 1.5:
        quick_ratio_score = 2
    elif 0.5 <= quick_ratio < 1:
        quick_ratio_score = 3
    else:
        quick_ratio_score = 4

    # Volume vs. Average Volume Score
    if volume > 3 * average_volume:
        volume_score = 1
    elif 2 * average_volume <= volume <= 3 * average_volume:
        volume_score = 2
    elif average_volume <= volume < 2 * average_volume:
        volume_score = 3
    else:
        volume_score = 4

    return current_ratio_score, quick_ratio_score, volume_score

def main():
    st.title("Stock Analysis")

    symbol = st.text_input("Enter Stock Symbol")

    if symbol:
        info = fetch_stock_data(symbol)
        market_scores = calculate_market_risk(info)
        liquidity_scores = calculate_liquidity_risk(info)

        st.subheader("Market Risk Scores")
        st.write(f"Beta Score: {market_scores[0]}")
        st.write(f"52-Week Change Score: {market_scores[1]}")
        st.write(f"Price Volatility Score: {market_scores[2]}")

        st.subheader("Liquidity Risk Scores")
        st.write(f"Current Ratio Score: {liquidity_scores[0]}")
        st.write(f"Quick Ratio Score: {liquidity_scores[1]}")
        st.write(f"Volume vs. Average Volume Score: {liquidity_scores[2]}")

if __name__ == "__main__":
    main()
