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

a = 0
while a == 1:  # infinite loop scrolling til the end
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
# print(html_nike3_bs.findAll('dl', {"class": "product_list_hover"})[-1])
# print(len(html_nike3_bs.findAll('dl', {"class": "product_list_hover"})))

# single and double quotation marks are different here!!
# this is xPath from HTML inspect
# because the xPath uses double quotes so we need to use correct it with single quote inside and make it a string
# double quotes usually enclosure single quotes, convention is that double quotes on the outer layer, because of hirearchy
path_input = "//*[@id='keyword']"
path_input_cross = '/html/body/div[28]/span/img'
time.sleep(10)

driver.find_element('xpath', path_input_cross).click()

# click on the input box on webpage
driver.find_element('xpath', path_input).click()
time.sleep(2)

#clear on the input box
driver.find_element('xpath', path_input).clear()
time.sleep(2)

# key in info
driver.find_element('xpath', path_input).send_keys('Nike Victori')
time.sleep(2)

# click on enter
driver.find_element('xpath', path_input).send_keys(Keys.ENTER)
time.sleep(2)