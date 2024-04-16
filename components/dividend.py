import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objs as go
from data.dataManage import aggregate_dividend_data, aggregate_dividend_data_by_month



def create_dividend_figure(dividend_df):
    aggregated_dividend_data = aggregate_dividend_data(dividend_df)
    fig = go.Figure()
    for dividend_type in aggregated_dividend_data.columns:
        fig.add_trace(go.Bar(
            x=aggregated_dividend_data.index,
            y=aggregated_dividend_data[dividend_type],
            name=dividend_type
        ))
    fig.update_layout(barmode='stack', title_text='Dividend Actions by Ticker')
    return fig


def create_monthly_dividend_figure(dividend_df):
    monthly_dividend_data = aggregate_dividend_data_by_month(dividend_df)
    fig = go.Figure()
    tickers = monthly_dividend_data['Ticker'].unique()
    for ticker in tickers:
        df_filtered = monthly_dividend_data[monthly_dividend_data['Ticker'] == ticker]
        for action in df_filtered['Action'].unique():
            df_action = df_filtered[df_filtered['Action'] == action]
            fig.add_trace(go.Bar(
                x=df_action['Month_Year'],
                y=df_action['Total (GBP)'],
                name=f'{ticker} - {action}'
            ))
    fig.update_layout(
        barmode='stack',
        title_text='Monthly Dividends by Ticker and Type',
        xaxis_title='Month',
        yaxis_title='Total GBP',
        xaxis={'categoryorder':'category ascending'}
    )
    return fig




def create_simplified_monthly_dividend_figure(dividend_df):
    monthly_dividend_data = aggregate_dividend_data_by_month(dividend_df)
    grouped_df = monthly_dividend_data.groupby(['Month_Year', 'Ticker'])['Total (GBP)'].sum().reset_index()
    fig = go.Figure()
    tickers = grouped_df['Ticker'].unique()
    for ticker in tickers:
        ticker_df = grouped_df[grouped_df['Ticker'] == ticker]
        fig.add_trace(go.Bar(
            x=ticker_df['Month_Year'],
            y=ticker_df['Total (GBP)'],
            name=ticker  
        ))
    
    fig.update_layout(
        barmode='stack',  
        title_text='Monthly Dividends by Ticker',
        xaxis_title='Month',
        yaxis_title='Total GBP',
        xaxis={'categoryorder':'category ascending'},
        legend_title='Ticker'
    )
    return fig





 



def get_dividend_layout(dividend_df):
    dividend_fig = create_dividend_figure(dividend_df)
    simplified_fig = create_simplified_monthly_dividend_figure(dividend_df)
    layout = html.Div([
        html.H2('Dividend Actions by Ticker and Type'),
        dcc.Graph(id='dividend-actions-chart', figure=dividend_fig),
        html.Button('Toggle View', id='dividend-detail-view', n_clicks=0),
        html.Div(id='toggle-simplified-view', children=[dcc.Graph(figure=simplified_fig)]),
    ])
    return layout






