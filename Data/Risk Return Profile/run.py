from tracemalloc import start
from matplotlib import ticker
import pandas as pd
import pandas_datareader as pdr
import numpy as np
import datetime as dt

start_date = dt.datetime(2016,3,1)
end_date = dt.datetime(2021,12,8)
days_between = end_date - start_date
risk_free = 0.01


# Import CRIX Historical Data
df = pd.read_excel('CRIX.xlsx')
crix_df = df.set_index('Date')

# Get Data for each Asset Class
tickers = ['SPY', 'IYR', 'GLD']
ticker_prices = pdr.DataReader(tickers, 'yahoo', start= start_date, end= end_date)['Adj Close']

# Combine each dataset and remove NaN Rows
data_frames = [crix_df, ticker_prices]
data = pd.concat(data_frames, axis=1,).dropna()


# Get daily percentage change for each ticker
tickers_pct_change = data.pct_change().applymap(lambda x: np.log(1+x))
# Get yearly standard deviation for each ticker
ann_sd = tickers_pct_change.apply(lambda x: np.log(1+x)).std().apply(lambda x: x*np.sqrt(250))


# Get yearly return for each ticker
yrly_return = ((data.pct_change().mean()+1)**252 - 1)


# Get Maximum Drawdown For Each Asset
rolling_max = data.rolling(window=days_between, min_periods=1).max()
daily_drawdown = data/rolling_max - 1.0
max_drawdown = daily_drawdown.min()


# Get Sortino Ratio for Each Asset
return_min_rf = tickers_pct_change - risk_free
downside_deviation = return_min_rf.clip(upper=0).std().apply(lambda x: x*np.sqrt(250))
sortino_ratio = (yrly_return-risk_free)/downside_deviation



print(yrly_return)
print(ann_sd)
print(sortino_ratio)
print(max_drawdown)

