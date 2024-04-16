import dash
from dash import dcc, html
import plotly.graph_objs as go
from data.dataManage import load_stock_close_data, load_investment_dates
import pandas as pd
import plotly.express as px

def create_stock_overview_figure(stock_df, investment_dates, investment_data, company_data, show_trend_after_last_buy=False, show_trend_after_last_sell=False, ma_period=10):
    stock_df.index = pd.to_datetime(stock_df.index, format='%d/%m/%Y')  
    extended_date = pd.to_datetime('11/03/2024')

    tickers = company_data['Ticker'].unique()
    # Use a continuous color scale from Plotly Express
    continuous_color_scale = px.colors.sequential.Plasma

    # Calculate equally spaced intervals for each ticker on the color scale
    n_tickers = len(tickers)
    interval = 1 / max(n_tickers - 1, 1)

    # Create a color map for each ticker based on its position in the dataset
    ticker_color_map = {
        ticker: px.colors.sample_colorscale(continuous_color_scale, i * interval)[0]
        for i, ticker in enumerate(tickers)
    }

    
    fig = go.Figure()
    for _, row in investment_dates.iterrows():
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

            
            #fig.add_trace(go.Scatter(x=filtered_df.index, y=filtered_df, mode='lines', name=ticker, line=dict(color=ticker_color_map[ticker]), legendgroup=legendgroup))

            # Filter buy and sell dates for the current ticker
            transactions = investment_data[(investment_data['Ticker'] == ticker) & 
                                           (investment_data['Action'].str.contains('buy|sell', case=False))]

            buy_dates = transactions[transactions['Action'].str.contains('buy', case=False)]['Transaction Date']
            sell_dates = transactions[transactions['Action'].str.contains('sell', case=False)]['Transaction Date']

            for date in buy_dates:
                fig.add_trace(go.Scatter(x=[date, date], y=[stock_df.loc[date, ticker], stock_df.loc[date, ticker]],
                                         mode='markers', name=f'{ticker} Buy', marker_symbol='triangle-up',
                                         marker_color='green', marker_size=7, showlegend=False, legendgroup=legendgroup))

            for date in sell_dates:
                fig.add_trace(go.Scatter(x=[date, date], y=[stock_df.loc[date, ticker], stock_df.loc[date, ticker]],
                                         mode='markers', name=f'{ticker} Sell', marker_symbol='triangle-down',
                                         marker_color='red', marker_size=7, showlegend=False, legendgroup=legendgroup))

    fig.update_layout(
        title='Customised Stock Overview',
        xaxis_title='Date',
        yaxis_title='Close Price',
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
    #stock_df = load_stock_close_data()
    stock_overview_fig = create_stock_overview_figure(stock_df, investment_dates,df, company_data)
    
    layout = html.Div([
        html.H2('Stock Prices Overview'),
        dcc.Graph(id='stock-overview-chart', figure=stock_overview_fig)
    ])
    return layout
