from matplotlib import ticker
import pandas as pd
import pandas_datareader as pdr

# Import CRIX Historical Data
df = pd.read_excel('CRIX.xlsx')
crix_df = df.set_index('Date')

# Get Data for each Asset Class
tickers = ['SPY', 'IYR', 'GLD']
ticker_prices = pdr.DataReader(tickers, 'yahoo', start='2016-03-01', end='2021-12-08')['Adj Close']

# Combine each dataset and remove NaN Rows
data_frames = [crix_df, ticker_prices]
data = pd.concat(data_frames, axis=1,).dropna()

# Get Correlation Table for each Asset Class
df_corr = data.corr(method='spearman')

# Export both dataframes to to excel
with pd.ExcelWriter('output.xlsx') as writer:
    data.to_excel(writer, sheet_name='Price Date')
    df_corr.to_excel(writer, sheet_name='Correlation')