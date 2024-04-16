import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go




# # Function to create the parallel coordinates chart
# def create_parallel_coordinates_figure(df):
    
#     fig = px.parallel_coordinates(df,
#                                   color="Ticker Symbol Index",
#                                   dimensions=[
#                                       "Ticker Symbol Index",
#                                       "Total Number of Shares Purchased",
#                                       "Total Purchase Amount",
#                                       "Average Price per Share",
#                                       "Total Number of Shares Sold",
#                                       "Total Sales Amount",
#                                       "Average Sale Price per Share",
#                                       "Net Total Number of Shares",
#                                       "Current Share Price",
#                                       "Total Dividends",
#                                       "Realized Capital Gain & Loss",
#                                       "Unrealized Capital Gain & Loss"
#                                   ],
#                                   labels={
#                                       "Ticker Symbol Index": "Ticker Symbol",
#                                       # Other labels as needed
#                                   },
#                                   color_continuous_scale=px.colors.diverging.Tealrose,
#                                   )
    
#     # Customize figure layout as necessary
#     fig.update_layout(coloraxis_colorbar=dict(title="Ticker Order"))
#     return fig













# def create_parallel_coordinates_figure(df):
#     # Reverse mapping for tick labels: from numeric index back to ticker symbol
#     index_to_ticker = {index: ticker for ticker, index in df['Ticker Symbol Index'].items()}

#     fig = go.Figure(data=go.Parcoords(
#         line=dict(color=df['Ticker Symbol Index'],
#                   colorscale=[[i/len(index_to_ticker), color] for i, color in enumerate(px.colors.qualitative.Plotly)]),
#         dimensions=[
#             dict(range=[1, len(index_to_ticker)],
#                  tickvals=list(index_to_ticker.keys()),
#                  ticktext=list(index_to_ticker.values()),
#                  label='Ticker Symbol', values=df['Ticker Symbol Index']),
#             # Add other dimensions as needed, similar to the above
#         ]
#     ))

#     fig.update_layout(
#         title='Company Data Analysis'
#     )

#     return fig






# import plotly.express as px

# def create_parallel_coordinates_figure(df):
    
#     # Convert numeric data to strings if necessary, to ensure all data is appropriately typed.
#     # Note: Plotly Express might handle numerical data more straightforwardly than categorical.
    
#     # Ensuring 'Ticker Symbol' is the first column to maintain its priority in the plot.
#     ordered_columns = ['Ticker Symbol'] + [col for col in df.columns if col != 'Ticker Symbol']
#     df = df[ordered_columns]
    
#     # The Plotly Express parallel_coordinates function does not directly support 
#     # categorical data as the 'color' argument without a numeric mapping. 
#     # Here, we focus on visualizing the dimensions including the ticker symbol as one of them.
#     fig = px.parallel_coordinates(df, color=df.columns[1],  # Example: use the second column for coloring
#                                   dimensions=ordered_columns,
#                                   labels={col: col.replace('_', ' ') for col in ordered_columns},
#                                   color_continuous_scale=px.colors.diverging.Tealrose)

#     fig.update_layout(
#         title='Risk Factors Analysis'
#     )
    
#     return fig




# def create_parallel_coordinates_figure(df):
#     # Create a numerical mapping for 'Ticker Symbol' to use as colors
#     unique_tickers = df['Ticker Symbol'].unique()
#     ticker_to_num = {ticker: i for i, ticker in enumerate(unique_tickers)}
#     df['Ticker Color'] = df['Ticker Symbol'].map(ticker_to_num)

#     # Generate the parallel coordinates plot using the numerical mapping for colors
#     fig = px.parallel_coordinates(df, color='Ticker Color',
#                                   labels={"Ticker Symbol": "Ticker Symbol", 
#                                           "Total Number of Shares Purchased": "Total Shares Purchased",
#                                           "Total Purchase Amount": "Total Purchase Amount",
#                                           "Average Price per Share": "Avg Price/Share (Purchase)",
#                                           "Total Number of Shares Sold": "Total Shares Sold",
#                                           "Total Sales Amount": "Total Sales Amount",
#                                           "Average Sale Price per Share": "Avg Price/Share (Sales)",
#                                           "Net Total Number of Shares": "Net Total Shares",
#                                           "Current Share Price": "Current Share Price",
#                                           "Total Dividends": "Total Dividends",
#                                           "Realized Capital Gain & Loss": "Realized Gains/Losses",
#                                           "Unrealized Capital Gain & Loss": "Unrealized Gains/Losses"},
#                                   dimensions=["Total Number of Shares Purchased", "Total Purchase Amount",
#                                                "Average Price per Share", "Total Number of Shares Sold",
#                                                "Total Sales Amount", "Average Sale Price per Share",
#                                                "Net Total Number of Shares", "Current Share Price",
#                                                "Total Dividends", "Realized Capital Gain & Loss",
#                                                "Unrealized Capital Gain & Loss"],
#                                   color_continuous_scale=px.colors.diverging.Tealrose,
#                                   color_continuous_midpoint=2)

#     # Customize the color scale and midpoint as needed
#     return fig




def create_parallel_coordinates_figure(df):
    # Mapping each ticker symbol to a unique number
    # ticker_map = {ticker: i for i, ticker in enumerate(df['Ticker'].unique())}
    # df['Ticker Index'] = df['Ticker'].apply(lambda x: ticker_map[x])

    # Creating a color scale based on the number of tickers
    # color_scale = [[i/len(ticker_map), color] for i, color in enumerate(px.colors.qualitative.Plotly)]

    # # Creating dimensions, starting with the Ticker as the first dimension
    # dimensions = [
    #     dict(range=[0, len(ticker_map)-1],
    #          tickvals=list(ticker_map.values()),
    #          ticktext=list(ticker_map.keys()),
    #          label='Ticker', values=df['Ticker Index']),

    unique_ticker_indices = df['Ticker Index'].unique()
    color_scale = [[i/len(unique_ticker_indices), color] for i, color in enumerate(px.colors.qualitative.Plotly)]

    # Adjusting dimensions to include 'Ticker' as the label with the values from 'Ticker Index'
    dimensions = [
        dict(range=[min(unique_ticker_indices), max(unique_ticker_indices)],
             tickvals=list(df['Ticker Index'].unique()),
             ticktext=list(df['Ticker'].unique()),  # Keeping the label as 'Ticker'
             label='Ticker', values=df['Ticker Index']),
        dict(label='Average Price per Share', values=df['Average Price per Share']),
        dict(label='Total Purchase Amount', values=df['Total Purchase Amount']),
        dict(label='Total Number of Shares Purchased', values=df['Total Number of Shares Purchased']),
        dict(label='Total Number of Shares Sold', values=df['Total Number of Shares Sold']),
        dict(label='Total Sales Amount', values=df['Total Sales Amount']),
        dict(label='Average Sale Price per Share', values=df['Average Sale Price per Share']),
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

    # Updating layout for better visibility
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        height = 900,
        font=dict(size=12),
    )

    return fig





# Layout function for the Risk Factors view
def get_risk_layout(df):
    # Use the chart creation function to generate the figure
    parallel_coordinates_fig = create_parallel_coordinates_figure(df)

    # Return the layout with the generated figure
    return html.Div([
        html.H2('Risk Factors'),
        dcc.Graph(id='risk-parallel-chart',figure=parallel_coordinates_fig),
        #html.Div(id='selection-output')
    ])
