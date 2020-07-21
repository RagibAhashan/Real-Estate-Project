import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def isLastPage(currentPage):
    x = currentPage
    current = x[:(x.find('/')-1)]
    last = x[(x.find('/'))+2 : len(x)]
    return current == last

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
    n = 0
    while True:
        time.sleep(1)
        all_info = driver.find_elements_by_class_name("shell")
        category = driver.find_elements_by_class_name("category")
        address = driver.find_elements_by_class_name("address")
        price = driver.find_elements_by_class_name("price")
        pages = driver.find_elements_by_class_name("pager-current")
        time.sleep(1)
        x = pages[0].text
        for i in range(len(price)):
            line = ', Price: {}, Category {}, address: {}'.format(price[i].text, category[i].text, address[i].text)
            n += 1
            print('#', n, line, '\n\n')
        currentPage = [int(s) for s in x.split() if s.isdigit()]
        time.sleep(1)

        print(x, 'pages completed. ETA: ', "{:.0f".format(currentPage[1]*5/60), 'mins')
        time.sleep(1)
        if currentPage[0] == currentPage[1]:
            break

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "next"))
        )
        element.click()
        time.sleep(1)



except:
    print('something went wrong..')
finally:
    print('DONE!')
    driver.quit()
