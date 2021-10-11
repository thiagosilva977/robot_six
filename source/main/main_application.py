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
import string
import random

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

    def generate_filename(self):

        now = datetime.datetime.now() # current date and time
        S = 6  # number of characters in the string.
        # call random.choices() string module to find the string in Uppercase + numeric data.
        ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))

        return str('ecac_')+str(ran)


    def save_table(self, data, columns):
        print('Saving Table')

        download_path = config_functions.create_paths(bot_name='e-CAC')

        data_name = self.generate_filename()


        path_file = str(str(download_path) + '\\' + str(data_name) + str(".xlsx"))


        df = pd.DataFrame(data, columns=columns)
        df.to_excel(path_file, index=False)

        print('\n\nOpening file: ',path_file)

        os.startfile(path_file)


    def run_program_table_iframe(self):

        browser = func_selenium.initialize_webdriver(webdriver_type='chrome')

        # remove this

        #browser.get('https://www.aliexpress.com/store/feedback-score/1665279.html')

        while True:
            input('ENTER para iniciar.')
            try:

                print('Tentando capturar a tabela ..')

                # IFRAME SWITCH

                iframename = 'frmApp'

                iframe = browser.find_element_by_xpath('//iframe[@id="'+str(iframename)+'"]')

                browser.switch_to.frame(iframe)

                print('iframe identificado !!!!')

                soup = bs4_functions.make_soup(browser.page_source)


                tablename1 = 'table table-hover table-condensed emissao is-detailed'
                tablename2 = 'table table-bordered'


                'https://www.w3schools.com/html/html_tables.asp'

                'https://www.aliexpress.com/store/feedback-score/1665279.html'
                ''
                namedocument = None
                try:
                    namedocument = browser.find_element_by_xpath('//span[@id="LabelParametros"]').text

                except:
                    pass

                print('namedocument: ',namedocument)

                regex_torre = re.compile('.*dataGrid.*')

                table = soup.find("table", {"class": regex_torre})
                columns = [i.get_text(strip=True) for i in table.find_all("th")]
                data = []

                for tr in table.find("tbody").find_all("tr"):
                    data.append([td.get_text(strip=True) for td in tr.find_all("td")])

                self.save_table(data=data, columns=columns)

                browser.switch_to.default_content()

            except BaseException:
                print('\n\n###### ERRO ####')
                msg = traceback.format_exc()
                print(msg)
                browser.switch_to.default_content()
                print('\n##############\n\nNão foi possível acessar a tabela')


    def run_program_check(self):

        browser = func_selenium.initialize_webdriver(webdriver_type='chrome')
        while True:
            input('ENTER para iniciar.')
            try:
                print('Tentando checar itens ...')




                iframename = 'rating-displayer'

                iframe = browser.find_element_by_xpath('//iframe[@id="'+str(iframename)+'"]')

                browser.switch_to.frame(iframe)




                #elements = browser.find_elements_by_xpath('//input[@id^="test-"]')
                elements = browser.find_elements_by_css_selector("input[id^='myCh']")

                print(len(elements))
                for element in elements:
                    element.click()

                print('Todos os elementos checados')

                browser.switch_to.default_content()


            except BaseException:
                print('\n\n###### ERROo ####')
                msg = traceback.format_exc()
                print(msg)
                browser.switch_to.default_content()

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
        botclass.run_program_table_iframe()

    elif 'checkonly' in execute_program:
        botclass = botname()
        botclass.run_program_check()

    elif 'anothercommand' in execute_program:
        print('anothercommand')

    else:
        print('cannot find a execution script')
