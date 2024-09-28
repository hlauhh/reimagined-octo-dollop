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

tickers = ['TSLA', 'RIVN']

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
        print(text_content)
        print('--' * 10)
        # time
        date_content = x.td.text.split()
        print(date_content)
        print('--' * 10)

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
