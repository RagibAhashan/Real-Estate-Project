import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import json
from bs4 import BeautifulSoup


PATH = os.getcwd() + '/chromedriver'
driver = webdriver.Chrome(PATH)
driver.get('https://www.centris.ca/en/properties~for-sale?view=Thumbnail')
data = []

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

    time.sleep(2)

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "filter-search"))
    )
    element.click()
    #PropertyTypeSection-accordion
    time.sleep(2)

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "PropertyTypeSection-accordion"))
    )
    element.click()

    select_boxes = ['Single-family home', 'Condo', 'Loft / Studio', 'Plex', 'Intergenerational']

    check_boxes = driver.find_elements_by_class_name("custom-control-label")
    time.sleep(1)
    for box in check_boxes:
        if box.text in select_boxes:
            box.click()
    
    time.sleep(2)

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "property-count"))
    )
    element.click()

    time.sleep(3)
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ButtonViewSummary"))
    )
    element.click()
    time.sleep(2)
    n = 0

    # category = driver.find_elements_by_class_name("category")
    # address  = driver.find_elements_by_class_name("address")

    title_address    = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "address"))
    )
    price    = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "BuyPrice"))
    )
    pages    = driver.find_elements_by_class_name("pager-current")

    # description    = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, "row teaser")) 
    # )
    # description2    = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, "row")) 
    # )
    time.sleep(1)
    title, address = title_address.text.split('\n')[0], title_address.text.split('\n')[1]

    print(title)
    print(address)
    print(price.text)
    print(pages[0].text)
    # print(driver.page_source)
    f = open("index.html", "a")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    divs = soup.findAll('div', {"class" : "row"})
    f.write(divs)
    f.close()
    # print(description)
    # print(description2)

except:
    print('something went wrong..')
finally:
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)
    print('DONE!')
    # driver.quit()
