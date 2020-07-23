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
import json
import datetime


def search():
    data = []
    PATH = os.getcwd() + '/geckodriver'
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
        time.sleep(2)

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "PropertyTypeSection-accordion"))
        )
        element.click()

        select_boxes = ['Single-family home', 'Condo', 'Loft / Studio', 'Plex', 'Intergenerational']

        check_boxes = driver.find_elements_by_class_name("custom-control-label")
        time.sleep(2)
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
        data = []
        with open('new_data.json', 'w') as outfile:
                    json.dump(data, outfile)

        while True:
            try:                
                time.sleep(1)
                title_address    = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "address"))
                )
                price    = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "BuyPrice"))
                )
                pages    = driver.find_elements_by_class_name("pager-current")
                #time.sleep(1)
                title, address = title_address.text.split('\n')[0], title_address.text.split('\n')[1]

                data = []
                with open('new_data.json', 'r') as json_file:
                    data = json.load(json_file)
                
                js_data = {}
                js_data["Property"] = title
                js_data["Address"] = address
                js_data["Price"] = price.text
                js_data["URL"] = driver.current_url

                soup = BeautifulSoup(driver.page_source, 'html.parser')
                divs1 = soup.findAll('div', {"class" : "carac-title"})
                divs2 = soup.findAll('div', {"class" : "carac-value"})
                #time.sleep(1)

                # Loads data to JSON Object for appending.
                for i in range(len(divs1)):
                    js_data[str(divs1[i].get_text())] = str(divs2[i].get_text())
                data.append(js_data)

                with open('new_data.json', 'w') as outfile:
                        json.dump(data, outfile)
                n += 1
                print('#', n, js_data)

                x = str(pages[0].text).replace(',','')
                print(x)
                # Checks if current page is final page...
                pages = [int(s) for s in x.split() if s.isdigit()]
                currentPage, lastPage = pages[0], pages[1]
                time_left = round(((lastPage-currentPage)*1/60), 2)
                seconds = int((time_left%1)*60)
                if seconds/10 < 1:
                    seconds = '0' + str(seconds)
                mins =  int(time_left)
                time_left = str(mins) + ':' + str(seconds)
                print(x, 'pages completed. ETA: ', time_left, 'mins')
                #time.sleep(1)
                if currentPage == lastPage:
                    break
                #time.sleep(1)

                # Goes to next page.
                element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "next"))
                )
                element.click()
                #time.sleep(1)
            except Exception as error:
                print(error)
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.LINK_TEXT, "Close"))
                )
                element.click()
            else:
                pass


    except Exception as error:
        print(error)
        print('something went wrong..\n Restarting...')
        data = []
        with open('new_data.json', 'r') as json_file:
            data = json.load(json_file)

        with open('error_saved_{}.json'.format(datetime.datetime.now()), 'w') as outfile:
            json.dump(data, outfile)
        driver.quit()

        search()
    finally:
        driver.quit()
        print('DONE!')


if __name__ == "__main__":
    search()
