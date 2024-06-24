import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], title="Financial Data Visualization")

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Financial Data Visualization Dashboard", className='text-center'), className="mb-4 mt-4")
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Label("Enter Ticker Symbols (comma separated)"),
            dbc.Input(id='tickers', placeholder="AAPL, MSFT, GOOGL", type="text")
        ], width=4),
        dbc.Col([
            dbc.Label("Select Date Range"),
            dcc.DatePickerRange(
                id='date-range',
                start_date=pd.to_datetime('2020-01-01'),
                end_date=pd.to_datetime('2023-01-01'),
                display_format='YYYY-MM-DD'
            )
        ], width=4),
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
                inline=True
            )
        ], width=4)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='price-chart')
        ])
    ])
])

# Define the callback to update the graph
@app.callback(
    Output('price-chart', 'figure'),
    [Input('tickers', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('moving-averages', 'value')]
)
def update_graph(tickers, start_date, end_date, moving_averages):
    if not tickers:
        return go.Figure()

    tickers = [ticker.strip() for ticker in tickers.split(',')]

    start_date = pd.to_datetime(start_date).strftime('%Y-%m-%d')
    end_date = pd.to_datetime(end_date).strftime('%Y-%m-%d')

    data = yf.download(tickers, start=start_date, end=end_date)

    fig = go.Figure()

    for ticker in tickers:
        df = data['Adj Close'][ticker].dropna()
        fig.add_trace(go.Scatter(x=df.index, y=df, mode='lines', name=f"{ticker} Price"))

        for ma in moving_averages:
            ma_series = df.rolling(window=ma).mean()
            fig.add_trace(go.Scatter(x=ma_series.index, y=ma_series, mode='lines', name=f"{ticker} {ma}-day MA"))

    fig.update_layout(
        title="Stock Prices and Moving Averages",
        xaxis_title="Date",
        yaxis_title="Price",
        legend_title="Legend",
        template="plotly_dark"
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
