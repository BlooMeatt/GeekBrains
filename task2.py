from selenium import webdriver
from selenium.webdriver.common.by import By
from pymongo import MongoClient
import time

client = MongoClient('127.0.0.1', 27017)
client.drop_database('Mvideo_Trends')
db = client['Mvideo_Trends']
collection = db.trends

url = 'https://www.mvideo.ru'

driver = webdriver.Chrome(executable_path='./chromedriver.exe')
driver.get(url)

# Хотел реализовать через wait.until,то не до конца разобрался как он работает
time.sleep(3)

# close_popup = driver.find_element_by_xpath('//mvid-icon[contains(@class,"modal-layout__close ng-tns-c72-1 ng-star-inserted")]')
# close_popup.click()


# Страница подгружается динамически по мере прокрутки
driver.execute_script("window.scrollTo(0,1500)")

time.sleep(3)

button = driver.find_element(By.XPATH, '//button[contains(@class,"tab-button ng-star-inserted")]')
button.click()

time.sleep(3)

while True:
    try:
        button = driver.find_elements(By.XPATH,'//mvid-shelf-group/*//button[contains(@class, "btn forward")]/mvid-icon[@type = "chevron_right"]')
        button.click()
        time.sleep(3)
    except:
        break

item_names = driver.find_elements(By.XPATH,
                                  '//mvid-shelf-group/*//div[@class = "product-mini-card__name ng-star-inserted"]')
item_prices = driver.find_elements(By.XPATH,
                                   '//mvid-shelf-group/*//div[@class = "product-mini-card__price ng-star-inserted"]/*//span[@class= "price__main-value"]')
trends_list = []
for i in range(len(item_names)):
    item_list = {}
    name = item_names[i].find_element(By.TAG_NAME, "a").text
    link = item_names[i].find_element(By.TAG_NAME, "a").get_attribute("href")
    price = item_prices[i].text
    item_list['Name'] = name
    item_list['URL'] = link
    item_list['Price'] = price
    trends_list.append(item_list)

collection.insert_many(trends_list)

driver.close()
