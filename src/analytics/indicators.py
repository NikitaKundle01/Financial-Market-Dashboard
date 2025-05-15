import pandas as pd
import numpy as np

def calculate_moving_averages(df, windows=[20, 50, 200]):
    """
    Calculate simple moving averages for given windows
    """
    for window in windows:
        df[f'SMA_{window}'] = df['Close'].rolling(window=window).mean()
    return df

def calculate_rsi(df, window=14):
    """
    Calculate Relative Strength Index (RSI)
    """
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df