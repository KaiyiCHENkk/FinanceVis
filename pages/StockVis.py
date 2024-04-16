import dash
from dash import dcc, html, callback, Input, Output, State, callback_context
import pandas as pd
import plotly.graph_objs as go
from components.buysellTrans import get_buysellTrans_layout
from data.dataManage import load_investment_data, filter_dividend_data, load_investment_dates, load_company_data,load_stock_close_data
from components.dividend import get_dividend_layout, create_monthly_dividend_figure, create_simplified_monthly_dividend_figure
from components.overview import get_overview_layout, create_stock_overview_figure
from components.single import get_single_layout, create_single_stock_figure
from components.risk import get_risk_layout, create_parallel_coordinates_figure
from components.home import get_home_layout
from dash.exceptions import PreventUpdate
import json 


dash.register_page(__name__, title="StockVis")


df =  load_investment_data()
dividend_df = filter_dividend_data(df)
start_end_date_df = load_investment_dates()
company_df = load_company_data()
stock_df = load_stock_close_data()

# Callback for dynamic page content
@callback(
    Output('page-content', 'children'),
    [Input('home', 'n_clicks'),
     Input('buysellTrans', 'n_clicks'), 
     Input('dividend', 'n_clicks'),
     Input('overview', 'n_clicks'),  # Input for View 3 button
     Input('single', 'n_clicks'),
     Input('risk', 'n_clicks')],
    prevent_initial_call=True
)
def display_view(home_btn, btn1, btn2, btn3, btn4, btn5):
    # Decide which button was clicked last
    ctx = dash.callback_context
    if not ctx.triggered:
        # Default to view 1 if no buttons have been clicked yet
        return get_buysellTrans_layout(df)
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'home':
        return get_home_layout(start_end_date_df, df, company_df, stock_df)
    elif button_id == 'dividend':
        return get_dividend_layout(dividend_df)
    elif button_id == 'overview':
        return get_overview_layout(start_end_date_df, df, company_df, stock_df)  
    elif button_id == 'single':
        return get_single_layout()
    elif button_id == 'risk':
        return get_risk_layout(company_df)
    else:
        return get_buysellTrans_layout(df)














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











# @callback(
#     Output('single-stock-graph', 'figure'),
#     [Input('single-stock-dropdown', 'value')]
# )
# def update_single_stock_graph(selected_ticker):
#     if selected_ticker:
#         return create_single_stock_figure(selected_ticker, start_end_date_df,df)
#     return go.Figure()















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

















# @callback(
#     [Output('selected-tickers-store', 'data'),  # To store selected ticker data
#      Output('selected-tickers-display', 'children')], 
#     [Input('risk-home-chart', 'relayoutData')],
#     State('risk-home-chart', 'figure'),
#     prevent_initial_call=True
# )
# def filter_tickers_based_on_adjustments(relayoutData, figure):
#     if relayoutData is None:
#         return "Adjust the filters on the parallel coordinates chart to filter tickers."

#     # Parse relayoutData to determine user-adjusted ranges
#     # Example: {'dimensions[0].constraintrange': [[100, 300]]}
#     for key, value in relayoutData.items():
#         if 'constraintrange' in key:
#             dim_index = int(key.split('[')[1].split(']')[0])  # Extract dimension index
#             constraintrange = value[0]  # Assuming a single range per dimension

#             # Filter DataFrame based on the adjusted range
#             # Identify the dimension name based on the figure layout
#             dim_name = figure['data'][0]['dimensions'][dim_index]['label']
#             filtered_df = df[(df[dim_name] >= constraintrange[0]) & (df[dim_name] <= constraintrange[1])]
#             filtered_tickers = ', '.join(filtered_df['Ticker'].unique())

#             return f"Filtered Tickers: {filtered_tickers}"

#     return "No applicable filters detected."


# @callback(
#     Output('overview-home-chart', 'figure'),
#     [Input('risk-home-chart', 'selectedData')],
#     [State('overview-home-chart', 'figure')]
# )
# def update_stock_focus(selectedData, figure):
#     print("Callback triggered", selectedData) 
#     if selectedData is None or 'points' not in selectedData:
#         raise PreventUpdate
    
