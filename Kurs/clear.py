import csv
import sys
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver


url = "https://valion.ua/navigation/prodazha-kvartir-v-kieve/?city=kiev&current_page="
driver = webdriver.Chrome('C:/Users/vladi/Desktop/chromedriver_win32/chromedriver.exe')

csvFile = open("result.csv", "w")
csvAttributes = "href,city,buildingType,district,microDistrict,street,buildNumber,rooms,metro,fullSquare,livingSquare,kitchenSquare,floor,floorCount,price"
csvFile.write(csvAttributes)
hrefsFile = open("hrefs.txt", "r")
start_time = datetime.now()
hrefs = hrefsFile.read().split('\n')
for href in hrefs:
    try:
        driver.get(href)
        print(href, datetime.now() - start_time)
        html = driver.page_source
        soup = BeautifulSoup(html.replace('  ', '').replace('\n', ''))
        attributeList = soup.find('ul', {'class': 'mh-estate__list__inner'})
        city = attributeList.find('li', {'id': 'mh-estate_attribute--3'}).contents[1]
        buildingType = attributeList.find('li', {'id': 'mh-estate_attribute--14'}).contents[1]
        district = attributeList.find('li', {'id': 'mh-estate_attribute--15'}).contents[1]
        microDistrict_attr = attributeList.find('li', {'id': 'mh-estate_attribute--36'})
        microDistrict = microDistrict_attr.contents[1] if microDistrict_attr is not None else "None"
        street = attributeList.find('li', {'id': 'mh-estate_attribute--18'}).contents[1]
        buildNumber = attributeList.find('li', {'id': 'mh-estate_attribute--12'}).contents[1]
        rooms = attributeList.find('li', {'id': 'mh-estate_attribute--20'}).contents[1]
        metro_attr = attributeList.find('li', {'id': 'mh-estate_attribute--16'})
        metro = metro_attr.contents[1] if metro_attr is not None else "None"
        floor = attributeList.find('li', {'id': 'mh-estate_attribute--23'}).contents[1]
        floorCount = attributeList.find('li', {'id': 'mh-estate_attribute--24'}).contents[1]
        price = soup.find('div', {'class': 'mh-estate__details__price__single'}).contents[0]

        list_attr = [href, city, buildingType, district, microDistrict, street, buildNumber, rooms, metro, floor, floorCount, price]
        csvFile.write("\n" + ','.join(list_attr))
        start_time = datetime.now()
    except :
        print("Something went wrong why reading: " + href)