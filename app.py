import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go

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
                inline=True
            )
        ], width=4, className="mb-3")
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Button("Show", id='show-button', color='primary', className='mt-2')
        ], width=12, className="d-flex justify-content-center mb-4")
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
    [Input('show-button', 'n_clicks')],
    [State('tickers', 'value'),
     State('date-range', 'start_date'),
     State('date-range', 'end_date'),
     State('moving-averages', 'value')]
)

def update_graph(n_clicks, tickers, start_date, end_date, moving_averages):
    if not n_clicks or not tickers:
        return go.Figure()

    tickers = [ticker.strip() for ticker in tickers.split(',')]

    # Convert start_date and end_date to proper date format
    start_date = pd.to_datetime(start_date).strftime('%Y-%m-%d')
    end_date = pd.to_datetime(end_date).strftime('%Y-%m-%d')

    data = yf.download(tickers, start=start_date, end=end_date)

    fig = go.Figure()

    if len(tickers) == 1:
        try:
            df = data['Adj Close'].dropna()
        except KeyError:
            raise "Invalid ticker name. Please recheck the company tickers."
        
        fig.add_trace(go.Scatter(x=df.index, y=df, mode='lines', name=f"{tickers[0]} Price"))

        for ma in moving_averages:
            ma_series = df.rolling(window=ma).mean()
            fig.add_trace(go.Scatter(x=ma_series.index, y=ma_series, mode='lines', name=f"{tickers[0]} {ma}-day MA"))
    
    else:
        for ticker in tickers:
            try:
                df = data['Adj Close'][ticker].dropna()
            except KeyError:
                raise "Invalid ticker name. Please recheck the company tickers."
                
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
