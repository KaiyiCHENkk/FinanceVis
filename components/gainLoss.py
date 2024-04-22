from dash import dcc, html
import plotly.graph_objects as go

def create_gain_loss_chart(data, sort_column = 'Total'):
    """
    Creates a horizontal bar chart to display total dividends and realized capital gains and losses for each ticker.

    Parameters:
        data (DataFrame): DataFrame containing 'Ticker', 'Total Dividends', and 'Realized Capital Gain & Loss'.
        sort_column (str, optional): Column name to sort the data by. Defaults to 'Total'.

    Returns:
        go.Figure: A Plotly graph object figure containing the bar chart.
    """
    data = data[['Ticker', 'Total Dividends', 'Realized Capital Gain & Loss']]
    data_grouped = data.groupby('Ticker').sum()

    # Calculate the total values for annotation
    data_grouped['Total'] = data_grouped['Total Dividends'] + data_grouped['Realized Capital Gain & Loss']

    # Sort data by the 'Total' column in descending order
    data_grouped = data_grouped.sort_values(sort_column, ascending=True)

    fig = go.Figure()

    # Add Total Dividends as a bar
    fig.add_trace(go.Bar(
        y=[f"{idx}: £{row[sort_column]:.2f}" for idx, row in data_grouped.iterrows()],  # Modified y-axis labels
        x=data_grouped['Total Dividends'],
        name='Total Dividends',
        orientation='h',
        marker_color='blue'
    ))

    # Add Realized Capital Gain & Loss as another bar
    fig.add_trace(go.Bar(
        y=[f"{idx}: £{row[sort_column]:.2f}" for idx, row in data_grouped.iterrows()],  # Reused modified y-axis labels
        x=data_grouped['Realized Capital Gain & Loss'],
        name='Capital Gain & Loss',
        orientation='h',
        marker_color='green'
    ))

    fig.update_layout(
        barmode='relative',
        title='Total Dividends and Capital Gain & Loss',
        xaxis_title='Pounds (£)',
        yaxis_title='Ticker',
        xaxis=dict(tickprefix="£"),
        autosize=False,
        width= 1000,
        height=1500,
        paper_bgcolor='white',
        plot_bgcolor='white',
        yaxis=dict(
            type='category'  
        )
    )

    return fig

def get_gainLoss_layout(df):
    """
    Generates the layout for the Gain/Loss view containing a bar chart.

    Parameters:
        df (DataFrame): DataFrame containing data to be displayed in the bar chart.

    Returns:
        html.Div: A Dash HTML component containing the Gain/Loss layout.
    """
    gain_loss_fig = create_gain_loss_chart(df)

    return html.Div([
        html.H2('Gain/Loss'),
        dcc.Graph(id='gain-loss-chart',figure=gain_loss_fig),
    ])