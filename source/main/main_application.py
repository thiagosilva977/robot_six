import argparse
import json
import argparse
import datetime
import json
import multiprocessing
import sys
import time
import traceback
import pandas as pd
import source.common.selenium_functions as func_selenium
import source.common.bs4_functions as bs4_functions
import source.common.parsing_functions as parsing_functions
import source.common.configuration_functions as config_functions
from pathlib import Path
import os


class botname:

    def step_1(self):
        print('Acessando Script')

        browser = func_selenium.initialize_webdriver(webdriver_type='chrome')

        browser.get('https://webscraper.io/test-sites/tables')

        time.sleep(2)

        soup = bs4_functions.make_soup(browser.page_source)

        """table = soup.find('table',{'class':'table table-bordered'})

        rows = table.find_all('tr')

        for row in rows:
            cols = row.find_all('td')
            for col in cols:"""

        table = soup.find("table", {"class": "table table-bordered"})
        columns = [i.get_text(strip=True) for i in table.find_all("th")]
        data = []

        for tr in table.find("tbody").find_all("tr"):
            data.append([td.get_text(strip=True) for td in tr.find_all("td")])

        self.save_table(data=data, columns=columns)

    def step_2(self):
        print('step1')

    def save_table(self, data, columns):
        print('Saving Table')

        download_path = config_functions.create_paths()

        data_name = 'data'

        path_file = str(str(download_path) + '\\' + str(data_name) + str(".xlsx"))


        df = pd.DataFrame(data, columns=columns)
        df.to_excel(path_file, index=False)

        print('\n\nOpening file: ',path_file)

        os.startfile(path_file)


if __name__ == "__main__":
    # This application is responsible to get an argument and decides what runs.

    bot_name = 'TEST'

    # Gets arguments from .bat or .sh file
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--to_execute', required=True, type=str, help="Program that will be initialized")
    args = parser.parse_args()

    execute_program = args.to_execute

    # Args treatment

    if execute_program == 'standard_initialization':
        botclass = botname()
        botclass.step_1()

    elif 'anothercommand' in execute_program:
        print('anothercommand')

    else:
        print('cannot find a execution script')
