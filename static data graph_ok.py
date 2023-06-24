import pandas as pd
import datetime as datetime
import mplfinance as mpf

file=("data.xlsx")
data=pd.read_excel(file)

data.timestamp=pd.to_datetime(data.timestamp)


data=data.set_index('timestamp')

ohlc_data = data['closing price'].resample('30S').ohlc()


mpf.plot(ohlc_data,type='candle', style='charles')