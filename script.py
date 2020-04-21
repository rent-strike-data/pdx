import datetime
from itertools import repeat
from time import sleep, time
from multiprocessing import Pool, cpu_count
import csv

from scrapers.scraper import get_driver, connect_to_base, \
    get_owner_data


def run_process(counter, output_filename):
    print(f'run_process: {counter}')
    browser = get_driver()
    p_id = get_pid(counter)
    if connect_to_base(browser, p_id):
        sleep(2)
        html = browser.page_source
        properties = get_owner_data(html, p_id)
        # print(properties)
        if counter % 50 == 0:
            print(f'writing to csv: {output_filename}')
            properties.to_csv('result_' + output_filename + '.csv')
        counter = counter + 1
        browser.quit()
    else:
        print('Error connecting')
        browser.quit()

def get_pid(counter):
    print(f'get_pid {counter}')
    with open("property_ids3.csv", newline='') as f:
        r = csv.reader(f)
        for i in range(counter):  # count from 0 to counter
            next(r)  # discard intervening rows
        row = next(r)
        # print(f'row: {row}')
        return row[0]


if __name__ == '__main__':
    print(f'cpu_count - 1 = {cpu_count() -1}')
    start_time = time()
    counter = 1
    output_timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    output_filename = f'output_{output_timestamp}.csv'

    # browser = get_driver()
    # while counter <= 50:
    #     p_id = get_pid(counter)
    #     print(f'Scraping property #{counter}, p_id {p_id}...')
    #     run_process(p_id, counter, output_filename, browser)
    #     counter = counter + 1
    # browser.quit()

    with Pool(cpu_count() - 1) as p:
        p_id = get_pid(counter)
        p.starmap(run_process, zip(range(1, 51), repeat(output_filename)))
    p.close()
    p.join()

    end_time = time()
    elapsed_time = end_time - start_time
    print(f'Elapsed run time: {elapsed_time} seconds')


