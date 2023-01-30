import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotVisibleException, StaleElementReferenceException
import platform
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup

import requests
import urllib

def init_browser():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    return browser

def run(link_crawl):
    data = []
    browser = init_browser()
    for j in range(24):
        print("Run page: ",j+1)
        item = []
        browser.get(link_crawl+'&start='+str(j)+'0')
        links = browser.find_elements(By.CLASS_NAME, 'css-1m051bw')
        for i in links:
            item.append(i.get_attribute('href'))
        data.extend(item)
    return data
def run_and_save_data(link_crawl, file_name):
    data = run(link_crawl)
    print(len(data))
    result = [i for n, i in enumerate(data) if i not in data[:n]]
    print(len(result))
    file = open(file_name+'.txt', 'w', encoding='utf-8')
    for i in result:
        file.write(i+'\n')
    file.close()

run_and_save_data('https://www.yelp.com/search?find_desc=Restaurants&find_loc=Queens%2C+NY%2C+United+States','yelp')