import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

PATH = os.getcwd() + '/chromedriver'

driver = webdriver.Chrome(PATH)

driver.get('https://www.centris.ca/en/properties~for-sale?view=Thumbnail')

try:
    input_area = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "select2-search__field"))
    )
    input_area.send_keys('Montreal')
    input_area.send_keys(Keys.RETURN)

    time.sleep(2)
    
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "select2-results__option"))
    )
    element.click()

    time.sleep(1)

    all_info = driver.find_elements_by_class_name("shell")
    category = driver.find_elements_by_class_name("category")
    address = driver.find_elements_by_class_name("address")
    price = driver.find_elements_by_class_name("price")

    for i in range(len(price)):
        line = 'Price: {}, Category {}, address: {}'.format(price[i].text, category[i].text, address[i].text)
        print('#', i, line, '\n\n')

    n = 11
    while True:
        time.sleep(2)
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "goLast"))
        )
        element.click()
        time.sleep(2)

        all_info = driver.find_elements_by_class_name("shell")
        category = driver.find_elements_by_class_name("category")
        address = driver.find_elements_by_class_name("address")
        price = driver.find_elements_by_class_name("price")
        for i in range(len(price)):
            line = 'Price: {}, Category {}, address: {}'.format(price[i].text, category[i].text, address[i].text)
            n += 1
            print('#', n, line, '\n\n')

except:
    print('something went wrong..')
finally:
    print('sss')
