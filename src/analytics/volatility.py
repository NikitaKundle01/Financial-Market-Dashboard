import pandas as pd
import numpy as np

def calculate_volatility(df, window=20):
    """
    Calculate historical volatility (standard deviation of returns)
    """
    # Ensure we're working with a DataFrame that has the expected structure
    if 'Close' not in df.columns:
        raise ValueError("DataFrame must contain 'Close' column")
    
    returns = np.log(df['Close'] / df['Close'].shift(1))
    df['Volatility'] = returns.rolling(window=window).std() * np.sqrt(252)  # Annualized
    return df

def calculate_bollinger_bands(df, window=20, num_std=2):
    """
    Calculate Bollinger Bands
    """
    # Ensure we're working with a Series (single column) for the calculations
    close_prices = df['Close'] if 'Close' in df else df
    
    # Calculate bands
    middle_band = close_prices.rolling(window=window).mean()
    std_dev = close_prices.rolling(window=window).std()
    
    # Assign to DataFrame
    df['Middle Band'] = middle_band
    df['Upper Band'] = middle_band + (std_dev * num_std)
    df['Lower Band'] = middle_band - (std_dev * num_std)
    
    return df