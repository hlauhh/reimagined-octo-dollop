# retrieve data
import yfinance as yf

# process data
import pandas as pd
import numpy as np
import math

from numpy import number
from scipy.stats import norm
from sklearn import preprocessing

# plotting data
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

# Set default renderer to browser
pio.renderers.default = 'browser'

# datetime logic
import datetime

from IPython.display import display

from sklearn.utils.sparsefuncs import min_max_axis

# Show all columns and display 2 d.p.
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', '{:.5f}'.format)

# static info
crypto_arr = ['BTC-USD', 'ETH-USD', 'XRP-USD']
index_arr = ['GC=F', 'GD=F', '^GSPC']  # gold, comdty index, SP
start_date = '2015-08-01'
end_date = '2024-08-31'

# yfinance
# df = yf.download(crypto_arr, start=start_date, end=end_date)
df1 = yf.download(crypto_arr + index_arr, start=start_date, end=end_date, group_by='ticker')
# print(df.head())

# print(crypto_arr + index_arr)

# extracting the adjusted close price from df
dict_closePrice = {}
for name in crypto_arr + index_arr:
    dict_closePrice[name] = df1[name]['Adj Close']
df_closePrice = pd.DataFrame(dict_closePrice)
# print(df_closePrice.head(1))

dict_volume = {}
for name in crypto_arr + index_arr:
    dict_volume[name] = df1[name]['Volume']
df_volume = pd.DataFrame(dict_volume)
# print(df_volume.head())
# print(df_closePrice.describe())
# print(df_volume.describe())

# print(df_closePrice.columns)
# df_data = df_closePrice  # df_volume
# title_name = 'Price Movement'

'''
fig_movement = px.line(df_data, x=df_data.index, y=df_data.columns, title=title_name)
fig_movement.update_xaxes(rangeslider_visible=True,
                          rangeselector=dict(buttons=list([
                              dict(count=1, label='YTD', step='year', stepmode='todate'),
                              dict(count=1, label='1Y', step='year', stepmode='backward'),
                              dict(step='all')
                          ])),
                          )

fig_movement.show()

# Create dataframes for adjusted close price and volume
df_closePrice = pd.DataFrame(dict_closePrice).fillna(method='ffill')
df_volume = pd.DataFrame(dict_volume).fillna(method='ffill')
'''


# Plotting function for price movement and volume
def plot_movement(df_data, title_name):
    fig_movement = px.line(df_data, x=df_data.index, y=df_data.columns, title=title_name)
    fig_movement.update_xaxes(rangeslider_visible=True,
                              rangeselector=dict(buttons=list([
                                  dict(count=1, label='YTD', step='year', stepmode='todate'),
                                  dict(count=1, label='1Y', step='year', stepmode='backward'),
                                  dict(step='all')
                              ])),
                              )
    return fig_movement


# Plot graphs
# graph_1 = plot_movement(df_closePrice.copy(), 'Price Movement')
# graph_2 = plot_movement(df_volume.copy(), 'Volume')

# Display both graphs
# graph_1.show()
# graph_2.show()

# X_std = (X-X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
# X_scaled = X_std * (max - min) + min

min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 100))
scaled = min_max_scaler.fit_transform(df_closePrice)
df_closePrice_scaled = pd.DataFrame(scaled, columns=df_closePrice.columns)

# print(df_closePrice_scaled.head())

graph_3 = plot_movement(df_closePrice_scaled, 'Scale Price Movement')
graph_3.show()

# Price_t / Price_t-1 -1
# df_shifting_1 = df_closePrice.shift(1)
df_return = df_closePrice / df_closePrice.shift(1) - 1
# print(df_return.head())

graph_4 = plot_movement(df_return, "Return Movement")
graph_4.show()

df_return_7D = df_closePrice.pct_change(periods=7)
# print(df_return_7D.head())

# build-in function, % change in past 7 days
graph_5 = plot_movement(df_return_7D, "7 Days Return Movement")
graph_5.show()

# L4 static plotting
plt.plot(df_closePrice.index, df_closePrice_scaled.values)
plt.show()

# Check correlation for pair trading and showing log standardising transformation
# print(df_closePrice.head())
df_log_rtn = np.log(df_closePrice.dropna().pct_change(periods=1).dropna())
df_log_rtn_corr = df_log_rtn.corr().style.background_gradient(cmap='RdYlBu').set_caption('Correlation Matrix')
print(df_log_rtn_corr)

# Check rolling correlation
df_rtn = df_closePrice.pct_change(periods=1).dropna()

df_rtn_corr = df_rtn.corr()
df_rolling_corr = df_rtn_corr.rolling(15)

df_rolling_mean = df_rtn.rolling(5).mean().dropna()
df_rolling_corr_new = df_rtn.rolling(15).corr(df_rtn['BTC-USD'])

graph_6 = plot_movement(df_rolling_corr_new, 'BTC-USD Rolling Correlation')
graph_6.show()

print("done")

# VaR (Value at Risk 99%), Mean (Average), Std, Max, Min on Returns
# Sharpe Ratio, Worst Drop, MMD (Max Draw down 5D), MMD (Max Draw down 30D)

df_indicators = df_rtn.describe().T
df_indicators.rename(columns={"25%": "Var_25", "count": "Count", "mean": "Mean", "std": "Std", 'max': 'Max'},
                     inplace=True)
#Sharpe Ratio
df_indicators['Sharpe Ratio'] = df_indicators['Mean'] / df_indicators['Std']

# Setting placeholder in list
df_indicators['VaR_99%'], df_indicators['Worst_Drop'], df_indicators['Worst_Date'] = 0,0,0
df_indicators['MMD_5D'], df_indicators['MMD_30D'] = 0,0

# for loop to get data from return df
for c in df_rtn.columns:
    print(c)
    sorted_return = df_rtn[c].dropna().sort_values(ascending=True)
    df_indicators.loc[c,'VaR_99%'] = sorted_return.quantile(0.01)
    df_indicators.loc[c,'Worst_Drop'] = sorted_return.min()
    df_indicators.loc[c,'Worst_Date'] = sorted_return.idxmin().strftime('%d-%b-%Y')

    # Max Drawdown
    for window in [5,30]:
        # rolling Max to get to calculate MMD using the closing Price
        roll_max = df_closePrice[c].rolling(window, min_periods=1).max()

        daily_drawdown = df_closePrice[c] / roll_max - 1

        max_daily_drawdown = daily_drawdown.min()
        col1 = 'MMD_' + str(window) + 'D'
        df_indicators.loc[c,col1] = max_daily_drawdown

# print(df_indicators)
display(df_indicators)
