import dash
from dash import dcc, html
import plotly.graph_objs as go
from data.dataManage import aggregate_dividend_data, aggregate_dividend_data_by_month
 


def create_dividend_figure(dividend_df):
    """
    Creates a bar chart displaying the total dividends by type for each ticker.
    
    Parameters:
        dividend_df (DataFrame): The DataFrame containing dividend data.

    Returns:
        go.Figure: A Plotly graph object figure containing the stacked bar chart of dividends.
    """

    aggregated_dividend_data = aggregate_dividend_data(dividend_df)
    aggregated_dividend_data['Total'] = aggregated_dividend_data.sum(axis=1)

    # Sort tickers based on the sum of dividends
    sorted_tickers = aggregated_dividend_data.sort_values('Total', ascending=False).index.tolist()
    aggregated_dividend_data = aggregated_dividend_data.drop('Total', axis=1)
    
    fig = go.Figure()
    for dividend_type in aggregated_dividend_data.columns:
        fig.add_trace(go.Bar(
            x=sorted_tickers,
            y=aggregated_dividend_data.loc[sorted_tickers, dividend_type],
            name=dividend_type
        ))
    fig.update_layout(
        barmode='stack', 
        title_text='Dividend Types by Ticker',
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    return fig


def create_monthly_dividend_figure(dividend_df):
    """
    Creates a stacked bar chart of monthly dividends by ticker and type over time.
    
    Parameters:
        dividend_df (DataFrame): The DataFrame containing monthly dividend data.

    Returns:
        go.Figure: A Plotly graph object figure with detailed views of monthly dividends.
    """

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
            type="date",
        ),
        height=500        
    )
    return fig

def create_simplified_monthly_dividend_figure(dividend_df):
    """
    Creates a simplified bar chart of monthly dividends by ticker.
    
    Parameters:
        dividend_df (DataFrame): The DataFrame containing monthly dividend data aggregated by ticker and month.

    Returns:
        go.Figure: A Plotly graph object figure with a simplified view of monthly dividends.
    """

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
        legend_title='Ticker',
        height=500,
    )
    return fig


def get_dividend_layout(dividend_df):
    """
    Constructs the layout for the dividend view, including the detailed and simplified charts.

    Parameters:
        dividend_df (DataFrame): The DataFrame containing all dividend data.

    Returns:
        html.Div: A Dash HTML component that includes all elements of the dividend layout.
    """
    
    dividend_fig = create_dividend_figure(dividend_df)
    simplified_fig = create_simplified_monthly_dividend_figure(dividend_df)
    layout = html.Div([
        html.H2('Dividend Actions by Ticker and Type'),
        dcc.Graph(id='dividend-actions-chart', figure=dividend_fig),
        html.Button('Toggle View', id='dividend-detail-view', n_clicks=0),
        html.Div(id='toggle-simplified-view', children=[dcc.Graph(figure=simplified_fig)]),
    ])
    return layout






