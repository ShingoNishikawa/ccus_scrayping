from selenium import webdriver
from selenium.webdriver.support.ui import Select
from time import sleep
import csv

def RunScrayping(areaName):
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get('https://www.mobile.ccus.jp/#/open_jigyousya_search')

    radioElement=driver.find_element_by_xpath('/html/body/ng-component/div[2]/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/span[2]/label/input')
    radioElement.click()
    sleep(3)

    praceElement = driver.find_element_by_xpath('/html/body/ng-component/div[2]/div/div/div[1]/div/div[2]/fieldset/div[1]/div[2]/div/select')
    praceSelectElement = Select(praceElement)
    praceSelectElement.select_by_visible_text(areaName)

    sleep(5)

    serchElement = driver.find_element_by_xpath('/html/body/ng-component/div[2]/div/div/div[2]/div/div/app-button[1]/button')
    serchElement.click()
    sleep(3)

    getData = []

    while True:

        trElements = driver.find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
        for trElement in trElements:
            print(trElement.text.split('\n'))
            with open('{}.csv'.format(areaName), 'a',encoding='shift_jis',newline="") as ff:
                writer = csv.writer(ff)
                writer.writerow(trElement.text.split('\n'))
                getData.append(trElement.text.split('\n'))

        nextPageLink = driver.find_element_by_class_name('pagination-next')

        if 'disabled' in nextPageLink.get_attribute("class"):
            break

        print('次のPageを取得します。')
        
        nextPageLink.click()
        sleep(5)

    with open('{}_bulkcreate.csv'.format(areaName), 'w',encoding='shift_jis',newline="") as f:
        writer = csv.writer(f)
        writer.writerows(getData)
    
    return

areas = ["京都府","滋賀県","和歌山県","兵庫県"]
for area in areas:
    RunScrayping(area)