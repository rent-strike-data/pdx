from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import csv
from time import sleep
from random import randint

property_ids = []
owners = []
owner_addresses = []

with open('property_ids3.csv', newline='') as f:
    reader = csv.reader(f)
    p_ids = list(reader)

counter = 0
for p_id in p_ids:
    p_id = p_id[0]

    url = "https://www.portlandmaps.com/detail/property/" + p_id + "_did/"

    driver = webdriver.Chrome()
    driver.get(url)
    sleep(randint(3, 7))
    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    owner_dt = soup.find('dt', string='Owner')
    if owner_dt is None:
        # print('no owner_dt found')
        owner = "NULL"
        owner_address = "NULL"
    else:
        # print("owner_dt found")
        # print(owner_dt)
        owner = owner_dt.find_next_sibling('dd').text
        try:
            owner
        except NameError:
            owner = "NULL"
        # if owner == "NULL":
        #     # print('no owner found')
        # else:
        #     # print("owner found")
        #     # print(owner)

        owner_address = soup.find('dt', string='Owner Address').find_next_sibling('dd').text
        try:
            owner_address
        except NameError:
            owner_address = "NULL"
        # print(owner_address)

        property_ids.append(p_id)
        owners.append(owner)
        owner_addresses.append(owner_address)

        properties = pd.DataFrame({
            'p_id': property_ids,
            'owner': owners,
            'owner_address': owner_addresses
        })

        # to see your dataframe
        # print(properties)

        # write all scraped data to a CSV file every 50 lines
        if counter % 50 == 0:
            properties.to_csv('result_' + str(counter) + '.csv')

        counter = counter + 1
        print(counter)
        driver.quit()
    # 835k total properties
    # 390k within pdx city limits
    # 319k with property id