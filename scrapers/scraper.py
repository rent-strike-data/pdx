import csv
import requests
import datetime
from time import sleep, time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

property_ids = []
owners = []
owner_addresses = []

def get_driver():
    # print('get_driver')
    # initialize options
    options = webdriver.ChromeOptions()
    # pass in headless argument to options
    options.add_argument('--headless')
    # initialize driver
    driver = webdriver.Chrome(chrome_options=options)
    return driver


def connect_to_base(browser, p_id):
    # print('connect_to_base')
    # print(p_id)
    base_url = f'https://www.portlandmaps.com/detail/property/{p_id}_did/'
    print(base_url)
    connection_attempts = 0
    while connection_attempts < 3:
        try:
            browser.get(base_url)
            # wait for table element with id = 'summary' to load
            # before returning True
            WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((By.ID, 'summary'))
            )
            return True
        except Exception as ex:
            connection_attempts += 1
            print(f'Error connecting to {base_url}.')
            print(f'Attempt #{connection_attempts}.')
    return False

def get_owner_data(html, p_id):
    # print('get_owner_data')
    # create soup object
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

        return properties
