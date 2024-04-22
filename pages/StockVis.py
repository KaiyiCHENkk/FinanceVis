import dash
from dash import dcc, html, callback, Input, Output, State, callback_context
import pandas as pd
import plotly.graph_objs as go
from components.buySell import get_buysellTrans_layout
from data.dataManage import load_investment_data, filter_dividend_data, load_investment_dates, load_company_data,load_stock_close_data
from components.dividend import get_dividend_layout, create_monthly_dividend_figure, create_simplified_monthly_dividend_figure
from components.multiple import get_overview_layout, create_stock_overview_figure
from components.single import get_single_layout, create_single_stock_figure
from components.company import get_risk_layout, create_parallel_coordinates_figure
from components.home import get_home_layout
from components.gainLoss import get_gainLoss_layout,create_gain_loss_chart
from dash.exceptions import PreventUpdate
import json 

# Register the page within the Dash application.
dash.register_page(__name__, title="StockVis", path='/')

df =  load_investment_data()
dividend_df = filter_dividend_data(df)
start_end_date_df = load_investment_dates()
company_df = load_company_data()
stock_df = load_stock_close_data()

@callback(
    Output('page-content', 'children'),
    [Input('home', 'n_clicks'),
     Input('buysellTrans', 'n_clicks'), 
     Input('dividend', 'n_clicks'),
     Input('overview', 'n_clicks'),  
     Input('single', 'n_clicks'),
     Input('gainLoss', 'n_clicks'),
     Input('risk', 'n_clicks')],
    prevent_initial_call=True
)
def display_view(home_btn, btn1, btn2, btn3, btn4, btn5, btn6):
    """
    Updates the content displayed on the page based on user interactions with navigation buttons.

    Parameters:
        home_btn, btn1, btn2, btn3, btn4, btn5, btn6 (int): Button click counts for different views.

    Returns:
        html.Div: The layout corresponding to the most recently clicked button.
    """    
    
    # Decide which button was clicked last
    ctx = dash.callback_context
    if not ctx.triggered:
        # Default to view 1 if no buttons have been clicked yet
        return get_home_layout(start_end_date_df, df, company_df, stock_df, dividend_df)
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'home':
        return get_home_layout(start_end_date_df, df, company_df, stock_df, dividend_df)
    elif button_id == 'dividend':
        return get_dividend_layout(dividend_df)
    elif button_id == 'overview':
        return get_overview_layout(start_end_date_df, df, company_df, stock_df)  
    elif button_id == 'single':
        return get_single_layout()
    elif button_id == 'risk':
        return get_risk_layout(company_df)
    elif button_id == 'buysellTrans':
        return get_buysellTrans_layout(df)
    elif button_id == 'gainLoss':
        return get_gainLoss_layout(company_df)
    else:
        return get_home_layout(start_end_date_df, df, company_df, stock_df, dividend_df)



# callback for dividend view, switch from simplefied and detail dividend view
@callback(
    Output('toggle-simplified-view', 'children'),
    [Input('dividend-detail-view', 'n_clicks')],
    prevent_initial_call=True
)
def toggle_dividend_view(n_clicks):
    # Determine if we should show the simplified or detailed view based on the number of clicks
    if n_clicks % 2 == 0:
        # Show detailed view
        figure = create_simplified_monthly_dividend_figure(dividend_df)
    else:
        # Show simplified view
        figure = create_monthly_dividend_figure(dividend_df)
    return [dcc.Graph(figure=figure)]



@callback(
    Output('ma-periods', 'data'),
    Input('add-ma', 'n_clicks'),
    State('ma-input', 'value'),
    State('ma-periods', 'data')
)
def update_ma_periods(n_clicks, new_period, existing_periods):
    if n_clicks > 0 and new_period is not None:
        existing_periods = existing_periods or []
        if new_period not in existing_periods:
            existing_periods.append(new_period)
            return existing_periods
    return existing_periods


@callback(
    Output('single-stock-graph', 'figure'),
    [Input('single-stock-dropdown', 'value'),
     Input('chart-style-dropdown', 'value'),
     Input('ma-periods', 'data')]
)
def update_graph_with_chart_style_and_ma(selected_ticker, chart_style, ma_periods):
    if selected_ticker:
        ma_periods = ma_periods or []
        return create_single_stock_figure(selected_ticker, start_end_date_df, df, ma_periods, chart_style)
    return go.Figure()


df_columns = ['Ticker Index', 'Average Price per Share', 'Total Purchase Amount', 
              'Total Number of Shares Purchased', 'Total Number of Shares Sold', 
              'Total Sales Amount', 'Average Sale Price per Share', 
              'Net Total Number of Shares', 'Current Share Price', 
              'Total Dividends', 'Realized Capital Gain & Loss', 
              'Unrealized Capital Gain & Loss']

