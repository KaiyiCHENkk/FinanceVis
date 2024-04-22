from dash import dcc, html
import pandas as pd
import plotly.graph_objs as go
from data.dataManage import filter_buysell_data, aggregate_data_volume

def create_buysell_volume(df):
    """
    Creates a bar chart representing monthly buy and sell transactions for different account types.

    Parameters:
        df (DataFrame): The main DataFrame containing transaction data.

    Returns:
        go.Figure: A Plotly graph object figure containing the bar chart of buy and sell volumes.
    """
    inv_buys = aggregate_data_volume(filter_buysell_data(df, 2131, 'buy'))
    inv_sells = aggregate_data_volume(filter_buysell_data(df, 2131, 'sell'))  
    isa_buys = aggregate_data_volume(filter_buysell_data(df, 2129, 'buy'))
    isa_sells = aggregate_data_volume(filter_buysell_data(df, 2129, 'sell'))  

    all_months = sorted(set(inv_buys.index) | set(inv_sells.index) | set(isa_buys.index) | set(isa_sells.index))
    inv_buys = inv_buys.reindex(all_months, fill_value=0)
    inv_sells = inv_sells.reindex(all_months, fill_value=0)
    isa_buys = isa_buys.reindex(all_months, fill_value=0)
    isa_sells = isa_sells.reindex(all_months, fill_value=0)

    fig = go.Figure()

    fig.add_trace(go.Bar(x=all_months, y=inv_buys, name='INV Buys', offsetgroup=0))
    fig.add_trace(go.Bar(x=all_months, y=isa_buys, name='ISA Buys', offsetgroup=0, base=inv_buys))
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
        ),
        height=500 
    )

    years = pd.to_datetime(all_months).year.unique()
    for year in years[1:]:  # Start from the second year to avoid adding a line at the very start
        start_of_year = f"{year}-01-01"
        fig.add_vline(x=start_of_year, line_width=1, line_dash="dash", line_color="black")
    return fig

def get_buysellTrans_layout(df):
    """
    Generates the layout for the Buy/Sell Transactions view.

    Parameters:
        df (DataFrame): DataFrame containing transaction data.

    Returns:
        html.Div: A Dash HTML component containing the layout for the buy/sell transactions.
    """
    return html.Div([
        html.H1('Investment Transactions: Buys and Sells'),
        dcc.Graph(figure=create_buysell_volume(df)),  # Dynamically create and use the figure here
    ])


