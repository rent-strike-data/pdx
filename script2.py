from urllib import urlopen
from bs4 import BeautifulSoup
from urlparse import urlparse, urljoin, urlunparse
from multiprocessing.pool import ThreadPool as Pool
from multiprocessing import cpu_count
import sys
import datetime
import csv
from scrapers.scraper import get_driver, connect_to_base, \
    get_owner_data


class ws:
    visited = []
    urls = []
    page_visited = []
    depth = 0
    counter = 0
    root = ""

    def __init__(self, depth):
        self.depth = depth

    def get_pid(row_num):
        # print(f'get_pid {row_num}')
        with open("property_ids3.csv", newline='') as f:
            r = csv.reader(f)
            for i in range(row_num):  # count from 0 to counter
                next(r)  # discard intervening rows
            row = next(r)
            # print(f'row: {row}')
            return row[0]

    def scrapeStep(self, row_number, output_filename):
        result_urls = []
        print(f'scrapeStep: {row_number}')
        browser = get_driver()
        p_id = get_pid(row_number)
        if connect_to_base(browser, p_id):
            sleep(1)
            try:
                html = browser.page_source
            except IOError as err:
                print("scrapeStep Error: {}".format(err.message))
            except Exception as err:
                print("scrapeStep Error: {}".format(err.message))

        try:
            properties = get_owner_data(html, p_id)
        except:
            print("scrapeStep Error: {}".format(sys.exc_info()))
        self.page_visited.append(p_id)

    def run(self):
        while self.counter < self.depth:
            for w in self.page_visited:
                if w not in self.visited:
                    self.visited.append(w)
                    self.urls.append(w)
            self.page_visited = []
            pool = Pool(cpu_count()*2)
            results = pool.map(self.scrapeStep, self.urls)
            self.counter+=1
        print(len(self.visited))
        return self.visited

print("Start: {0}".format(datetime.datetime.now()))
mysite = ws(100)
mysite.run()
print("End: {0}".format(datetime.datetime.now()))