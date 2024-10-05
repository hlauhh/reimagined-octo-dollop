# 1. Simple Trading Strategy

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

# for ipynb can add
# %matplotlib inline
import warnings as w
w.filterwarnings('ignore')
from ta import add_all_ta_features
from ta.utils import dropna
pd.set_option('display.max_columns', None)


df = yf.download('PDD', start='2020-01-01', end='2024-10-04')
# print(df.head())

df_ta = df.copy() # referencing to isolate the impact from the original dataset
df_ta = add_all_ta_features(df_ta, open="Open", high="High", low="Low", close="Close", volume="Volume", fillna=True)
# print(df_ta.head())

# to search for an indicator
'''
for c in df_ta.columns:
    # print(c)
    if "RSI" in c.upper():
        print(c)
'''

from ta.volatility import BollingerBands

# Clean NaN values
# df_ta = dropna(df_ta)

# Initialize Bollinger Bands Indicator
indicator_bb = BollingerBands(close=df_ta["Close"], window=20, window_dev=2)

# Add Bollinger Bands features
df_ta['bb_bbm'] = indicator_bb.bollinger_mavg()
df_ta['bb_bbh'] = indicator_bb.bollinger_hband()
df_ta['bb_bbl'] = indicator_bb.bollinger_lband()

# Add Bollinger Band high indicator
df_ta['bb_bbhi'] = indicator_bb.bollinger_hband_indicator()

# Add Bollinger Band low indicator
df_ta['bb_bbli'] = indicator_bb.bollinger_lband_indicator()

df_ta = df_ta[~df_ta['bb_bbm'].isnull()]
# or
# df_ta = df_ta[df_ta['bb_bbm'].isnull()].reset_index(drop=True)
# doing positive extraction instead of negation and/or choosing to reset index

print(df_ta.head())

print(df_ta[['Open']])

df_ta.iloc[-500:][['Close','bb_bbm','bb_bbh','bb_bbl']].plot(figsize=(30,20))
# plt.show()

# note that some breakout work some don't
# and some mean reversion work some don't
# on bbh and bbl

# Long Short Window
short_window = 20
long_window = 100

signals = pd.DataFrame(index = df_ta.index)
signals['signal'] = 0
# print(signals.head())

# moving average
signals['short_mavg'] = df_ta['Adj Close'].rolling(window=short_window, min_periods=1, center=False).mean()
signals['long_mavg'] = df_ta['Adj Close'].rolling(window=long_window, min_periods=1, center=False).mean()

# print(signals.tail())

# create the signal of golden cross when 20 days go passthrough 100 days mavg, using the short window of 20 day as range.
signals['signal'][short_window:] = np.where(signals['short_mavg'].iloc[short_window:] > signals['long_mavg'].iloc[short_window:], 1, 0)

print(signals[(signals.index >= '2020-09-25')&(signals.index <= '2020-10-30')])
print(signals.head(50))

# to find where we have a signal
print(signals[signals['short_mavg']> signals['long_mavg']].head())

# position
# signals['position'] = signals['signal'].shift(1)
signals['position'] = signals['signal'].diff()

fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel='Price ($)')
df_ta['Adj Close'].plot(ax=ax1, color='r', lw=2.0)
signals[['short_mavg','long_mavg']].plot(ax=ax1, lw=2.0, figsize=(20,8))

ax1.plot(signals.loc[signals.position==1].index,
         signals.short_mavg[signals.position==1],'^', markersize=10, color='y')
ax1.plot(signals.loc[signals.position==-1].index,
         signals.short_mavg[signals.position==-1],'v', markersize=10, color='g')

plt.show()

initial_capital= float(100000.0)

positions = pd.DataFrame(index= signals.index)
positions['PDD'] = 100*signals['signal']
portfolio = positions.multiply(df_ta['Adj Close'], axis=0)
pos_diff = positions.diff()
portfolio['holdings'] = positions.multiply(df_ta['Adj Close'], axis=0).sum(axis=1)
portfolio['cash'] = initial_capital - (pos_diff.multiply(df_ta['Adj Close'], axis=0)).sum(axis=1).cumsum()
portfolio['total'] = portfolio['cash'] + portfolio['holdings']
portfolio['returns'] = portfolio['total'].pct_change()

print(portfolio.head())

'''
fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel='Portfolio Value in ($)')
df_ta['Adj Close'].plot(ax=ax1, color='r', lw=2.0)
signals[['short_mavg','long_mavg']].plot(ax=ax1, lw=2.0, figsize=(20,8))

ax1.plot(signals.loc[signals.position==1].index,
         signals.short_mavg[signals.position==1],'^', markersize=10, color='y')
ax1.plot(signals.loc[signals.position==-1].index,
         signals.short_mavg[signals.position==-1],'v', markersize=10, color='g')

plt.show()
'''
# df_ta.head(2)

df_portf = pd.merge(signals, df_ta['Adj Close'], how='left', left_index=True, right_index=True)
df_return = df_portf[df_portf.position != 0]
df_return['Notional'] = df_return['position'] * df_return['Adj Close'] * -1
print(df_return.head())
