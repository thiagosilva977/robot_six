import argparse
import json
import argparse
import datetime
import json
import multiprocessing
import re
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


    def run_program_table(self):

        browser = func_selenium.initialize_webdriver(webdriver_type='chrome')
        while True:
            input('ENTER para iniciar.')
            try:
                print('Tentando capturar a tabela ..')
                soup = bs4_functions.make_soup(browser.page_source)


                tablename1 = 'table table-hover table-condensed emissao is-detailed'
                tablename2 = 'table table-bordered'


                'https://www.w3schools.com/html/html_tables.asp'

                regex_torre = re.compile('.*customers.*')

                table = soup.find("table", {"id": regex_torre})
                columns = [i.get_text(strip=True) for i in table.find_all("th")]
                data = []

                for tr in table.find("tbody").find_all("tr"):
                    data.append([td.get_text(strip=True) for td in tr.find_all("td")])

                self.save_table(data=data, columns=columns)

            except BaseException:
                print('\n\n###### ERRO ####')
                msg = traceback.format_exc()
                print(msg)
                print('\n##############\n\nNão foi possível acessar a tabela')


    def run_program_check(self):

        browser = func_selenium.initialize_webdriver(webdriver_type='chrome')
        while True:
            input('ENTER para iniciar.')
            try:
                print('Tentando checar itens ...')
                #elements = browser.find_elements_by_xpath('//input[@id^="test-"]')
                elements = browser.find_elements_by_css_selector("input[id^='myCh']")

                print(len(elements))
                for element in elements:
                    element.click()

                print('Todos os elementos checados')



            except BaseException:
                print('\n\n###### ERRO ####')
                msg = traceback.format_exc()
                print(msg)
                print('\n##############\n\nNão foi possível checar itens')



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
        botclass.run_program_table()

    elif 'checkonly' in execute_program:
        botclass = botname()
        botclass.run_program_check()

    elif 'anothercommand' in execute_program:
        print('anothercommand')

    else:
        print('cannot find a execution script')
