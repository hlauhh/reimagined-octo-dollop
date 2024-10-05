import pandas as pd
import os
from pathlib import Path
from datatime import time
import matplotlib.pyplot as plt
import plotly.graph_objects as go

contract1_path = Path()
'''
CSI 500 Futures Demo
http://www.cffex.com.cn/en_new/CSI300IndexFutures.html
Calendar spread on current month vs next month

IC2307
After joining two month’s dataframes, outer join
spread_df.dropna(); reset_index(); 

Dealing with Bid / Ask Spreads
'''
spread_df= pd.DataFrame()

spread_df[‘spread_ask’] = spread_df[‘ask_price_1_x’] - spread_df[‘bid_price_1_y’]
spread_df[‘spread_bid’] = spread_df[‘bid_price_1_x’] - spread_df[‘ask_price_1_y’]
spread_df[‘spread_mid’] = (spread_df[‘spread_ask’] - spread_df[‘spread_bid’])/2

spread_df[‘spread_ma’] = spread_df[‘spread_mid’].rolling(120).mean()
spread_df[‘spread_uppper’] = spread_df[‘spread_ma’]+1 # +1 CNH here, but could be std better
spread_df[‘spread_lower’] = spread_df[‘spread_ma’]-1 # samething here

# correlation
np.corrcoef(spread_df['last_price_x'], spread_df['last_price_y'])[0,1]

print(spread_df.shape())

#Trimming the timeframe for showing
spread_df_1 = spread_df.iloc[12400:12600]

# plotting July Contract bid ask spread _x means July
ask = go.Scatter(y=spread_df_1['ask_price_1_x'] name='ask', mode='lines')
bid = go.Scatter(y=spread_df_1['bid_price_1_x'] name='bid', mode='lines')
last = go.Scatter(y=spread_df_1['last_price_1_x'] name='last', mode='lines')
fig1 = go.Figure(layout = go.Layout(title = 'Contract Tick Plot July', data=[ask, bid, last])
fig1.show()

# plotting Sept Contract bid ask spread _y means Sept
ask = go.Scatter(y=spread_df_1['ask_price_1_y'] name='ask', mode='lines')
bid = go.Scatter(y=spread_df_1['bid_price_1_y'] name='bid', mode='lines')
last = go.Scatter(y=spread_df_1['last_price_1_y'] name='last', mode='lines')
fig2 = go.Figure(layout = go.Layout(title = 'Contract Tick Plot Sept', data=[ask, bid, last])
fig2.show()

# plotting +1/-1 CNH over bid ask spread
ask = go.Scatter(y=spread_df_1['spread_ask'] name='ask', mode='lines')
bid = go.Scatter(y=spread_df_1['spread_bid'] name='bid', mode='lines')
ma = go.Scatter(y=spread_df_1['spread_ma'] name='bid', mode='lines')
upper = go.Scatter(y=spread_df_1['spread_upper'] name='upper', mode='lines')
lower = go.Scatter(y=spread_df_1['spread_lower'] name='lower', mode='lines')
fig3 = go.Figure(layout = go.Layout(title = 'Contract Tick Ploty July', data=[ask, bid, last])
fig3.show()

# defining signal, you can only long the asking price, and only short the bid.
# only buy when asking is lower than the lower band
spread_df_1['buy_signal'] = spread_df_1['spread_ask'] < spread_df_1['spread_lower']
spread_df_1['short_signal'] = spread_df_1['spread_bid'] > spread_df_1['spread_upper']

# defining signal the other side. But trigger when reaching average.
# can't do bid price
spread_df_1['buy_signal'] = spread_df_1['spread_bid'] > spread_df_1['spread_ma']
spread_df_1['cover_signal'] = spread_df_1['spread_ask'] < spread_df_1['spread_ma']

# backtesting
position = 0

long_trades = []
short_trades = []

# signals
# long_trade_signals = []
# short_trade_signals = []
'''
for tick in spread_df_1.itertuples():
    print(tick)
    break
'''

for tick in spread_df_1.itertuples():
    if tick.datetime.time() > time(14,55):
        if position > 0:
            short_trades.append({'datetime':tick.datetime, 'price':tick.spread_bid})
            position -= 1
        elif position < 0:
            long_trades.append({'datetime':tick.datetime, 'price':tick.spread_ask})
            position += 1
    if position == 0:
        if tick.buy_signal:
            long_trades.append({'datetime':tick.datetime, 'price':tick.spread_ask})
            position += 1
        elif position > 0:
            long_trades.append({'datetime': tick.datetime, 'price': tick.spread_ask})
            position += 1
    if position < 0:
        if tick.buy_signal:
            long_trades.append({'datetime': tick.datetime, 'price': tick.spread_ask})
            position += 1
        elif position > 0:
            long_trades.append({'datetime': tick.datetime, 'price': tick.spread_ask})
        position += 1


long_df = pd.DataFrame(long_trades, columns=['long_datetime', 'long_price'])
short_df = pd.DataFrame(short_trades, columns=['short_datetime', 'short_price'])

result_df = pd.concat([long_df, short_df], axis=1)

# this is doing a calendar spread on +1 or -1 CNH with the average of 120 ticks between July and Spet of CSI500

