from dash import dcc, html
import plotly.graph_objs as go
from data.dataManage import load_ticker_stock_data, get_all_tickers, load_stock_close_single
import pandas as pd


def create_single_stock_figure(ticker, investment_dates, investment_data, ma_periods =[], chart_style='line'):
    """
    Creates a stock figure for a single ticker with specified chart style and moving averages.

    Parameters:
        ticker (str): The stock ticker.
        investment_dates (DataFrame): DataFrame containing start and end dates for each ticker.
        investment_data (DataFrame): DataFrame containing transaction data.
        ma_periods (list, optional): List of integers representing moving average periods.
        chart_style (str, optional): The style of the chart ('line', 'candle', 'ohlc', 'area').

    Returns:
        go.Figure: Plotly graph object figure containing the stock chart with transactions and moving averages.
    """
    df = load_ticker_stock_data(ticker)
    dfclose = load_stock_close_single()
    
    # Find the start and end dates for the ticker
    start_date, end_date = investment_dates[investment_dates['Ticker'] == ticker][['Start Date', 'End Date']].iloc[0]

    # Filter the stock data and investment data based on the dates
    df_filtered = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    df_filtered_close = dfclose[(dfclose['Date'] >= start_date) & (dfclose['Date'] <= end_date)]
    transactions = investment_data[(investment_data['Ticker'] == ticker) & (investment_data['Action'].str.contains('buy|sell', case=False))]

    fig = go.Figure()

    if chart_style == 'line':
    # Add the main stock line
        fig.add_trace(go.Scatter(x=df_filtered_close['Date'], y=df_filtered_close[ticker], mode='lines', name=ticker))

    elif chart_style == 'candle':
        fig.add_trace(go.Candlestick(x=df_filtered['Date'],
                                     open=df_filtered['Open'], high=df_filtered['High'],
                                     low=df_filtered['Low'], close=df_filtered['Close'],
                                     name=ticker))
    elif chart_style == 'ohlc':
        fig.add_trace(go.Ohlc(x=df_filtered['Date'],
                              open=df_filtered['Open'], high=df_filtered['High'],
                              low=df_filtered['Low'], close=df_filtered['Close'],
                              name=ticker))
    elif chart_style == 'area':
        fig.add_trace(go.Scatter(x=df_filtered['Date'], y=df_filtered['Close'], fill='tozeroy', name=ticker))
    
    # Add buy and sell points
    for _, transaction in transactions.iterrows():
        date_time = pd.to_datetime(f"{transaction['Transaction Date']} {transaction['Time']}")
        price = transaction['Price / share']
        action = 'Buy' if 'buy' in transaction['Action'].lower() else 'Sell'
        color = 'green' if action == 'Buy' else 'red'
        fig.add_trace(go.Scatter(x=[date_time], y=[price], mode='markers', name=f'{action}',
                                 marker=dict(color=color, size=10, symbol='circle'), showlegend=False))
    
    for period in ma_periods:
        ma = calculate_moving_average(ticker, df_filtered_close, period)
        fig.add_trace(go.Scatter(x=df_filtered_close['Date'], y=ma, mode='lines', name=f'MA {period} days'))
    
    fig.update_layout(title=f'{ticker} Stock Data with Transactions', xaxis_title='Date', yaxis_title='Price',
                      xaxis=dict(
                        rangeselector=dict(
                            buttons=list([
                                dict(count=1, label="1m", step="month", stepmode="backward"),
                                dict(count=6, label="6m", step="month", stepmode="backward"),
                                dict(count=1, label="1y", step="year", stepmode="backward"),
                                dict(step="all")
                            ])
                        ),
                        rangeslider=dict(
                            visible=True
                        ),
                        type="date"
                    ),)

    return fig


def calculate_moving_average(ticker, df, period):
    """
    Calculates the moving average for the given period.

    Parameters:
        ticker (str): The stock ticker for which the moving average is calculated.
        df (DataFrame): DataFrame containing close price data.
        period (int): The number of days over which to calculate the moving average.

    Returns:
        Series: A pandas Series representing the moving average.
    """
    return df[ticker].rolling(window=period, min_periods=1).mean()


def get_single_layout():
    """
    Generates the layout for the single stock analysis page with options for chart style and moving average.

    Returns:
        html.Div: A Dash HTML component containing the layout for single stock analysis.
    """
    tickers = get_all_tickers()
    chart_styles = ['line', 'candle', 'area', 'ohlc']
    ma_controls = html.Div([
        dcc.Input(id='ma-input', type='number', placeholder='Enter MA period', style={'marginRight': '10px'}),
        html.Button('Add Moving Average', id='add-ma', n_clicks=0),
        dcc.Store(id='ma-periods')  # Store for holding MA periods
    ])
    return html.Div([
        dcc.Dropdown(
            id='single-stock-dropdown',
            options=[{'label': ticker, 'value': ticker} for ticker in tickers],
            placeholder="Select a ticker",
        ),
        dcc.Dropdown(  # Chart style selector
            id='chart-style-dropdown',
            options=[{'label': style.capitalize(), 'value': style} for style in chart_styles],
            value='line',  # Default value is 'line'
            placeholder="Select chart style",
        ),
        dcc.Graph(id='single-stock-graph'),
        ma_controls
    ])



