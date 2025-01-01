import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import io
import base64

# Initialize the app with a Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "AI Marketing Insights"

# Layout
app.layout = dbc.Container([
    # Header Section
    html.Div([
        html.H1("AI Marketing Insights", className="text-center", style={"color": "#007bff", "marginBottom": "20px"}),
        html.P("Upload your data, select relevant fields, and generate insightful visualizations.", 
               className="text-center", style={"color": "black", "marginBottom": "40px"}),
    ]),

    # Step 1: Upload Data
    dbc.Card([
        dbc.CardHeader("Step 1: Upload Your Data", style={"backgroundColor": "#007bff", "color": "white"}),
        dbc.CardBody([
            dcc.Upload(
                id='upload-data',
                children=html.Div(['Drag and Drop or ', html.A('Browse')]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'backgroundColor': '#f8f9fa',
                    'color': '#343a40'
                },
                multiple=False
            ),
            html.Div(id='file-info', className="mt-3", style={"color": "black"}),
        ])
    ], className="mb-4 shadow-sm", style={"border": "1px solid #dee2e6", "backgroundColor": "white"}),

    # Step 2: Select Fields and Visualization Type
    dbc.Card([
        dbc.CardHeader("Step 2: Select Fields and Visualization Type", style={"backgroundColor": "#007bff", "color": "white"}),
        dbc.CardBody([
            html.Div([
                html.P("AI Suggested Fields:", style={"color": "black"}),
                html.Div(id='ai-suggested-fields', style={"color": "black", "marginBottom": "10px"}),
                html.P("Select Fields to Use:", style={"color": "black"}),
                dcc.Checklist(id='field-selection', style={"color": "black"}),
                html.P("Select Visualization Type:", style={"color": "black"}),
                dcc.Dropdown(
                    id='visualization-type',
                    options=[
                        {'label': 'Scatter Plot', 'value': 'scatter'},
                        {'label': 'Bar Chart', 'value': 'bar'},
                        {'label': 'Line Chart', 'value': 'line'},
                        {'label': 'Histogram', 'value': 'histogram'},
                        {'label': '3D Scatter Plot', 'value': 'scatter_3d'},
                        {'label': 'Heatmap', 'value': 'heatmap'},
                        {'label': 'Bubble Chart', 'value': 'bubble'},
                        {'label': 'Pie Chart', 'value': 'pie'},
                        {'label': 'Box Plot', 'value': 'box'},
                        {'label': 'Violin Plot', 'value': 'violin'}
                    ],
                    value='scatter',
                    style={'marginTop': '10px', 'backgroundColor': 'white', 'color': 'black'}
                ),
            ]),
            html.Button("Generate Report", id="generate-report-btn", n_clicks=0, 
                        className="btn", style={"backgroundColor": "#007bff", "color": "white", "marginTop": "20px"})
        ])
    ], className="mb-4 shadow-sm", style={"border": "1px solid #dee2e6", "backgroundColor": "white"}),

    # Step 3: View Results
    dbc.Card([
        dbc.CardHeader("Step 3: View Results", style={"backgroundColor": "#007bff", "color": "white"}),
        dbc.CardBody([
            html.Div(id='report-output', style={"color": "black"})
        ])
    ], className="shadow-sm", style={"border": "1px solid #dee2e6", "backgroundColor": "white"})
], fluid=True, style={"backgroundColor": "#f8f9fa", "padding": "20px"})

# Helper function to parse uploaded file
def parse_contents(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        df.columns = [col.replace('_', ' ').title() for col in df.columns]
        return df
    except Exception as e:
        return None

# Helper function to suggest fields
def suggest_fields(df):
    numerical_cols = df.select_dtypes(include=['number'])
    top_variance = numerical_cols.var().sort_values(ascending=False).index[:3].tolist()
    if 'Purchase Likelihood' in df.columns:
        correlations = numerical_cols.corrwith(df['Purchase Likelihood']).abs().sort_values(ascending=False)
        top_correlated = correlations.index[:3].tolist()
    else:
        top_correlated = []
    suggested_fields = list(dict.fromkeys(top_variance + top_correlated))
    return suggested_fields[:3]

# Callback to process uploaded data and suggest fields
@app.callback(
    [Output('file-info', 'children'),
     Output('ai-suggested-fields', 'children'),
     Output('field-selection', 'options')],
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def process_file(contents, filename):
    if contents is not None:
        df = parse_contents(contents)
        if df is not None:
            suggested_fields = suggest_fields(df)
            options = [{'label': col, 'value': col} for col in df.columns]
            return (
                html.Div([
                    html.H5(f"File Uploaded: {filename}", style={"color": "black"}),
                    html.P(f"Data Shape: {df.shape[0]} rows, {df.shape[1]} columns", style={"color": "black"}),
                    html.Pre(df.head().to_string(), style={'overflowX': 'scroll', 'color': "black"})
                ]),
                f"Suggested Fields: {', '.join(suggested_fields)}",
                options
            )
        else:
            return "Error processing file.", "", []
    return "No file uploaded.", "", []

# Callback to generate report
@app.callback(
    Output('report-output', 'children'),
    [Input('generate-report-btn', 'n_clicks')],
    [State('upload-data', 'contents'),
     State('field-selection', 'value'),
     State('visualization-type', 'value')]
)
def generate_report(n_clicks, contents, selected_fields, visualization_type):
    if n_clicks > 0 and contents is not None and selected_fields:
        df = parse_contents(contents)
        if df is not None:
            if visualization_type == 'scatter' and len(selected_fields) >= 2:
                fig = px.scatter(df, x=selected_fields[0], y=selected_fields[1], title="Scatter Plot", template='simple_white')
            elif visualization_type == 'bar' and len(selected_fields) >= 2:
                fig = px.bar(df, x=selected_fields[0], y=selected_fields[1], title="Bar Chart", template='simple_white')
            elif visualization_type == 'line' and len(selected_fields) >= 2:
                fig = px.line(df, x=selected_fields[0], y=selected_fields[1], title="Line Chart", template='simple_white')
            elif visualization_type == 'histogram' and len(selected_fields) >= 1:
                fig = px.histogram(df, x=selected_fields[0], title="Histogram", template='simple_white')
            elif visualization_type == 'scatter_3d' and len(selected_fields) == 3:
                fig = px.scatter_3d(df, x=selected_fields[0], y=selected_fields[1], z=selected_fields[2], title="3D Scatter Plot", template='simple_white')
            elif visualization_type == 'heatmap' and len(selected_fields) >= 2:
                fig = px.density_heatmap(df, x=selected_fields[0], y=selected_fields[1], title="Heatmap", template='simple_white')
            elif visualization_type == 'bubble' and len(selected_fields) >= 3:
                fig = px.scatter(df, x=selected_fields[0], y=selected_fields[1], size=selected_fields[2], title="Bubble Chart", template='simple_white')
            elif visualization_type == 'pie' and len(selected_fields) >= 1:
                fig = px.pie(df, names=selected_fields[0], title="Pie Chart", template='simple_white')
            elif visualization_type == 'box' and len(selected_fields) >= 1:
                fig = px.box(df, y=selected_fields[0], title="Box Plot", template='simple_white')
            elif visualization_type == 'violin' and len(selected_fields) >= 1:
                fig = px.violin(df, y=selected_fields[0], title="Violin Plot", template='simple_white')
            else:
                return "Insufficient fields selected for visualization."
            return dcc.Graph(figure=fig)
    return "No valid fields selected or insufficient data for visualization."

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
