import dash
from dash import dcc, html, callback, Input, Output, State
import pandas as pd
import plotly.graph_objs as go

dash.register_page(__name__)

df = pd.read_csv('Investment Transaction.csv')

df['Transaction Date'] = pd.to_datetime(df['Transaction Date'], dayfirst=True)
df['Month_Year'] = df['Transaction Date'].dt.strftime('%Y-%m')

def filter_data(account_number, transaction_type):
    action = 'Market buy' if transaction_type == 'buy' else 'Market sell'
    return df[(df['Account Number'] == account_number) & (df['Action'].str.contains(action))]

def aggregate_data(filtered_df):
    return filtered_df.groupby('Month_Year')['No. of shares'].sum()

inv_buys = aggregate_data(filter_data(2052131, 'buy'))
inv_sells = aggregate_data(filter_data(2052131, 'sell'))  
isa_buys = aggregate_data(filter_data(2052129, 'buy'))
isa_sells = aggregate_data(filter_data(2052129, 'sell'))  


all_months = sorted(set(inv_buys.index) | set(inv_sells.index) | set(isa_buys.index) | set(isa_sells.index))
inv_buys = inv_buys.reindex(all_months, fill_value=0)
inv_sells = inv_sells.reindex(all_months, fill_value=0)
isa_buys = isa_buys.reindex(all_months, fill_value=0)
isa_sells = isa_sells.reindex(all_months, fill_value=0)

fig = go.Figure()

# Buys
fig.add_trace(go.Bar(x=all_months, y=inv_buys, name='INV Buys', offsetgroup=0))
fig.add_trace(go.Bar(x=all_months, y=isa_buys, name='ISA Buys', offsetgroup=0, base=inv_buys))

# Sells
fig.add_trace(go.Bar(x=all_months, y=-inv_sells, name='INV Sells', offsetgroup=1))
fig.add_trace(go.Bar(x=all_months, y=-isa_sells, name='ISA Sells', offsetgroup=1, base=-inv_sells))

fig.update_layout(
    barmode='relative',
    title_text='Monthly Buy and Sell Transactions',
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
    )
)

def filter_dividend_data():
    dividend_types = [
        "Dividend (Ordinary)",
        "Dividend (Return of capital non us)",
        "Dividend (Demerger)",
        "Dividend (Bonus)",
        "Dividend (Ordinary manufactured payment)",
        "Dividend (Dividends paid by us corporations)",
        "Dividend (Dividends paid by foreign corporations)"
    ]
    # Assuming 'Action' column contains the dividend types information
    return df[df['Action'].isin(dividend_types)]

def aggregate_dividend_data(filtered_df):
    # Sum up 'Total (GBP)' for each 'Ticker' and 'Type of Dividend'
    aggregated_df = filtered_df.groupby(['Ticker', 'Action'])['Total (GBP)'].sum().unstack().fillna(0)
    return aggregated_df

dividend_df = filter_dividend_data()
aggregated_dividend_data = aggregate_dividend_data(dividend_df)

def create_simplified_monthly_dividend_figure(aggregated_df):
    grouped_df = aggregated_df.groupby(['Month_Year', 'Ticker'])['Total (GBP)'].sum().reset_index()
    fig = go.Figure()
    tickers = grouped_df['Ticker'].unique()
    for ticker in tickers:
        ticker_df = grouped_df[grouped_df['Ticker'] == ticker]
        fig.add_trace(go.Bar(
            x=ticker_df['Month_Year'],
            y=ticker_df['Total (GBP)'],
            name=ticker  # Use the ticker as the legend name
        ))
    
    fig.update_layout(
        barmode='stack',  # Enable stacking
        title_text='Monthly Dividends by Ticker',
        xaxis_title='Month',
        yaxis_title='Total GBP',
        xaxis={'categoryorder':'category ascending'},
        legend_title='Ticker'
    )
    return fig

