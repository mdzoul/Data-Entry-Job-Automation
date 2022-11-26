import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

GOOGLE_FORM_URL = 'https://forms.gle/F9nGavN5kGa87qRX8'
ZILLOW_URL = 'https://www.zillow.com/san-francisco-ca/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C' \
             '%22usersSearchTerm%22%3A%22Singapore%20Dunes%20Way%20%237%20Saugatuck%2C%20MI%2049453%22%2C%22mapBounds' \
             '%22%3A%7B%22north%22%3A37.86058820332192%2C%22east%22%3A-122.31488314990234%2C%22south%22%3A37' \
             '.68989718250557%2C%22west%22%3A-122.55177585009766%7D%2C%22mapZoom%22%3A12%2C%22regionSelection%22%3A' \
             '%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState' \
             '%22%3A%7B%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22ah%22%3A%7B' \
             '%22value%22%3Atrue%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C' \
             '%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value' \
             '%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D '
HEADER = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/107.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

response = requests.get(url=ZILLOW_URL, headers=HEADER)
website = response.text

soup = BeautifulSoup(website, 'html.parser')
# print(soup.prettify())

link_list = []
property_links = soup.find_all(name='a', class_='property-card-link', href=True)
for link in property_links:
    if f'https://www.zillow.com{link["href"]}' not in link_list:
        link_list.append(f'https://www.zillow.com{link["href"]}')
    else:
        pass
# print(link_list)

name_list = []
address_list = []
name_address = soup.find_all(name='a', class_='property-card-link')
for address in name_address:
    if address.text != '':
        address_list.append(address.text.split(' | ')[1])
        name_list.append(address.text.split(' | ')[0])
# print(address_list)
# print(name_list)

price_list = []
prices = soup.select('[data-test="property-card-price"]')
for price in prices:
    price_list.append(price.text.split('+')[0])
# print(price_list)

s = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options, service=s)
driver.maximize_window()

for i in range(len(link_list)):
    driver.get(GOOGLE_FORM_URL)

    time.sleep(3)
    property_name = driver.find_element(By.CSS_SELECTOR, '[aria-labelledby="i1"]')
    property_address = driver.find_element(By.CSS_SELECTOR, '[aria-labelledby="i5"]')
    property_price = driver.find_element(By.CSS_SELECTOR, '[aria-labelledby="i9"]')
    property_link = driver.find_element(By.CSS_SELECTOR, '[aria-labelledby="i13"]')

    property_name.send_keys(name_list[i])
    property_address.send_keys(address_list[i])
    property_price.send_keys(price_list[i])
    property_link.send_keys(link_list[i])
    driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div').click()
    driver.find_element(By.LINK_TEXT, 'Submit another response').click()
