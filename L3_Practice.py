## HK Housing Authority Scrap

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests as r
from bs4 import BeautifulSoup as bs
import json

# because this web page doesn't load all the content in table on frontend HTML
# we need to load the json from the HTML

url = r'https://www.housingauthority.gov.hk/json/transaction-record/byMonth/2024/08.json?_=1726886941590'
html_hos = r.get(url)
hos_json = json.loads(html_hos.content)

# checking position
# print(hos_json)
# print(hos_json[1])
# html_hos_bs = bs(html_hos.content, 'html.parser')
# print(html_hos_bs)

# To peel the JSON onion and get to the data
print(hos_json[0]['district'][0]['location'][0]['location'][0])
# if result is a list, you need to specific the location of list, use [0] to get the first item in list
# the key is the term before the colon : in JSON
print(hos_json[0]['district'][0]['location'][0]['location'][0].keys())
# print(hos_json[0]['district'][0].keys()) # get keys from dictionary

