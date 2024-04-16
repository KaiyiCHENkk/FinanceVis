import dash
from dash import dcc, html
import plotly.express as px

dash.register_page(__name__, title="MoneyVis")

df = px.data.tips()

layout = html.Div(
    [
        dcc.Markdown('Page 2')
    ]
)
