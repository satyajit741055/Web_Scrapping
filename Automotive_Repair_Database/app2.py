""" 

Scope
I would like to scrape an online directory of all of the smog test centers in California
Output
The output should be a .csv file with all fields filled out, and should be error-free
Method
1. Go to https://search.dca.ca.gov/advanced
2. Under “Boards Or Bureau” select “Automotive Repair, Bureau Of”
3. Under “License Type” select “Smog Check Station”.
4. Under City, the scraper will cycle through each and every city, as there is a limit on the search for about 1,000 records. See below where I select “National City” as an example. Then click “Search”



Task 
1.URL : https://search.dca.ca.gov/advanced 
2.“Boards Or Bureau” select “Automotive Repair, Bureau Of”
3.“License Type” select “Smog Check Station”.
4. Select 1 city 
    5. New Page will appear now Click to each license number 
        6.  New Page will appear of info scrap the info
            - Name, e.g. “07 AUTO SMOG TEST AND REPAIR”
            - License Type, e.g. “SMOG STATION – TEST & REPAIR”
            - License Status, e.g. “VALID”
            - Phone Number e.g. “619-477-1322”
            - Address Number and Street, e.g. “25 EAST 18th ST”
            - Address Line #2, if any, e.g. “null”
            - City, e.g. “NATIONAL CITY”
            - State, e.g. “CA”
            - ZIP, e.g. “91950”
            - County, e.g. “SAN DIEGO COUNTY”
            - Named Individual #1, e.g. “COBIAN, PEDRO ANDRES JR”
            - Named Individual #2, if any, e.g. “null”
        - 




"""

from select import select
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time 
import os
from selenium.webdriver.support.ui import Select
import csv

# constants 
URL = 'https://search.dca.ca.gov/advanced'
Board_of_Bureau = 'Automotive Repair, Bureau Of' 
License_Type  = 'Smog Check Station'




driver = webdriver.Chrome(executable_path=r"D:\Projects_new\Upwork\Webscrapping\Automotive_Repair_Database\chromedriver.exe")

driver.get(URL)
driver.maximize_window()

def get_url(URL=URL):
    driver.get(URL)
    
    element = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.ID, 'boardCode'))
    )
    board_code= driver.find_element_by_id('boardCode')
    drop=Select(board_code)
    drop.select_by_index(3)

    print(f'{Board_of_Bureau} selected')

    license_Type = driver.find_element_by_id('licenseType')
    drop= Select(license_Type)
    drop.select_by_visible_text(License_Type)
    print(f'{License_Type} selected')


    



csv_columns = ['Name', 'License Type', 'License Status', 'Phone Number', 'Address Number and Street', 'Address Line', 'City', 'State', 'ZIP', 'County', 'Named Individual #1', 'Named Individual #2']


# Filling constant data such as Board_of_Bureau,License_Type

element = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.ID, 'boardCode'))
    )
board_code= driver.find_element_by_id('boardCode')
drop=Select(board_code)
drop.select_by_index(3)

print(f'{Board_of_Bureau} selected')

license_Type = driver.find_element_by_id('licenseType')
drop= Select(license_Type)
drop.select_by_visible_text(License_Type)
print(f'{License_Type} selected')

# extracting All cities from california and saved into california_cities
l= driver.find_element_by_name("advCity")
d= Select(l)

'''for i in d.options:
    #print(i.text)
    city.append(i.text)
    with open('california_cities','a') as f:
        f.write(i.text+'\n')
    if i.text == 'Zenia':
        break'''
with open('california_cities' , 'r',encoding='utf-8') as f:
    a = f.readlines()

city = [a[i].strip() for i in range(len(a))]
city_1 = [''] 

def scrolldown():
    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
       


print(len(city) , ' city Length')

