import dash
from dash import dcc, html
from components.multiple import create_stock_overview_figure
from components.company import create_parallel_coordinates_figure
from components.gainLoss import create_gain_loss_chart
from components.buySell import create_buysell_volume
from components.dividend import create_dividend_figure,create_simplified_monthly_dividend_figure


def get_home_layout(investment_dates,df, company_data,stock_df, dividend_df):
    """
    Generates the home layout for the dashboard with multiple graph visualizations.

    Parameters:
        investment_dates (DataFrame): Data about investment dates.
        df (DataFrame): Investment transaction data frame used across various components.
        company_data (DataFrame): Data specific to companies (company metadata).
        stock_df (DataFrame): Stock-related data from API.
        dividend_df (DataFrame): Dividend-related data.

    Returns:
        html.Div: A Dash HTML component that includes all elements of the home layout.
    """

    stock_overview_fig = create_stock_overview_figure(stock_df, investment_dates,df, company_data)
    parallel_coordinates_fig = create_parallel_coordinates_figure(company_data)
    gain_loss_fig = create_gain_loss_chart(company_data)
    buy_sell_fig = create_buysell_volume(df)
    dividend_ticker_fig = create_dividend_figure(dividend_df)
    dividend_time_fig = create_simplified_monthly_dividend_figure(dividend_df)

    layout = html.Div([

        html.Div([  # Container for graphs
            html.Div([  # Sub-container for the left two graph
                
                html.Div([
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
                ], style={'padding': '10px'}),
                dcc.Graph(id='overview-home-chart', figure=stock_overview_fig),
                dcc.Graph(id='risk-home-chart', figure=parallel_coordinates_fig)
            ], style={'display': 'inline-block', 'width': '50%'}),

            html.Div([  # Sub-container for the Gain/Loss chart
                html.Div(style={'height': '200px'}),
                dcc.Graph(id='gain-loss-chart', figure=gain_loss_fig)
            ], style={'display': 'inline-block', 'width': '19%'}),

            html.Div([  # Sub-container for Dividend and Buy/Sell charts
                html.Div(style={'height': '220px'}),
                dcc.Graph(id='buy_sell_fig-home', figure=buy_sell_fig),
                dcc.Graph(id='divi-time-home', figure=dividend_time_fig),
                dcc.Graph(id='divi-ticker-home', figure=dividend_ticker_fig)
            ], style={'display': 'inline-block', 'width': '31%'}),
        ], style={'display': 'flex'}),

        dcc.Store(id='user-selections-store')
    ])
    return layout