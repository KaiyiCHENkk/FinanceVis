import dash
from dash import dcc, html
import plotly.graph_objs as go
from data.dataManage import load_stock_close_data, load_investment_dates
import pandas as pd
import plotly.express as px
from components.overview import create_stock_overview_figure
from components.risk import create_parallel_coordinates_figure




def get_home_layout(investment_dates,df, company_data,stock_df):
    #stock_df = load_stock_close_data()
    stock_overview_fig = create_stock_overview_figure(stock_df, investment_dates,df, company_data)
    parallel_coordinates_fig = create_parallel_coordinates_figure(company_data)
    layout = html.Div([
        
        dcc.Checklist(
            id='trend_checkboxes',
            options=[
                {'label': ' Show trend after the last buy', 'value': 'last_buy'},
                {'label': ' Show trend after the last sell', 'value': 'last_sell'}
            ],
            value=[]  # By default, no checkboxes are ticked
        ),
        dcc.Input(id='ma-period-input', type='number', value=10, min=1, style={'marginRight':'10px'}),
        html.Button('Update Moving Average', id='update-ma-btn', n_clicks=0),
        dcc.Graph(id='overview-home-chart', figure=stock_overview_fig),  # Placeholder for the Stock Overview chart
        dcc.Graph(id='risk-home-chart',figure=parallel_coordinates_fig),
        
        #html.Div(id='selection-output')
        # dcc.Store(id='selected-tickers-store'),
        # html.Div(id='selected-tickers-display'),
        dcc.Store(id='user-selections-store')
        #html.Div(id='some-output')
    ])
    return layout