count = 0
for i in city:
    city = driver.find_element_by_name("advCity")
    drop= Select(city)
    drop.select_by_visible_text(i)
    print(f'{i} city selected')

    search_bar = driver.find_element_by_xpath('//*[@id="srchSubmitHome"]')
    search_bar.click()


    '''
    Extract all licence href 
    go to them one by one and scrapp the data 
   '''

    try:
        element = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.ID, 'mD0'))
        )
    except:
        with open('log.txt','a') as s:
            s.write(f'{i} city Has no url  ')
            dict_data = [{'Name': 'Null', 
                    'License Type': 'Null', 
                    'License Status': 'Null',
                    'Phone Number' : 'Null',
                    'Address Number and Street': 'Null',
                    'Address Line':'Null' ,
                    'City':i,
                    'State':'Null',
                    'ZIP':'Null',
                    'County':'Null',
                    'Named Individual #1':'Null',
                    'Named Individual #2':'Null'}]

        try:
            with open('data.csv', 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                for data in dict_data:
                    writer.writerow(data)
        except IOError:
            print("I/O error")
            continue

    scrolldown()
    license_numbers_url = []
    license_num = driver.find_elements_by_xpath('//*[@class="button newTab"]')

    for j in license_num:
        #print(j.get_attribute("href"))
        license_numbers_url.append(j.get_attribute("href"))
 
    
    print(f'{len(license_numbers_url)} in city {i}')


    for k in license_numbers_url:
        driver.get(k)
        
        element = WebDriverWait(driver, 50).until(
                EC.presence_of_element_located((By.ID, 'licDetail'))
            )
        




        name_select = driver.find_element_by_xpath('//*[@id="name"]')
        a = name_select.text
        
        Name = a.split(': ')[1]
        print(f'Name : {Name}')



        license_type__select = driver.find_element_by_xpath('//*[@id="licType"]')
        a = license_type__select.text
        license_type = a.split(': ')[1]
        print(f'License Type : {license_type}')

        license_status_select = driver.find_element_by_xpath('//*[@id="primaryStatus"]/span[2]')
        license_status = license_status_select.text
        print(f'License Status: {license_status}')

        Phone_number_select = driver.find_element_by_xpath('//*[@id="licRegClass"]')
        a = Phone_number_select.text
        phone_number = a.split(': ')[1]
        print(f'Phone Number {phone_number}')

        Address_NUM_select = driver.find_element_by_xpath('//*[@id="address"]/p[2]')
        a = Address_NUM_select.text
        Address_Number_and_Street = a.split('\n')[0]
        print(f'Address_Number_and_Street: {Address_Number_and_Street}')

        Address_line = 'Null'
        print(f'Address Line : {Address_line}')

        if len(i.split(' ')) ==2:  ## need to code properly
            b = a.split('\n')[1]
            city = b.split(' ')[0] +' '+ b.split(' ')[1]
            print(f'city: {city}')

            state = b.split(' ')[2]
            print(f'state: {state}')

            zip = b.split(' ')[3]
            print(f'zip: {zip}')
        elif len(i.split(' ')) ==3:
            b = a.split('\n')[1]
            city = b.split(' ')[0] +' '+ b.split(' ')[1] +' '+ b.split(' ')[2]
            print(f'city: {city}')

            state = b.split(' ')[3]
            print(f'state: {state}')

            zip = b.split(' ')[4]
            print(f'zip: {zip}')
        elif len(i.split(' ')) ==4:
            b = a.split('\n')[1]
            city = b.split(' ')[0] +' '+ b.split(' ')[1] +' '+ b.split(' ')[2]+' '+ b.split(' ')[3]
            print(f'city: {city}')

            state = b.split(' ')[4]
            print(f'state: {state}')

            zip = b.split(' ')[5]
            print(f'zip: {zip}')
        else:
            b = a.split('\n')[1]
            city = b.split(' ')[0]
            print(f'city: {city}')

            state = b.split(' ')[1]
            print(f'state: {state}')

            zip = b.split(' ')[2]
            print(f'zip: {zip}')
        
        county = a.split('\n')[2]
        print(f'county: {county}')


        try:
            element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, 'qualManagersandPrincipals'))
                    )
        except: 
            element = False

        if element:
            name_individual_1_select = driver.find_element_by_xpath('//*[@id="qualManagersandPrincipals"]/div[1]/p')
            name_individual_1_ = name_individual_1_select.text
            name_individual_1 = name_individual_1_.split(':')[1]
        else:
            name_individual_1 = 'null'

        print(f'Named Individual #1 : {name_individual_1}')


        try:
            element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="qualManagersandPrincipals"]/div[3]'))
                    )
        except: 
            element = False

        if element:
            name_individual_2_select = driver.find_element_by_xpath('//*[@id="qualManagersandPrincipals"]/div[3]')
            a = name_individual_2_select.text
            name_individual_2 = a.split(': ')[1]
        else:
            name_individual_2 = 'null'


        print(f'Named Individual #2 : {name_individual_2}')
  
        dict_data = [{'Name': Name, 
                    'License Type': license_type, 
                    'License Status': license_status,
                    'Phone Number' : phone_number,
                    'Address Number and Street': Address_Number_and_Street,
                    'Address Line':Address_line ,
                    'City':city,
                    'State':state,
                    'ZIP':zip,
                    'County':county,
                    'Named Individual #1':name_individual_1,
                    'Named Individual #2':name_individual_2}]

        try:
            with open('data.csv', 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                for data in dict_data:
                    writer.writerow(data)
        except IOError:
            print("I/O error")

        with open('log.txt','a') as s:
            s.write(f'{i} city and licenese url :{k}\n  ')


   # implementing logic for going to next city
    time.sleep
    count = count +1
    get_url(URL=URL)