#     # Extract selected points' indices; these correspond to rows in company_df
#     selected_indices = [point['pointIndex'] for point in selectedData['points']]
    
#     # Use these indices to get the corresponding tickers from company_df
#     selected_tickers = company_df.iloc[selected_indices]['Ticker'].unique()
    
#     # selected_tickers includes the corresponding tickers
#     if not selected_tickers:
#         # If no tickers are selected, don't update the figure.
#         raise PreventUpdate
    
#     # Now, update the stock overview chart based on selected tickers
#     new_fig_data = []
#     for trace in figure['data']:
#         # Check if the trace (ticker) is in the selected tickers
#         if trace.get('name') in selected_tickers:
#             trace['visible'] = True
#         else:
#             # Make other traces less visible or adjust as needed
#             trace['visible'] = 'legendonly'
#         new_fig_data.append(trace)
    
#     figure['data'] = new_fig_data
#     return figure




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
        
        # Convert existing selections from JSON if necessary
        if isinstance(existing_selections, str):
            existing_selections = json.loads(existing_selections)
        
        # Update the selections based on restyleData
        for change in restyle_data:
            if 'dimensions' in str(change):
                for key, value in change.items():
                    # Extract the dimension index
                    dim_index = int(key.split("[")[1].split("]")[0])
                    dimension_name = df_columns[dim_index]
                    # Process the constraintrange values
                    # if value:  # If there are selections
                    #     ranges = value[0] if isinstance(value[0], list) else [value[0]]
                    #     # Flatten the list if it's nested
                    #     flattened_ranges = [item for sublist in ranges for item in sublist] if any(isinstance(el, list) for el in ranges) else ranges
                    #     existing_selections[dimension_name] = flattened_ranges
                    
                    
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






# @callback(
#     Output('overview-home-chart', 'figure'),  # Adjust this to your actual output component and property
#     Input('user-selections-store', 'data'),  # Triggered when the store's data changes
#     State('overview-home-chart', 'figure')
# )
# def process_user_selections(stored_selections, current_fig):
#     if not stored_selections:
#         # If no selections are stored, do not update the chart
#         raise PreventUpdate
    
#     if stored_selections:
#         selections_dict = json.loads(stored_selections)
#         selections_df = pd.DataFrame(list(selections_dict.items()), columns=['Dimension', 'Ranges'])
        
#         valid_indices = set(company_df['Ticker'])

#         #print(selections_df)  # For demonstration; replace with your processing logic

#         for index, row in selections_df.iterrows():
#             if row['Ranges'] is not None:
#                 dimension = row['Dimension']
#                 temp_indices = set()

#                 for selected_range in row['Ranges']:
#                     condition = (company_df[dimension] >= selected_range[0]) & (company_df[dimension] <= selected_range[1])
#                     temp_indices.update(company_df[condition]['Ticker'])
                
#                 valid_indices.intersection_update(temp_indices)

#         valid_indices_list = list(valid_indices)
        
#         for trace in current_fig['data']:
#             ticker = trace.get('name')
#             group = trace.get('legendgroup')

#             if ticker and ticker in valid_indices_list:
#                 trace['visible'] = True
#         # For buy/sell markers, 'name' includes 'Buy'/'Sell'. Match their group with the ticker line trace.
#             elif group and any(ticker for ticker in valid_indices_list if group.endswith(ticker)):
#                 trace['visible'] = True
#             else:
#                 trace['visible'] = 'legendonly'