@callback(
    Output('user-selections-store', 'data'),
    [Input('risk-home-chart', 'restyleData')],
    State('user-selections-store', 'data')
)
def update_user_selections(restyle_data, existing_selections):
    if restyle_data:
        # Initialize a new selections dict if none exists
        if not existing_selections:
            existing_selections = {col: None for col in df_columns}
        # Convert existing selections from JSON 
        if isinstance(existing_selections, str):
            existing_selections = json.loads(existing_selections)
        # Update the selections based on restyleData
        for change in restyle_data:
            if 'dimensions' in str(change):
                for key, value in change.items():
                    # Extract the dimension index
                    dim_index = int(key.split("[")[1].split("]")[0])
                    dimension_name = df_columns[dim_index]                    
                    if value:  # If there are selections
                        if not isinstance(value[0][0], list):
                            existing_selections[dimension_name] = [value[0]]  # Wrap single range in list of lists
                        else:
                            existing_selections[dimension_name] = value[0] 
                    else:  # If the selection is cleared
                        existing_selections[dimension_name] = None
        # Convert updated selections back to JSON for storage
        return json.dumps(existing_selections)
    return existing_selections if existing_selections else json.dumps({col: None for col in df_columns})
    

@callback(
    Output('overview-home-chart', 'figure'),
    [Input('update-ma-btn', 'n_clicks'),Input('trend_checkboxes', 'value'),Input('user-selections-store', 'data')],
    [State('trend_checkboxes', 'value'),State('user-selections-store', 'data'),State('ma-period-input', 'value'),State('overview-home-chart', 'figure')]
)
def update_overview_chart(n_clicks,trend_checkbox_values, stored_selections, trend_checkboxes_states,stored_selections_state, ma_period, current_fig):
    ctx = callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if trigger_id == 'trend_checkboxes':
        show_trend_after_last_buy = 'last_buy' in trend_checkbox_values
        show_trend_after_last_sell = 'last_sell' in trend_checkbox_values

    # Generate the figure with updated parameters based on checkbox selection
        current_fig = create_stock_overview_figure(stock_df, start_end_date_df, df, company_df, show_trend_after_last_buy, show_trend_after_last_sell, ma_period)
        
    elif trigger_id == 'user-selections-store':
    
        if not stored_selections:
            # If no selections are stored, do not update the chart
            raise PreventUpdate
        
        if stored_selections:
            selections_dict = json.loads(stored_selections)
            selections_df = pd.DataFrame(list(selections_dict.items()), columns=['Dimension', 'Ranges'])

            valid_indices = set(company_df['Ticker'])

            for index, row in selections_df.iterrows():
                if row['Ranges'] is not None:
                    dimension = row['Dimension']
                    temp_indices = set()

                    for selected_range in row['Ranges']:
                        condition = (company_df[dimension] >= selected_range[0]) & (company_df[dimension] <= selected_range[1])
                        temp_indices.update(company_df[condition]['Ticker'])
                    
                    valid_indices.intersection_update(temp_indices)

            valid_indices_list = list(valid_indices)

            for trace in current_fig['data']:
                ticker = trace.get('name')
                group = trace.get('legendgroup')
                if ticker and ticker in valid_indices_list:
                    trace['opacity'] = 1
                # For buy/sell markers associated with the selected tickers, ensure they are also fully opaque
                elif group and any(ticker for ticker in valid_indices_list if group.endswith(ticker)):
                    trace['opacity'] = 1
                else:
                    # For non-selected tickers, reduce opacity to make them transparent but still present on the plot
                    trace['opacity'] = 0.15
    elif trigger_id == 'update-ma-btn' and n_clicks > 0:

        show_trend_after_last_buy = 'last_buy' in trend_checkbox_values
        show_trend_after_last_sell = 'last_sell' in trend_checkbox_values
        current_fig = create_stock_overview_figure(stock_df, start_end_date_df, df, company_df, show_trend_after_last_buy, show_trend_after_last_sell, ma_period)
        
    else:
        raise PreventUpdate
    
    return current_fig


@callback(
    Output('gain-loss-chart', 'figure'),
    [Input('gain-loss-chart', 'restyleData')],
    [State('gain-loss-chart', 'figure')]
)
def update_chart(restyle_data, existing_figure):
    ctx = dash.callback_context
    if not ctx.triggered or not restyle_data:
        sort_column = 'Total'
    else:
        visible_traces = restyle_data[0]['visible']
        if visible_traces[0] is True:
            sort_column = 'Total Dividends'
        else:
            sort_column = 'Realized Capital Gain & Loss'

    fig = create_gain_loss_chart(company_df,sort_column)

    return fig


layout = html.Div([
    html.Div([
        html.Button('Home', id='home'), 
        html.Button('Buy/Sell', id='buysellTrans'),
        html.Button('Gain/Loss', id='gainLoss'),
        html.Button('Dividend', id='dividend'),
        html.Button('Company', id='risk'),
        html.Button('Multiple', id='overview'), 
        html.Button('Single', id='single'),
    ]),
    html.Div(id='page-content', children=get_home_layout(start_end_date_df, df, company_df, stock_df, dividend_df))  
])

