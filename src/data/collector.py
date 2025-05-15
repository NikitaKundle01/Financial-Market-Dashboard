# src/data/collector.py
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def fetch_real_time_data(tickers):
    """
    Fetch real-time market data for given tickers
    """
    data = yf.download(
        tickers=tickers,
        period="1d",
        interval="1m",
        group_by='ticker',
        progress=False
    )
    return data

def fetch_historical_data(tickers, period="1y"):
    """
    Fetch historical market data for given tickers
    """
    data = yf.download(
        tickers=tickers,
        period=period,
        group_by='ticker',
        progress=False,
        auto_adjust=True  # Added to handle the API change
    )
    return data