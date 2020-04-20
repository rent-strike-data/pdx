import datetime
from time import sleep, time

from scrapers.scraper import get_driver, connect_to_base, \
    parse_html, write_to_file


def run_process(p_id, counter, browser):
    if connect_to_base(browser, p_id):
        sleep(2)
        html = browser.page_source
        soup = parse_html(html)
        properties = get_owner_data(soup, p_id)
        print(properties)
        if counter % 50 == 0:
            properties.to_csv('result_' + str(counter) + '.csv')
        print(counter)
    else:
        print('Error connecting')

def get_pid(counter):
    with open("property_ids3.csv", newline='') as f:
        r = csv.reader(f):
        for i in range(counter):  # count from 0 to counter
            next(r)  # discard intervening rows
        row = next(r)
        print(f'row: {row}')
        return row

def get_owner_data(soup, p_id):
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


if __name__ == '__main__':
    start_time = time()
    counter = 1
    output_timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    output_filename = f'output_{output_timestamp}.csv'
    browser = get_driver()
    while counter <= 50:
        p_id = get_pid(counter)
        print(f'Scraping property #{counter}, p_id {p_id}...')
        run_process(p_id, counter, browser)
        counter = counter + 1
    browser.quit()
    end_time = time()
    elapsed_time = end_time - start_time
    print(f'Elapsed run time: {elapsed_time} seconds')