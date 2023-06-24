import websockets
import mplfinance as mpf
import pandas as pd
import json

# Create a WebSocket object
ws = websockets.connect('wss://stream.aliceblue.in/')

# Subscribe to the Tata Motors instrument
data = {'exchange': 'NSE', 'symbol': 'TATAMOTORS'}
ws.send(json.dumps(data))

# Create a candlestick chart
fig, ax = mpf.plot(None, type='candlestick')

# Start receiving data from the WebSocket server
while True:
    message = ws.recv()
    data = json.loads(message)

    # Add the new data to the chart
    df = pd.DataFrame(data, columns=['timestamp', 'lp'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    mpf.plot(df, ax=ax)

    # Update the chart
    plt.show()
