# src/config/settings.py
"""
Configuration settings for the financial dashboard
"""

# Yahoo Finance API settings (yfinance doesn't actually require an API key)
YFINANCE_TIMEOUT = 10  # seconds
YFINANCE_RETRIES = 3

# Database settings
DATABASE_PATH = 'data/database/finance.db'

# Default tickers
DEFAULT_TICKERS = ['AAPL', 'MSFT', 'GOOG', 'AMZN']

# Display settings
MAX_TICKERS = 10  # Maximum number of tickers to display at once