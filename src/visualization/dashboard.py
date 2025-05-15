import streamlit as st
from src.data.collector import fetch_historical_data
from src.data.database import FinancialDatabase
from src.analytics.indicators import calculate_moving_averages, calculate_rsi
from src.analytics.volatility import calculate_volatility, calculate_bollinger_bands
from src.analytics.correlation import calculate_correlation_matrix
from src.visualization.charts import plot_price_chart, plot_rsi_chart, plot_correlation_heatmap
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Initialize database
db = FinancialDatabase()

def normalize_column_names(df):
    """Normalize column names to standard format (Capitalized)"""
    if isinstance(df.columns, pd.MultiIndex):
        # For multi-index, normalize both levels
        new_columns = []
        for col in df.columns:
            if isinstance(col, tuple):
                new_columns.append(tuple(c.capitalize() for c in col))
            else:
                new_columns.append(col.capitalize())
        df.columns = pd.MultiIndex.from_tuples(new_columns)
    else:
        # For single index
        df.columns = [col.capitalize() for col in df.columns]
    return df

def ensure_proper_dataframe(df, ticker):
    """Ensure we have a properly formatted DataFrame with required columns"""
    if df.empty:
        return pd.DataFrame()
    
    # Normalize column names first
    df = normalize_column_names(df)
    
    # Handle multi-index case
    if isinstance(df.columns, pd.MultiIndex):
        if ticker in df.columns.levels[0]:
            df = df[ticker]
        else:
            # If ticker not found, use first available
            df = df[df.columns.levels[0][0]]
    
    # Ensure we have a DataFrame (not Series)
    if isinstance(df, pd.Series):
        df = df.to_frame('Close')
    
    # Ensure we have required columns (case-insensitive check)
    required_cols_lower = ['close']
    available_cols_lower = [col.lower() for col in df.columns]
    
    if not all(req in available_cols_lower for req in required_cols_lower):
        missing = [req for req in required_cols_lower if req not in available_cols_lower]
        st.warning(f"Missing required columns {missing} for {ticker}")
        return pd.DataFrame()
    
    # Standardize column names
    col_mapping = {
        'close': 'Close',
        'open': 'Open',
        'high': 'High',
        'low': 'Low',
        'volume': 'Volume',
        'adj close': 'Adj Close'
    }
    
    df.columns = [col_mapping.get(col.lower(), col) for col in df.columns]
    
    return df

