import yfinance as yf

import pandas as pd
import numpy as np
import math

from jinja2.utils import urlize
from numpy import number
from scipy.stats import norm  # standardising
from sklearn import preprocessing

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

# Set default renderer to browser
pio.renderers.default = 'browser'

import datetime

import json
import requests as r
from bs4 import BeautifulSoup as bs
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager  # install the driver
from selenium.webdriver.chrome.service import Service as ChromeService  # config the driver

pd.set_option('display.max_columns', None)

import nltk

nltk.downloader.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Initialize the Chrome driver
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

agent_info = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

finviz_url = 'https://finviz.com/quote.ashx?t='

tickers = ['TSLA', 'AAPL']

news_tables = {}

for t in tickers:
    print(t)
    t_content = r.get(finviz_url + t, headers=agent_info).content
    content_bs = bs(t_content, 'html.parser')
    news_tab = content_bs.find(id="news-table")
    news_tables[t] = news_tab
    print('--' * 10)

# print(content_bs.prettify(formatter="html"))
# print(news_tables['RIVN'].find('tr'))
# news_tables['RIVN'].findAll('tr')

table_array = []
news_table = []

for name, news_table in news_tables.items():
    print(name)

    for x in news_table.findAll('tr'):
        # headline
        text_content = x.a.get_text()
        # print(text_content)
        # print('--' * 10)
        # time
        date_content = x.td.text.split()
        # print(date_content)
        # print('--' * 10)

        if len(date_content) == 1:
            time = date_content[0]
        elif len(date_content) == 2:
            date = date_content[0]
            time = date_content[1]

        table_array.append([name, date, time, text_content])

table_news = pd.DataFrame(table_array, columns=['Ticker', 'Date', 'Time', 'Headline'])

table_news['Date'] = np.where(table_news['Date'] == 'Today', datetime.date.today(), table_news['Date'])

table_news['Date'] = pd.to_datetime(table_news['Date']).dt.date

print(table_news.head(10))

print(table_news['Date'][0])

# NLTK
# Initialize the SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

# text_results = analyzer.polarity_scores('where will rivian be in 5 years')
# compound is the weighted average between -1 to +1
# print(text_results)

sentiment_output = table_news['Headline'].apply(analyzer.polarity_scores).tolist()
sentiment_df = pd.DataFrame(sentiment_output)
table_news1 = table_news.join(sentiment_df[['compound']])

# print(sentiment_df.head(),table_news1.head())
# table_news1.groupby(['Ticker','Date']).mean().unstack().index
# print(table_news1.groupby(['Ticker','Date']).mean().unstack().column)

# table_news2 = table_news1.groupby(['Ticker','Date']).mean(numeric_only=True).unstack().xs("compound",axis='columns').transpose()

# Step 1: Group by 'Ticker' and 'Date'
grouped = table_news1.groupby(['Ticker', 'Date'])

# Step 2: Calculate the mean of numeric columns within each group
mean_grouped = grouped.mean(numeric_only=True)

# Step 3: Unstack the 'Date' level of the index to columns
unstacked = mean_grouped.unstack()

# Step 4: Extract the 'compound' column
compound_column = unstacked.xs('compound', axis=1)

# Step 5: Transpose the DataFrame
table_news2 = compound_column.transpose()

# Print the table
print(table_news2)

# Set the figure size for the plot
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = (20, 6)

# Plot the data in a bar chart
table_news2.plot(kind='bar')

# Display the plot
plt.show()

# L5 starts here
# install tensorflow, pytorch, tf-keras and so install hugging-face's transformers

# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("text-classification", model="mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")

var = pipe('tesla is an EV name')[0]

sent_df = pd.DataFrame(table_news['Headline'].apply(pipe).tolist())

print(sent_df.head())

x = {'label': 'neutral', 'score': 0.999}
# print(x['score'])

def process_score(x):
    global score
    if x['label'] == 'neutral':score = 0
    elif x['label'] == 'positive':score = x['score']
    elif x['label'] == 'negative':score = -1 * x['score']
    return score

# test = {'label':'abcd','score':0.999)
# process_score(test)

sent_series = sent_df[0].apply(process_score)
print(sent_series.head(10))

table_news_1 = table_news.join(sent_series)
print(table_news_1.head(10))

table_news_2 = table_news_1.groupby(['Ticker', 'Date']).mean(numeric_only=True).unstack().xs(0,axis='columns').transpose()
print(table_news_2)

apple_price = yf.download('AAPL', start = '2024-09-30', end = '2024-10-05')
print(apple_price['Adj Close'])

fig, ax1 = plt.subplots(figsize=(20, 10))
l1, = ax1.plot(apple_price.index, apple_price['Adj Close'],label='Apple Adj Close', color = 'red')

ax2 = ax1.twinx()
ax2.bar(table_news_2.index, table_news_2['AAPL'], color='grey')

plt.show()
