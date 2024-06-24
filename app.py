import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
from redis_cache import get_stock_data  # Import the caching function

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], title="Financial Data Visualization")

# Define the layout of the app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Financial Data Visualization Dashboard", className='text-center'), className="mb-4 mt-4")
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Label("Enter Ticker Symbols (comma separated)"),
            dbc.Input(id='tickers', placeholder="AAPL, MSFT, GOOGL", type="text")
        ], width=4, className="mb-3"),
        dbc.Col([
            dbc.Label("Select Date Range"),
            dcc.DatePickerRange(
                id='date-range',
                start_date='2020-01-01',
                end_date='2024-06-01',
                display_format='YYYY-MM-DD'
            )
        ], width=4, className="mb-3"),
        dbc.Col([
            dbc.Label("Select Moving Averages"),
            dcc.Checklist(
                id='moving-averages',
                options=[
                    {'label': '20-day', 'value': 20},
                    {'label': '50-day', 'value': 50},
                    {'label': '100-day', 'value': 100}
                ],
                value=[20, 50],
                inline=True,
                className='mt-2'
            )
        ], width=4, className="mb-3")
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Label("Select Additional Features"),
            dcc.Checklist(
                id='additional-features',
                options=[
                    {'label': 'Show Trading Volume', 'value': 'volume'}
                ],
                value=['volume'],
                inline=True,
                className='mt-2'
            )
        ], width=12, className="mb-4")
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Button("Show", id='show-button', color='primary', className='mt-2')
        ], width=12, className="d-flex justify-content-center mb-4")
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='price-chart')
        ], className='mb-4')
    ])
])

# Define the callback to update the graph
@app.callback(
    Output('price-chart', 'figure'),
    [Input('show-button', 'n_clicks')],
    [State('tickers', 'value'),
     State('date-range', 'start_date'),
     State('date-range', 'end_date'),
     State('moving-averages', 'value'),
     State('additional-features', 'value')]
)

def update_graph(n_clicks, tickers, start_date, end_date, moving_averages, additional_features):
    if not n_clicks or not tickers:
        return go.Figure()

    tickers = [ticker.strip() for ticker in tickers.split(',')]

    # Convert start_date and end_date to proper date format
    start_date = pd.to_datetime(start_date).strftime('%Y-%m-%d')
    end_date = pd.to_datetime(end_date).strftime('%Y-%m-%d')

    # Get or set cached data
    data = get_stock_data(tickers, start_date, end_date)

    fig = go.Figure()

    for ticker in tickers:
        if len(tickers) == 1:
            df_price = data['Adj Close'].dropna()
            df_volume = data['Volume'].dropna()
        else:
            df_price = data['Adj Close'][ticker].dropna()
            df_volume = data['Volume'][ticker].dropna()

        fig.add_trace(go.Scatter(x=df_price.index, y=df_price, mode='lines', name=f"{ticker} Price"))

        for ma in moving_averages:
            ma_series = df_price.rolling(window=ma).mean()
            fig.add_trace(go.Scatter(x=ma_series.index, y=ma_series, mode='lines', name=f"{ticker} {ma}-day MA"))

        if 'volume' in additional_features:
            fig.add_trace(go.Bar(x=df_volume.index, y=df_volume, name=f"{ticker} Volume", yaxis='y2', opacity=0.3))

    fig.update_layout(
        title="Stock Prices and Moving Averages",
        xaxis_title="Date",
        yaxis_title="Price",
        legend_title="Legend",
        template="plotly_dark",
        yaxis2=dict(
            title='Volume',
            overlaying='y',
            side='right',
            showgrid=False
        )
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
