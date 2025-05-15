import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def plot_price_chart(df, ticker):
    """
    Create interactive price chart with moving averages
    """
    fig = go.Figure()
    
    # Candlestick chart
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='Price'
    ))
    
    # Add moving averages if they exist
    for col in df.columns:
        if col.startswith('SMA_'):
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df[col],
                name=col,
                line=dict(width=1)
            ))
    
    # Add Bollinger Bands if they exist
    if 'Upper Band' in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['Upper Band'],
            name='Upper Band',
            line=dict(color='rgba(200, 200, 200, 0.5)')
        ))
        
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['Lower Band'],
            name='Lower Band',
            line=dict(color='rgba(200, 200, 200, 0.5)')
        ))
    
    fig.update_layout(
        title=f'{ticker} Price Chart',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False
    )
    
    return fig

def plot_rsi_chart(df):
    """
    Create RSI chart
    """
    if 'RSI' not in df.columns:
        return None
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['RSI'],
        name='RSI',
        line=dict(color='blue', width=2)
    ))
    
    # Add overbought/oversold lines
    fig.add_hline(y=70, line_dash="dash", line_color="red")
    fig.add_hline(y=30, line_dash="dash", line_color="green")
    
    fig.update_layout(
        title='Relative Strength Index (RSI)',
        xaxis_title='Date',
        yaxis_title='RSI',
        yaxis_range=[0, 100]
    )
    
    return fig

def plot_correlation_heatmap(correlation_matrix):
    """
    Create correlation heatmap
    """
    fig = px.imshow(
        correlation_matrix,
        text_auto=True,
        color_continuous_scale='RdBu',
        zmin=-1,
        zmax=1
    )
    
    fig.update_layout(
        title='Asset Correlation Matrix',
        xaxis_title='Ticker',
        yaxis_title='Ticker'
    )
    
    return fig