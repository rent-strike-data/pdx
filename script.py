import datetime
from itertools import repeat
from time import sleep, time
from multiprocessing import Pool, Value, Lock, cpu_count, RawValue
import csv

from scrapers.scraper import get_driver, connect_to_base, \
    get_owner_data


class Counter(object):
    def __init__(self, initval=0):
        self.val = RawValue('i', initval)
        self.lock = Lock()

    def increment(self):
        with self.lock:
            self.val.value += 1

    @property
    def value(self):
        return self.val.value

def run_process(row_number, output_filename):
    print(f'run_process: {counter.value}')
    browser = get_driver()
    p_id = get_pid()
    if connect_to_base(browser, p_id):
        sleep(2)
        html = browser.page_source
        properties = get_owner_data(html, p_id)
        # print(properties)
        if counter.value % 50 == 0:
            print(f'writing to csv: {output_filename}')
            properties.to_csv('result_' + output_filename)
        counter.increment()
        browser.quit()
    else:
        print('Error connecting')
        browser.quit()

def get_pid():
    print(f'get_pid {counter.value}')
    with open("property_ids3.csv", newline='') as f:
        r = csv.reader(f)
        for i in range(counter.value):  # count from 0 to counter
            next(r)  # discard intervening rows
        row = next(r)
        # print(f'row: {row}')
        return row[0]


if __name__ == '__main__':
    counter = Counter(0)
    print(f'cpu_count - 1 = {cpu_count() -1}')
    start_time = time()
    output_timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    output_filename = f'output_{output_timestamp}.csv'

    # browser = get_driver()
    # while counter <= 50:
    #     p_id = get_pid(counter)
    #     print(f'Scraping property #{counter}, p_id {p_id}...')
    #     run_process(p_id, counter, output_filename, browser)
    #     counter = counter + 1
    # browser.quit()

    # pool = Pool(4, initializer, (counter, lock))

    # with Pool(cpu_count() - 1) as p:
    #     p_id = get_pid(counter)
    #     p.starmap(run_process, zip(range(1, 51), repeat(output_filename)))
    # p.close()
    # p.join()

    with Pool(4, None, (counter)) as p:
        p_id = get_pid()
        p.starmap(run_process, zip(range(1, 51), repeat(output_filename)))
    p.close()
    p.join()

    end_time = time()
    elapsed_time = end_time - start_time
    print(f'Elapsed run time: {elapsed_time} seconds')


