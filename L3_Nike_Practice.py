import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import requests as r
from bs4 import BeautifulSoup as bs
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager  # install the driver
from selenium.webdriver.chrome.service import Service as ChromeService  # config the driver

'''
url2 = r'https://www.nike.com.hk/fa24midonm_md/list.htm?intpromo=PETP'
html_nike2 = r.get(url2)
html_nike2_bs = bs(html_nike2.content, 'html.parser')
# print(html_nike2_bs)
nike2_bs_product = html_nike2_bs.find_all('dl', {"class": "product_list_hover"})
print(nike2_bs_product)
'''

# install the browser driver
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get(r'https://www.nike.com.hk/fa24midonm_md/list.htm?intpromo=PETP')
SCROLL_PAUSE_TIME = 5  # no. of seconds it shall wait for the internet to load just in case

last_height = driver.execute_script("return document.body.scrollHeight")  # measure the height of HTML body in pixel
# print(driver.execute_script("return document.body.scrollHeight"))

while True:  # infinite loop scrolling til the end
    print(last_height)
    # scroll down as height
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    # wait
    time.sleep(SCROLL_PAUSE_TIME)
    # find new height
    new_height = driver.execute_script('return document.body.scrollHeight')
    # to stop
    if new_height == last_height:  # comparing
        break
    last_height = new_height  # overriding the height value

html_nike3_bs = bs(driver.page_source, 'html.parser')