def create_dividend_figure(aggregated_df):
    fig = go.Figure()
    for dividend_type in aggregated_df.columns:
        fig.add_trace(go.Bar(
            x=aggregated_df.index,
            y=aggregated_df[dividend_type],
            name=dividend_type
        ))
    fig.update_layout(barmode='stack', title_text='Dividend Actions by Ticker')
    return fig

def aggregate_dividend_data_by_month(filtered_df):
    return filtered_df.groupby(['Month_Year', 'Ticker', 'Action'])['Total (GBP)'].sum().reset_index()

def create_monthly_dividend_figure(aggregated_df):
    fig = go.Figure()
    tickers = aggregated_df['Ticker'].unique()
    for ticker in tickers:
        df_filtered = aggregated_df[aggregated_df['Ticker'] == ticker]
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

dividend_fig = create_dividend_figure(aggregated_dividend_data)

monthly_dividend_data = aggregate_dividend_data_by_month(dividend_df)
monthly_dividend_fig = create_monthly_dividend_figure(monthly_dividend_data)
simplified_monthly_dividend_fig = create_simplified_monthly_dividend_figure(monthly_dividend_data)










# Callback for dynamic page content
@callback(
    Output('page-content', 'children'),
    [Input('btn-view1', 'n_clicks'), 
     Input('btn-view2', 'n_clicks'),
     Input('btn-view3', 'n_clicks'),  # Input for View 3 button
     Input('btn-view4', 'n_clicks')],
    prevent_initial_call=True
)
def display_view(btn1, btn2, btn3, btn4):
    # Decide which button was clicked last
    ctx = dash.callback_context
    if not ctx.triggered:
        # Default to view 1 if no buttons have been clicked yet
        return get_view_1_layout()
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'btn-view2':
        return get_view_2_layout()
    elif button_id == 'btn-view3':
        return get_view_3_layout()  # Layout for View 3
    elif button_id == 'btn-view4':
        return get_view_4_layout()
    else:
        return get_view_1_layout()

def get_view_1_layout():
    return html.Div([
        html.H1('Investment Transactions: Buys and Sells'),
        dcc.Graph(figure=fig),  # Assuming 'fig' is defined elsewhere as your detailed chart
    ])

def get_view_2_layout():
    return html.Div([
        html.H2('Dividend Actions by Ticker and Type'),
        dcc.Graph(id='dividend-actions-chart', figure=dividend_fig),
        html.Button('Show Dividend Types', id='dividend-detail-view', n_clicks=0),
        html.Div(id='toggle-simplified-view', children=[dcc.Graph(figure=simplified_monthly_dividend_fig)]),
    ])


def get_view_3_layout():
    # Return a layout for View 3
    return html.Div([
        html.H1('Content for View 3'),
        # Include any components specific to View 3 here.
    ])

# Placeholder function for View 4 layout.
def get_view_4_layout():
    # Return a layout for View 4
    return html.Div([
        html.H1('Content for View 4'),
        # Include any components specific to View 4 here.
    ])


@callback(
    Output('toggle-simplified-view', 'children'),
    [Input('dividend-detail-view', 'n_clicks')],
    prevent_initial_call=True
)

def toggle_dividend_view(n_clicks):
    # Determine if we should show the simplified or detailed view based on the number of clicks
    if n_clicks % 2 == 0:
        # Show detailed view
        figure = simplified_monthly_dividend_fig
    else:
        # Show simplified view
        figure = monthly_dividend_fig
    return [dcc.Graph(figure=figure)]



layout = html.Div([
    html.Div([
        html.Button('Buy/Sell', id='btn-view1', n_clicks=0),
        html.Button('Dividend', id='btn-view2', n_clicks=0),
        html.Button('View 3', id='btn-view3', n_clicks=0),  # New button for View 3
        html.Button('View 4', id='btn-view4', n_clicks=0),
    ]),
    html.Div(id='page-content', children=get_view_1_layout())  # Directly load View 1 content.
])

