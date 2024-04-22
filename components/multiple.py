import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
 
def create_stock_overview_figure(stock_df, investment_dates, investment_data, company_data, show_trend_after_last_buy=False, show_trend_after_last_sell=False, ma_period=10):
    """
    Creates a stock overview figure with options to extend trend lines and display transactions.

    Parameters:
        stock_df (DataFrame): DataFrame containing stock data.
        investment_dates (DataFrame): DataFrame with the start and end dates for each stock.
        investment_data (DataFrame): DataFrame with investment transaction data.
        company_data (DataFrame): DataFrame with company data.
        show_trend_after_last_buy (bool, optional): Whether to extend the trend line after the last buy action.
        show_trend_after_last_sell (bool, optional): Whether to extend the trend line after the last sell action.
        ma_period (int, optional): The period over which to calculate the moving average.

    Returns:
        go.Figure: A Plotly graph object figure containing the stock overview chart.
    """
    stock_df.index = pd.to_datetime(stock_df.index, format='%d/%m/%Y')  
    extended_date = pd.to_datetime('11/03/2024')

    tickers = company_data['Ticker'].unique()

    continuous_color_scale = px.colors.sequential.Plasma

    # Calculate equally spaced intervals for each ticker on the color scale
    n_tickers = len(tickers)
    interval = 1 / max(n_tickers - 1, 1)

    sorted_tickers = sorted(tickers, key=lambda x: company_data[company_data['Ticker'] == x].index[0], reverse=True)

    # Create a color map for each ticker 
    ticker_color_map = {
        ticker: px.colors.sample_colorscale(continuous_color_scale, i * interval)[0]
        for i, ticker in enumerate(tickers)
    }
    
    fig = go.Figure()
    for ticker in sorted_tickers:
        investment_rows = investment_dates[investment_dates['Ticker'] == ticker]
        for _, row in investment_rows.iterrows():
            ticker = row['Ticker']
            start_date = pd.to_datetime(row['Start Date'], format='%d/%m/%Y')
            end_date = pd.to_datetime(row['End Date'], format='%d/%m/%Y')
            last_action = row.get('Last Action', None)
            
            if (show_trend_after_last_buy and last_action == 'Buy') or (show_trend_after_last_sell and last_action == 'Sell'):
                end_date = extended_date

            if ticker in stock_df.columns:
                filtered_df = stock_df.loc[start_date:end_date, ticker]
                
                ma = filtered_df.rolling(window=ma_period, min_periods=1).mean()

                legendgroup = f"group_{ticker}"
                
                fig.add_trace(go.Scatter(x=ma.index, y=ma, mode='lines', name=f'{ticker}', line=dict(color=ticker_color_map[ticker]), legendgroup=legendgroup))

                buy_transactions = investment_data[(investment_data['Ticker'] == ticker) & (investment_data['Action'].str.contains('buy', case=False))]
            sell_transactions = investment_data[(investment_data['Ticker'] == ticker) & (investment_data['Action'].str.contains('sell', case=False))]

            # Plot buy and sell markers with transaction price in the investment transaction dataset
            for _, buy in buy_transactions.iterrows():
                fig.add_trace(go.Scatter(
                    x=[buy['Transaction Date']], y=[buy['Price / share']],
                    mode='markers', name=f'{ticker} Buy', marker_symbol='triangle-up',
                    marker_color='green', marker_size=7, showlegend=False, legendgroup=legendgroup
                ))

            for _, sell in sell_transactions.iterrows():
                fig.add_trace(go.Scatter(
                    x=[sell['Transaction Date']], y=[sell['Price / share']],
                    mode='markers', name=f'{ticker} Sell', marker_symbol='triangle-down',
                    marker_color='red', marker_size=7, showlegend=False, legendgroup=legendgroup
                ))

    fig.update_layout(
        title='Stock Investment Overview',
        xaxis_title='Date',
        yaxis_title='Price',
        height=800,
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )
    )
    return fig


def get_overview_layout(investment_dates, df, company_data, stock_df):
    """
    Generates the layout for the Stock Prices Overview view.

    Parameters:
        investment_dates (DataFrame): DataFrame with the start and end dates for each stock.
        df (DataFrame): DataFrame containing transaction data.
        company_data (DataFrame): DataFrame with company data.
        stock_df (DataFrame): DataFrame containing stock data.

    Returns:
        html.Div: A Dash HTML component containing the layout for the stock overview.
    """
    stock_overview_fig = create_stock_overview_figure(stock_df, investment_dates,df, company_data)
    
    layout = html.Div([
        html.H2('Stock Prices Overview'),
        dcc.Graph(id='stock-overview-chart', figure=stock_overview_fig)
    ])
    return layout

