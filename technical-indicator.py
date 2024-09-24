import yfinance as yf
import pandas as pd
"""
RSI:
Buy: RSI < 30
Sell: RSI > 70


MACD:
Buy: MACD crosses above the signal line.
Sell: MACD crosses below the signal line.

Stochastic Oscillator:
Buy: %K < 20 (oversold).
Sell: %K > 80 (overbought).

ATR (Average True Range):
ATR doesn’t provide direct buy/sell signals but indicates volatility. A high ATR suggests high volatility.
"""


# RSI Calculation
def calculate_rsi(data, period=14):
    delta = data['Close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

# MACD Calculation
def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    short_ema = data['Close'].ewm(span=short_window, adjust=False).mean()
    long_ema = data['Close'].ewm(span=long_window, adjust=False).mean()
    
    macd = short_ema - long_ema
    signal_line = macd.ewm(span=signal_window, adjust=False).mean()
    
    return macd, signal_line

# Stochastic Oscillator Calculation
def calculate_stochastic(data, period=14, smooth_k=3, smooth_d=3):
    low_min = data['Low'].rolling(window=period).min()
    high_max = data['High'].rolling(window=period).max()
    
    stochastic_k = 100 * (data['Close'] - low_min) / (high_max - low_min)
    stochastic_d = stochastic_k.rolling(window=smooth_d).mean()
    
    return stochastic_k, stochastic_d

# ATR Calculation
def calculate_atr(data, period=14):
    high_low = data['High'] - data['Low']
    high_close = (data['High'] - data['Close'].shift()).abs()
    low_close = (data['Low'] - data['Close'].shift()).abs()
    
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    
    return atr

# Stock Data Fetching
def get_stock_data(ticker, period='3mo', interval='1d'):
    stock_data = yf.download(ticker, period=period, interval=interval)
    return stock_data

# Signal Check for RSI
def check_rsi_signal(rsi):
    if rsi.iloc[-1] > 70:
        return "RSI Signal: Sell (Overbought)"
    elif rsi.iloc[-1] < 30:
        return "RSI Signal: Buy (Oversold)"
    else:
        return "RSI Signal: No clear signal"

# Signal Check for MACD
def check_macd_signal(macd, signal_line):
    if macd.iloc[-1] > signal_line.iloc[-1] and macd.iloc[-2] < signal_line.iloc[-2]:
        return "MACD Signal: Buy"
    elif macd.iloc[-1] < signal_line.iloc[-1] and macd.iloc[-2] > signal_line.iloc[-2]:
        return "MACD Signal: Sell"
    else:
        return "MACD Signal: No clear signal"

# Signal Check for Stochastic Oscillator
def check_stochastic_signal(stochastic_k, stochastic_d):
    if stochastic_k.iloc[-1] > 80:
        return "Stochastic Oscillator: Sell (Overbought)"
    elif stochastic_k.iloc[-1] < 20:
        return "Stochastic Oscillator: Buy (Oversold)"
    else:
        return "Stochastic Oscillator: No clear signal"

# Signal Check for ATR
def check_atr_signal(atr):
    # ATR is often used as a volatility measure, so we do not generate direct buy/sell signals
    # We can print the ATR value and suggest that high ATR indicates high volatility
    return f"ATR (Average True Range) Value: {atr.iloc[-1]:.2f} (High ATR implies high volatility)"

# Main function
def analyze_stock(ticker):
    data = get_stock_data(ticker)
    
    # Calculate indicators
    rsi = calculate_rsi(data)
    macd, signal_line = calculate_macd(data)
    stochastic_k, stochastic_d = calculate_stochastic(data)
    atr = calculate_atr(data)
    
    # Get individual signals
    rsi_signal = check_rsi_signal(rsi)
    macd_signal = check_macd_signal(macd, signal_line)
    stochastic_signal = check_stochastic_signal(stochastic_k, stochastic_d)
    atr_signal = check_atr_signal(atr)
    
    # Print signals
    print(f"Stock: {ticker}")
    print(rsi_signal)
    print(macd_signal)
    print(stochastic_signal)
    print(atr_signal)

# Example usage
analyze_stock("MSFT")  # You can replace 'AAPL' with any stock ticker

