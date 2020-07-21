import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import json

def isLastPage(currentPage):
    x = currentPage
    current = x[:(x.find('/')-1)]
    last = x[(x.find('/'))+2 : len(x)]
    return current == last

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
    n = 0

    while True:
        time.sleep(2)
        all_info = driver.find_elements_by_class_name("shell")
        category = driver.find_elements_by_class_name("category")
        address = driver.find_elements_by_class_name("address")
        price = driver.find_elements_by_class_name("price")
        pages = driver.find_elements_by_class_name("pager-current")

        x = pages[0].text
        for i in range(len(price)):
            line = ', Price: {}, Category {}, address: {}'.format(price[i].text, category[i].text, address[i].text)
            line.replace('\n', ' ')
            n += 1
            print('#', n, line, '\n\n')
            
            data.append({
                'price': price[i].text,
                'category': category[i].text,
                'address': address[i].text
            })
        pages = [int(s) for s in x.split() if s.isdigit()]
        currentPage, lastPage = pages[0], pages[1]

        time.sleep(1)
        time_left = round(((lastPage-currentPage)*5/60), 2)
        seconds = int((time_left%1)*60)
        if seconds/10 < 1:
            seconds = '0' + str(seconds)
        mins =  int(time_left)
        time_left = str(mins) + ':' + str(seconds)

        print(x, 'pages completed. ETA: ', time_left, 'mins')
        time.sleep(1)
        if currentPage == lastPage:
            break

        element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "next"))
        )
        element.click()
        time.sleep(1)

except:
    print('something went wrong..')
finally:
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)
    print('DONE!')
    driver.quit()
