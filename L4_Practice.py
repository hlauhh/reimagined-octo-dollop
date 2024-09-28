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

from L3_Nike_Practice import SCROLL_PAUSE_TIME

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

import nltk

nltk.downloader.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Start from here

# Initialize the Chrome driver
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Finviz URL for Ticker (RIVN)
finviz_url = 'https://finviz.com/quote.ashx?t=RIVN'
driver.get(finviz_url)
time.sleep(2)

# Get the page source and parse it with BeautifulSoup
html_finviz_text = driver.page_source
soup = bs(html_finviz_text, 'html.parser')

# Locate the news table on the page
news_table = soup.find('table', id='news-table')

# Initialize lists to store the scraped data
news_time = []
news_headlines = []
news_links = []
news_sources = []

# Loop through each row of the news table and extract time, headline, and link
for row in news_table.findAll('tr'):
    # Extract the time (it could be split across rows if there's no date)
    time_text = row.td.text.strip()

    # Extract the headline and its link
    headline_data = row.find_all('td')[1].find('div', class_='news-link-left')
    if headline_data:
        headline = headline_data.a.text.strip()  # Headline text
        link = headline_data.a['href']  # News link

        # Check if there's a source (it is sometimes attached to the headline div)
        source = row.find('div', class_='news-link-right')
        source_text = source.text.strip() if source else 'N/A'  # Extract source if available

        # Append extracted data to the lists
        news_time.append(time_text)
        news_headlines.append(headline)
        news_links.append(link)
        news_sources.append(source_text)

# Create a DataFrame to organize the scraped news data
df_news = pd.DataFrame({
    'Time': news_time,
    'Headline': news_headlines,
    'Link': news_links,
    'Source': news_sources
})

# Display the DataFrame
import ace_tools as tools;

tools.display_dataframe_to_user(name="Tesla News Data", dataframe=df_news)

# Close the Selenium driver
driver.quit()
