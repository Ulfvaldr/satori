import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import os

# Load dataset
file_path = "static/sample_data.csv"  # Replace with your uploaded file path
df = pd.read_csv(file_path)

app = dash.Dash(__name__)

# Build layout
app.layout = html.Div([
    html.H1("Data Insights Dashboard"),
    html.Div([
        html.Label("Select X-axis:"),
        dcc.Dropdown(
            id="x-axis",
            options=[{"label": col, "value": col} for col in df.columns],
            value=df.columns[0]
        ),
        html.Label("Select Y-axis:"),
        dcc.Dropdown(
            id="y-axis",
            options=[{"label": col, "value": col} for col in df.columns],
            value=df.columns[1]
        )
    ]),
    dcc.Graph(id="scatter-plot"),
    dcc.Graph(
        id="correlation-heatmap",
        figure=px.imshow(df.corr(), title="Correlation Heatmap")
    )
])

# Callback to update scatterplot
@app.callback(
    dash.dependencies.Output("scatter-plot", "figure"),
    [dash.dependencies.Input("x-axis", "value"),
     dash.dependencies.Input("y-axis", "value")]
)
def update_scatter(x_col, y_col):
    return px.scatter(df, x=x_col, y=y_col, title=f"{x_col} vs {y_col}")

if __name__ == '__main__':
    app.run_server(debug=True)