def main():
    st.set_page_config(
        page_title="Financial Market Dashboard",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("📈 Real-Time Financial Market Dashboard")
    
    # Sidebar configuration
    st.sidebar.header("Configuration")
    default_tickers = "AAPL,MSFT,GOOG,AMZN"  # Using valid default tickers
    tickers = st.sidebar.text_input("Enter tickers (comma separated)", default_tickers).upper()
    ticker_list = [t.strip() for t in tickers.split(",") if t.strip()]
    
    time_frame = st.sidebar.selectbox(
        "Select time frame",
        ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y"],
        index=5  # Default to 1y
    )
    
    # Technical indicators options
    st.sidebar.subheader("Technical Indicators")
    show_sma = st.sidebar.checkbox("Show Moving Averages", value=True)
    show_rsi = st.sidebar.checkbox("Show RSI", value=True)
    show_volatility = st.sidebar.checkbox("Show Volatility", value=True)
    show_bollinger = st.sidebar.checkbox("Show Bollinger Bands", value=True)
    
    # Fetch and process data
    st.sidebar.subheader("Data Options")
    refresh_data = st.sidebar.button("Refresh Data")
    store_data = st.sidebar.checkbox("Store data in database", value=True)
    
    if refresh_data or not st.session_state.get('data_loaded', False):
        with st.spinner("Fetching market data..."):
            historical_data = {}
            correlation_data = {}
            failed_tickers = []
            
            for ticker in ticker_list:
                try:
                    raw_data = fetch_historical_data(ticker, time_frame)
                    df = ensure_proper_dataframe(raw_data, ticker)
                    
                    if df.empty:
                        st.warning(f"No data returned for {ticker} - possibly invalid ticker")
                        failed_tickers.append(ticker)
                        continue
                    
                    # Calculate indicators based on user selection
                    if show_sma:
                        df = calculate_moving_averages(df)
                    if show_rsi:
                        df = calculate_rsi(df)
                    if show_volatility:
                        df = calculate_volatility(df)
                    if show_bollinger:
                        df = calculate_bollinger_bands(df)
                    
                    # Store in historical data
                    historical_data[ticker] = df
                    
                    # Prepare data for correlation matrix
                    correlation_data[ticker] = df['Close'].rename(ticker)
                    
                    # Store in database if enabled
                    if store_data:
                        db.store_historical_data(ticker, df)
                
                except Exception as e:
                    st.error(f"Error processing {ticker}: {str(e)}")
                    failed_tickers.append(ticker)
                    continue
            
            # Remove failed tickers
            ticker_list = [t for t in ticker_list if t not in failed_tickers]
            
            # Calculate correlations if we have multiple tickers
            if len(correlation_data) > 1:
                try:
                    correlation_matrix = calculate_correlation_matrix(correlation_data)
                    st.session_state.correlation_matrix = correlation_matrix
                except Exception as e:
                    st.error(f"Error calculating correlations: {str(e)}")
                    st.session_state.correlation_matrix = None
            else:
                st.session_state.correlation_matrix = None
            
            # Store in session state
            st.session_state.historical_data = historical_data
            st.session_state.data_loaded = True
            st.session_state.ticker_list = ticker_list
    
    # Display dashboard
    if st.session_state.get('data_loaded', False) and st.session_state.ticker_list:
        # Create tabs
        tab1, tab2, tab3 = st.tabs(["Price Charts", "Technical Indicators", "Correlation Analysis"])
        
        with tab1:
            st.header("Price Charts")
            selected_ticker = st.selectbox("Select ticker for price chart", st.session_state.ticker_list)
            
            if selected_ticker in st.session_state.historical_data:
                df = st.session_state.historical_data[selected_ticker]
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    fig = plot_price_chart(df, selected_ticker)
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    latest = df.iloc[-1]
                    st.metric("Current Price", f"${latest['Close']:.2f}")
                    
                    if 'High' in df.columns:
                        st.metric("Period High", f"${df['High'].max():.2f}")
                    if 'Low' in df.columns:
                        st.metric("Period Low", f"${df['Low'].min():.2f}")
                    if 'Volume' in df.columns:
                        st.metric("Latest Volume", f"{latest['Volume']:,.0f}")
        
        with tab2:
            st.header("Technical Indicators")
            if len(st.session_state.ticker_list) > 1:
                selected_ticker = st.selectbox("Select ticker for indicators", st.session_state.ticker_list)
            else:
                selected_ticker = st.session_state.ticker_list[0]
            
            if selected_ticker in st.session_state.historical_data:
                df = st.session_state.historical_data[selected_ticker]
                
                if show_rsi and 'RSI' in df.columns:
                    st.subheader("Relative Strength Index (RSI)")
                    st.plotly_chart(plot_rsi_chart(df), use_container_width=True)
                
                if show_volatility and 'Volatility' in df.columns:
                    st.subheader("Historical Volatility")
                    st.line_chart(df['Volatility'])
                
                if show_bollinger and all(b in df.columns for b in ['Upper Band', 'Middle Band', 'Lower Band']):
                    st.subheader("Bollinger Bands")
                    st.write("Price between upper and lower bands:")
                    bb_fig = go.Figure()
                    bb_fig.add_trace(go.Scatter(x=df.index, y=df['Upper Band'], name='Upper Band'))
                    bb_fig.add_trace(go.Scatter(x=df.index, y=df['Middle Band'], name='Middle Band'))
                    bb_fig.add_trace(go.Scatter(x=df.index, y=df['Lower Band'], name='Lower Band'))
                    st.plotly_chart(bb_fig, use_container_width=True)
        
        with tab3:
            st.header("Correlation Analysis")
            if st.session_state.correlation_matrix is not None:
                st.plotly_chart(
                    plot_correlation_heatmap(st.session_state.correlation_matrix),
                    use_container_width=True
                )
                
                st.write("Correlation values range from -1 to 1:")
                st.markdown("- **1** means perfect positive correlation")
                st.markdown("- **-1** means perfect negative correlation")
                st.markdown("- **0** means no correlation")
            else:
                st.warning("Correlation analysis requires at least 2 valid tickers")
    elif not st.session_state.get('ticker_list', []):
        st.error("No valid tickers available. Please check your ticker symbols and try again.")

if __name__ == "__main__":
    main()