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

# datetime logic
import datetime

from sklearn.utils.sparsefuncs import min_max_axis

'''
# Show all columns and display 2 d.p.
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', '{:.2f}'.format)
'''

# static info
crypto_arr = ['BTC-USD', 'ETH-USD', 'XRP-USD']
index_arr = ['GC=F', 'GD=F', '^GSPC']  # gold, comdty index, SP
start_date = '2015-08-01'
end_date = '2024-08-31'

# yfinance
df = yf.download(crypto_arr, start=start_date, end=end_date)
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
graph_1 = plot_movement(df_closePrice.copy(), 'Price Movement')
graph_2 = plot_movement(df_volume.copy(), 'Volume')

# Display both graphs
graph_1.show()
graph_2.show()

# X_std = (X-X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
# X_scaled = X_std * (max - min) + min

min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 100))
scaled = min_max_scaler.fit_transform(df_closePrice)
df_closePrice_scaled = pd.DataFrame(scaled, columns=df_closePrice.columns)

