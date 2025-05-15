import pandas as pd

def calculate_correlation_matrix(ticker_dfs):
    """
    Calculate correlation matrix between multiple tickers
    """
    # Combine close prices from all tickers
    close_prices = pd.DataFrame()
    
    for ticker, df in ticker_dfs.items():
        close_prices[ticker] = df['Close']
    
    # Calculate daily returns
    returns = close_prices.pct_change().dropna()
    
    # Calculate correlation matrix
    correlation_matrix = returns.corr()
    
    return correlation_matrix