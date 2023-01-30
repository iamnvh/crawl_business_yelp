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

def run():
    browser = init_browser()
    browser.get('https://www.tripadvisor.com/Restaurant_Review-g60763-d7716799-Reviews-Frisson_Espresso-New_York_City_New_York.html')
    
    # html_page = requests.get('').content
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    data = []
    name = soup.find("h1", class_='HjBfq').text
    # rating = float(soup.find("svg", class_="UctUV d H0")['aria-label'].split(" ")[0].strip())
    # rank = soup.find_all("span", class_="DsyBj cNFrA")[0].text
    address = soup.find_all("span", class_="DsyBj cNFrA")[1].text
    contact = soup.find_all("span", class_="DsyBj cNFrA")[2].text
    thummb = soup.find_all("img", class_="basicImg")[0]['data-lazyurl']
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    gg = browser.find_element(By.CSS_SELECTOR, '#taplc_resp_hr_nearby_rr_responsive_0 > div > div.ui_columns.neighborhood > div > div > img').get
    data.append({
        "businessName": name,
        "businessType":None,
        "geolocation": gg,
        # "rating": rating,
        # "rank": rank,
        "businessAddress": address,
        "phoneNumber": contact,
        "businessHours": None,
        "thumbnailUrl": thummb,
    })
    print(data)

run()


