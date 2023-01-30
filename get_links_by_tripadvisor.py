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

def init_browser():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    return browser


def run(link, count_run):
    browser = init_browser()
    browser.get(link)
    time.sleep(20)
    data = []
    for i in range(count_run):
        links = []
        for j in range(40):
            try:
                elems = browser.find_element(By.CSS_SELECTOR,'#component_2 > div > div:nth-child('+str(j+2)+') > div > span > div.zqsLh > div._T > span:nth-child(2) > a').get_attribute('href')
                links.append(elems)
                print(j, elems)
                continue
            except: pass
            try:
                elems = browser.find_element(By.CSS_SELECTOR,'#component_2 > div > div:nth-child('+str(j+2)+') > div > span > div.zqsLh > div._T > span > a').get_attribute('href')
                links.append(elems)
                print(j, elems)
            except: pass
        print('Số link get được: ',len(links))
        data.extend(links)
        element = 5
        if i <= 5:
            element = i
        browser.find_element(By.CSS_SELECTOR, '#EATERY_LIST_CONTENTS > div.deckTools.btm > div > div > a:nth-child('+str(element+2)+')').send_keys(Keys.ENTER)
        time.sleep(5)
    return data

def run_and_save_data(link_crawl, count_run, file_name):
    data = run(link_crawl, count_run)
    file = open(file_name+'.txt', 'a', encoding='utf-8')
    for i in data:
        file.write(i+'\n')
    file.close()


run_and_save_data('https://www.tripadvisor.com/RestaurantSearch-g60763-a_geobroaden.false-New_York_City_New_York.html#EATERY_LIST_CONTENTS',2,'data')


