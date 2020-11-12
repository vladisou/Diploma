#!/usr/bin/python
# -*- coding: ascii -*-
import os, sys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from datetime import datetime
from selenium import webdriver
import pandas as pd
import Coordinates

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)
geolocator = Nominatim(user_agent="NeuronSystem", timeout=30)
geo = dict()


def ReadHrefsOfApartments ():
    url = "https://kiev.mesto.ua/sale/?p="

    hrefsFile = open("mesto_ua.csv.txt", "w")

    for i in range(1, 158):
        start_time = datetime.now()
        fullUrl = url + str(i)
        driver.get(fullUrl)
        html = driver.page_source
        soup = BeautifulSoup(html, features="lxml")
        flatsList = soup.findAll('a',
            {'class': 'title'})
        for item in flatsList:
            link = item.attrs['href'] + '\n'
            hrefsFile.write(link)

        print(i, str(datetime.now() - start_time))
    hrefsFile.close()
    driver.close()


def ReadDataOfApartments ():
    csvFile = open("fullDataset2.0.csv", "w")
    csvAttributes = "href,city,buildingType,district,microDistrict,street,buildNumber,rooms," \
                    "metro,fullSquare,livingSquare,kitchenSquare,floor,floorCount,price"
    csvFile.write(csvAttributes + '\n')
    hrefsFile = open("hrefs.txt", "r")

    hrefs = hrefsFile.read().split('\n')
    for href in hrefs:
        try:
            start_time = datetime.now()

            driver.get(href)
            html = driver.page_source
            soup = BeautifulSoup(html.replace('  ', '').replace('\n', ''), features="lxml")
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
            fullSquare = attributeList.find('li', {'id': 'mh-estate_attribute--7'}).contents[1].replace('??', '')
            livingSquare = attributeList.find('li', {'id': 'mh-estate_attribute--21'}).contents[1].replace('??', '')
            kitchenSquare = attributeList.find('li', {'id': 'mh-estate_attribute--22'}).contents[1].replace('??', '')
            floor = attributeList.find('li', {'id': 'mh-estate_attribute--23'}).contents[1]
            floorCount = attributeList.find('li', {'id': 'mh-estate_attribute--24'}).contents[1]
            price = soup.find('div', {'class': 'mh-estate__details__price__single'}).contents[0].replace('???.', '') \
                .replace(' ', '')

            list_attr = [href, city, buildingType, district, microDistrict, street, buildNumber, rooms, metro,
                         fullSquare,
                         livingSquare, kitchenSquare, floor, floorCount, price]
            csvFile.write("\n" + ','.join(list_attr))

            print("Time spent while reading " + href + ": " + str(datetime.now() - start_time))
        except:
            print("Something went wrong while reading: " + href)

    csvFile.close()
    hrefsFile.close()


def GetCoordinates(address):
    currCoord = geo.get(address)
    if currCoord is None:
        geo[address] = currCoord = geolocator.geocode(address)
    if currCoord is None:
        print("Address "+ address + " is not recognized.")
        return Coordinates.Coordinates(latitude = 0, longitude = 0)
    return currCoord


def CalculateCoordinatesToResultDataset ():
    df = pd.read_csv("fullDataset2.0.csv", encoding = 'windows-1251')
    df['latitude'] = list(map(
        lambda x: GetCoordinates(x).latitude, (df['street'] + ' ' + df['buildNumber']) + ', ' + df['city']))
    df['langitude'] = list(map(
        lambda x: GetCoordinates(x).longitude, (df['street'] + ' ' + df['buildNumber'])))
    df.to_csv("resultDataset2.0.csv")


#ReadHrefsOfApartments()
ReadDataOfApartments()
CalculateCoordinatesToResultDataset()