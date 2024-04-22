import dash
from dash import html, dcc 
import dash_bootstrap_components as dbc

# Initialize the Dash app with specific external stylesheets and configuration settings.
# The app uses the Dash Bootstrap SPACELAB theme and suppresses exceptions for callback.
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SPACELAB], suppress_callback_exceptions=True)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div("Welcome to FinVis!",
                         style={'fontSize':50, 'textAlign':'center'}))
    ]),

    html.Hr(),

    dbc.Row(
        [
            dbc.Col(
                [
                    dash.page_container
                ], xs=9, sm=9, md=12, lg=12, xl=12, xxl=12)
        ]
    )
], fluid=True)


if __name__ == '__main__':
    app.run_server(debug=True, port=8052)

