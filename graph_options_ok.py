import pandas as pd
import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go

file = "data.xlsx"
data = pd.read_excel(file)
data.timestamp = pd.to_datetime(data.timestamp)
data = data.set_index('timestamp')

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div(
        dcc.Graph(
            id='chart',
            config={'displayModeBar': True},
            style={'width': '100vw', 'height': '90vh'}
        ),
        style={'position': 'relative'}
    ),
    html.Div([
        html.Label('Select Time Range:'),
        dcc.RadioItems(
            id='time-range',
            options=[
                {'label': '1 Minute', 'value': '1Min'},
                {'label': '2 Minute', 'value': '2Min'},
                {'label': '3 Minute', 'value': '3Min'},
                {'label': '5 Minutes', 'value': '5Min'},
                {'label': '10 Minutes', 'value': '10Min'},
                {'label': '15 Minutes', 'value': '15Min'},
                {'label': '30 Minutes', 'value': '30Min'}
            ],
            value='1Min',
            labelStyle={'display': 'inline-block', 'margin-right': '10px'}
        )
    ], style={'margin-top': '20px'}),
    html.Div([
        html.Button('Zoom In', id='zoom-in-btn', n_clicks=0, style={'margin-right': '10px'}),
        html.Button('Zoom Out', id='zoom-out-btn', n_clicks=0)
    ], style={'margin-top': '10px'})
])

@app.callback(
    dash.dependencies.Output('chart', 'figure'),
    dash.dependencies.Input('time-range', 'value'),
    dash.dependencies.Input('zoom-in-btn', 'n_clicks'),
    dash.dependencies.Input('zoom-out-btn', 'n_clicks')
)
def update_chart(time_range, zoom_in_btn_clicks, zoom_out_btn_clicks):
    # Handle time range selection
    ohlc_data = data['closing price'].resample(time_range).ohlc()
    
    # Handle zoom in/out button clicks
    zoom_level = 0.2 * (zoom_in_btn_clicks - zoom_out_btn_clicks)
    x_range = [data.index[0] - pd.DateOffset(seconds=zoom_level), data.index[-1] + pd.DateOffset(seconds=zoom_level)]
    
    figure = {
        'data': [
            go.Candlestick(
                x=ohlc_data.index,
                open=ohlc_data['open'],
                high=ohlc_data['high'],
                low=ohlc_data['low'],
                close=ohlc_data['close']
            )
        ],
        'layout': go.Layout(
            title="Candlestick Chart",
            xaxis=dict(
                title="Timestamp",
                range=x_range,
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label='1d', step='day', stepmode='backward'),
                        dict(count=7, label='1w', step='day', stepmode='backward'),
                        dict(count=1, label='1m', step='month', stepmode='backward'),
                        dict(count=3, label='3m', step='month', stepmode='backward'),
                        dict(step='all')
                    ]),
                    bgcolor='rgba(150, 200, 250, 0.4)',
                    x=0.98,
                    xanchor='right',
                    y=1.05,
                    yanchor='top'
                )
            ),
            yaxis=dict(title="Price"),
            uirevision=True
        )
    }
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
