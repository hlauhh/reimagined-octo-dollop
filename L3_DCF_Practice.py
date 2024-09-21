# retrieve data
import yfinance as yf

# process data
import pandas as pd
import numpy as np
import math
from scipy.stats import norm
from sklearn import preprocessing

# plotting data
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# datetime logic
import datetime

# Show all columns
pd.set_option('display.max_columns', None)

# static info
crypto_arr = ['BTC-USD','ETH-USD','XRP-USD']
index_arr = ['GC=F','GD=F','^GSPC'] # gold, comdty index, SP
start_date = '2015-08-01'
end_date = '2024-08-31'

# yfinance
df = yf.download(crypto_arr, start=start_date, end=end_date)
df1 = yf.download(crypto_arr+index_arr, start=start_date, end=end_date, group_by='ticker')
# print(df.head())

print(crypto_arr+index_arr)

# extracting the adjusted close price from df
dict_closePrice = {}
for name in crypto_arr+index_arr:
    dict_closePrice[name] = df1[name]['Adj Close']
df_closePrice = pd.DataFrame(dict_closePrice)
# print(df_closePrice.head())

dict_volume = {}
for name in crypto_arr+index_arr:
    dict_volume[name] = df1[name]['Volume']
df_volume = pd.DataFrame(dict_volume)
# print(df_volume.head())
print(df_closePrice.describe())
print(df_volume.describe())