#             # if trace['name'] in valid_indices_list:
#             #     trace['visible'] = True
#             # else:
#             #     trace['visible'] = 'legendonly'

        
#         return current_fig

    

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
            
            print(selections_df)

            valid_indices = set(company_df['Ticker'])

            #print(selections_df)  # For demonstration; replace with your processing logic

            for index, row in selections_df.iterrows():
                if row['Ranges'] is not None:
                    dimension = row['Dimension']
                    temp_indices = set()

                    for selected_range in row['Ranges']:
                        condition = (company_df[dimension] >= selected_range[0]) & (company_df[dimension] <= selected_range[1])
                        temp_indices.update(company_df[condition]['Ticker'])
                    
                    valid_indices.intersection_update(temp_indices)

            valid_indices_list = list(valid_indices)
            
            #print(valid_indices_list)

            for trace in current_fig['data']:
                ticker = trace.get('name')
                group = trace.get('legendgroup')
                #print(ticker)
                if ticker and ticker in valid_indices_list:
                    trace['opacity'] = 1
                    #print(ticker)
                # For buy/sell markers associated with the selected tickers, ensure they are also fully opaque
                elif group and any(ticker for ticker in valid_indices_list if group.endswith(ticker)):
                    trace['opacity'] = 1
                    print(ticker)
                else:
                    # For non-selected tickers, reduce opacity to make them transparent but still present on the plot
                    trace['opacity'] = 0.2
                    #print(ticker+"0.2")
    elif trigger_id == 'update-ma-btn' and n_clicks > 0:

        

        show_trend_after_last_buy = 'last_buy' in trend_checkbox_values
        show_trend_after_last_sell = 'last_sell' in trend_checkbox_values
        current_fig = create_stock_overview_figure(stock_df, start_end_date_df, df, company_df, show_trend_after_last_buy, show_trend_after_last_sell, ma_period)

        
    else:
        raise PreventUpdate
    
    return current_fig





# @callback(
#     Output('selection-output', 'children'),
#     [Input('risk-home-chart', 'restyleData')]
# )
# def handle_restyle(restyleData):
#     if not restyleData:
#         return "No restyling detected. Please interact with the chart."

#     # Example processing of restyleData. This will be highly dependent on the
#     # specific restyle actions users can take in your chart and may not directly
#     # correspond to selecting or brushing data in the traditional sense.
#     restyle_info = str(restyleData)  # Placeholder for actual processing logic
#     print("Received restyleData:", restyleData)
#     return f"Restyling detected: {restyle_info}"







# def process_relayout_data(relayoutData):
#     print("Received relayoutData:", relayoutData)
#     if not relayoutData:
#         return "Adjust the filters to see results."
    
#     # Initialize a variable to hold filter criteria
#     filter_criteria = []
    
#     for key, value in relayoutData.items():
#         if 'constraintrange' in key:
#             # Extract the dimension index and the constraint range
#             dim_index = int(key.split('[')[1].split(']')[0])
#             constraintrange = value[0]  # Assuming a single range for simplicity
            
#             # Map the index to a DataFrame column name (this example directly uses index mapping for simplicity)
#             dimension_name = ['Average Price per Share', 'Current Share Price'][dim_index]
#             filter_criteria.append((dimension_name, constraintrange))
    
#     # Filter the DataFrame based on the extracted criteria
#     filtered_df = company_df
#     for dimension_name, dimension_range in filter_criteria:
#         filtered_df = filtered_df[(filtered_df[dimension_name] >= dimension_range[0]) & (filtered_df[dimension_name] <= dimension_range[1])]
    
#     # For debugging, return the filtered DataFrame as a string or any other details you find relevant
#     return f"Filtered DataFrame based on `relayoutData`: {filtered_df.to_dict('records')}"























# @callback(
#     Output('overview-home-chart', 'figure'),
#     [Input('trend_checkboxes', 'value')]
# )
# def update_overview_chart(trend_checkbox_values):

#     # Load the stock close data required for the chart
#      # Ensure this function is defined and accessible

#     # Check which checkboxes are ticked
#     show_trend_after_last_buy = 'last_buy' in trend_checkbox_values
#     show_trend_after_last_sell = 'last_sell' in trend_checkbox_values

#     # Generate the figure with updated parameters based on checkbox selection
#     updated_figure = create_stock_overview_figure(stock_df, start_end_date_df, df, company_df, show_trend_after_last_buy, show_trend_after_last_sell)

#     return updated_figure




layout = html.Div([
    html.Div([
        html.Button('Home', id='home'), 
        html.Button('Buy/Sell', id='buysellTrans'),
        html.Button('Dividend', id='dividend'),
        html.Button('Overview', id='overview'), 
        html.Button('Single', id='single'),
        html.Button('Risk Factors', id='risk'),
    ]),
    html.Div(id='page-content', children=get_buysellTrans_layout(df))  
])

