import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def create_parallel_coordinates_figure(df):
    """
    Creates a parallel coordinates plot for visualizing multivariate data points across different dimensions.

    Parameters:
        df (DataFrame): The DataFrame containing company-related data indexed by tickers.

    Returns:
        go.Figure: A Plotly graph object figure containing the parallel coordinates plot.
    """

    unique_ticker_indices = df['Ticker Index'].unique()

    plasma_color_scale = px.colors.sequential.Plasma
    
    # Calculate equally spaced intervals for each ticker on the Plasma color scale
    n_tickers = len(unique_ticker_indices)

    # Create a color scale for each ticker
    color_scale = [
        [i / (n_tickers - 1), plasma_color_scale[int(i * (len(plasma_color_scale) - 1) / (n_tickers - 1))]]
        for i in range(n_tickers)
    ]

    # Adjusting dimensions to include 'Ticker' as the label with the values from 'Ticker Index'
    dimensions = [
        dict(range=[min(unique_ticker_indices), max(unique_ticker_indices)],
             tickvals=list(df['Ticker Index'].unique()),
             ticktext=list(df['Ticker'].unique()),  # Keeping the label as 'Ticker'
             label='Ticker', values=df['Ticker Index']),
        dict(label='Number of Shares Purchased', values=df['Total Number of Shares Purchased']),
        dict(label='Total Purchase Amount', values=df['Total Purchase Amount']),
        dict(label='Average Purchase Price/Share', values=df['Average Price per Share']),
        dict(label='Number of Shares Sold', values=df['Total Number of Shares Sold']),
        dict(label='Total Sales Amount', values=df['Total Sales Amount']),
        dict(label='Average Sale Price/Share', values=df['Average Sale Price per Share']),
        dict(label='Net Total Number of Shares', values=df['Net Total Number of Shares']),
        dict(label='Current Share Price', values=df['Current Share Price']),
        dict(label='Total Dividends', values=df['Total Dividends']),
        dict(label='Realized Capital Gain & Loss', values=df['Realized Capital Gain & Loss']),
        dict(label='Unrealized Capital Gain & Loss', values=df['Unrealized Capital Gain & Loss']),
    ]

    # Creating the figure with the dimensions list
    fig = go.Figure(data=go.Parcoords(
        line=dict(color=df['Ticker Index'], colorscale=color_scale),
        dimensions=dimensions
    ))

    # Add a scatter trace with a color bar for color mapping visualization
    fig.add_trace(go.Scatter(
        x=[None], y=[None], mode='markers',
        marker=dict(
            size=10,
            color=unique_ticker_indices,
            colorscale=plasma_color_scale,
            showscale=True,
            cmin=min(unique_ticker_indices),
            cmax=max(unique_ticker_indices),
            colorbar=dict(title="Colour Map")
        )
    ))

    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        height = 900,
        font=dict(size=12),
        xaxis={'visible': False},  
        yaxis={'visible': False},
        title='Company Metadata Overview', 
    )

    return fig





# Layout function for the Risk Factors view
def get_risk_layout(df):
    """
    Generates the layout for the Risk Factors view containing a parallel coordinates chart.

    Parameters:
        df (DataFrame): DataFrame containing data to be displayed in the parallel coordinates chart.

    Returns:
        html.Div: A Dash HTML component containing the Risk Factors layout.
    """
    # Use the chart creation function to generate the figure
    parallel_coordinates_fig = create_parallel_coordinates_figure(df)

    # Return the layout with the generated figure
    return html.Div([
        html.H2('Risk Factors'),
        dcc.Graph(id='risk-parallel-chart',figure=parallel_coordinates_fig),
    ])
 