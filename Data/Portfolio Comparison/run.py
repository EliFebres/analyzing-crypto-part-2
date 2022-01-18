from get_data import *
import pandas as pd
import matplotlib.pyplot as plt

start_date = dt.datetime(2016,3,1)
end_date = dt.datetime(2021,12,8)
days_between = end_date - start_date
rf = 0.01


df = pd.read_excel('Data\price_data.xlsx')
price_data = df.set_index('Date')
tickers = price_data.columns.tolist()
# Get daily percentage change for each ticker
tickers_pct_change = price_data.pct_change()
# Get yearly standard deviation for each ticker
ann_sd = tickers_pct_change.apply(lambda x: np.log(1+x)).std().apply(lambda x: x*np.sqrt(250))
# Get yearly return for each ticker
yrly_return = ((price_data.pct_change().mean()+1)**252 - 1)

# Create a covariance and correlation matrix for all assets
cov_matrix = tickers_pct_change.apply(lambda x: x*np.sqrt(250)).cov()
corr_matrix = tickers_pct_change.corr()

# Pf Names
pf_names = ['S&P 500', 'Max Sharpe Ratio', 'Max Sortino Ratio', 'Max Calmar Ratio', 'Out-of-Sample Portfolio']

# Put All Pf Weights Into A DataFrame
stock_market_weights =  [0,1,0,0,0]
max_sharpe_weights =    [0.486843,0.394498,0.000238,0.073276,0.045145]
max_sortino_weights =   [0.575821,0.201929,0.00571,0.211612, 0.004927]
max_calmar_weights =    [0.934066,0.009329,0.022229,0.027774,0.006602]
target_pf_weights =     [0.233626,0.073597,0.003829,0.233443,0.455504]

pf_weights = []
pf_weights.append(stock_market_weights)
pf_weights.append(max_sharpe_weights)
pf_weights.append(max_sortino_weights)
pf_weights.append(max_calmar_weights)
pf_weights.append(target_pf_weights)

pf_daily_prices = pd.DataFrame(columns=pf_names)
pf_returns = []
pf_standard_deviation = []
pf_downside_deviation = []
pf_maximum_drawdown = []
pf_sharpe_ratio = []
pf_sortino_ratio = []
pf_calmar_ratio = []
for i in range(len(pf_weights)):
    # Get Daily Prices for Each Pf
    pf_price_data = price_data.dot(pf_weights[i])
    pf_daily_prices[pf_names[i]] = pf_price_data
    # Portfolio annual and daily return
    pf_return = np.dot(pf_weights[i], yrly_return)
    pf_returns.append(pf_return)
    # Portfolio sharpe ratio
    pf_var = cov_matrix.mul(pf_weights[i], axis=0).mul(pf_weights[i], axis=1).sum().sum()
    pf_sd = np.sqrt(pf_var)
    pf_standard_deviation.append(pf_sd)
    pf_sharpe = ((pf_return-rf)/pf_sd)
    pf_sharpe_ratio.append(pf_sharpe)
    # Portfolio sharpe ratio
    pf_daily_returns = tickers_pct_change.mul(pf_weights[i]).sum(axis=1)
    downside_deviation = pf_daily_returns.clip(upper=0).std()
    annual_dd = abs(downside_deviation * np.sqrt(250))
    pf_downside_deviation.append(annual_dd)
    pf_sortino = ((pf_return-rf)/annual_dd)
    pf_sortino_ratio.append(pf_sortino)
    # Portfolio Calmar Ratio
    pf_daily_price = price_data.mul(pf_weights[i]).sum(axis=1)
    rolling_max = pf_daily_price.cummax()
    daily_drawdown = (pf_daily_price/rolling_max) - 1.0
    max_drawdown = abs(daily_drawdown.cummin().min())
    pf_maximum_drawdown.append(max_drawdown)
    pf_calmar = ((pf_return-rf)/max_drawdown)
    pf_calmar_ratio.append(pf_calmar)


pf_data = {'Return':pf_returns , 'Standard Deviation': pf_standard_deviation, 
        'Downside Deviation': pf_downside_deviation, 'Maximum Drawdown': pf_maximum_drawdown,
        'Sharpe Ratio': pf_sharpe_ratio, 'Sortino Ratio': pf_sortino_ratio, 
        'Calmar Ratio': pf_calmar_ratio}

portfolio_performance = pd.DataFrame(pf_data, index=pf_names)

# Take first row divide by 100 then times the reat by answer
shares_df = 100/pf_daily_prices
[shares] = shares_df[0:1].values.tolist()
pf_value = shares * pf_daily_prices


portfolio_performance.to_excel('Results\Portfolio Metrics.xlsx')
pf_value.to_excel('Results\Portfolio Performance.xlsx')