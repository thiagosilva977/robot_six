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
import source.common.input_functions as input_functions
from pathlib import Path
import os
import string
import random
import codecs
import xlsxwriter
import source.main.dbstyle as dbstyle


class Projetoecac:

    def generate_filename(self):

        now = datetime.datetime.now()  # current date and time
        S = 6  # number of characters in the string.
        # call random.choices() string module to find the string in Uppercase + numeric data.
        ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))

        return str('ecac_') + str(ran)

    def save_table(self, data, columns, cnpj='NaN', nome='NaN', data_arrecadacao='NaN',open_auto=False):
        print('Saving Table')

        download_path = config_functions.organize_custom_path(bot_name='Programa e-CAC', cnpj=cnpj)

        data_name = str(cnpj + '_' + str(data_arrecadacao).replace('a', '_')).replace(' ', '').replace('/', '-')

        path_file = str(str(download_path) + '\\' + str(data_name) + str(".xlsx"))

        print(path_file)

        df = pd.DataFrame(data, columns=columns)

        """df = df.drop(['columnsname'], axis=1)"""
        """df = df.drop(['SaldoDisponível'], axis=1)"""

        # Removing some Unused columns
        df.drop(df.columns[[0, 1, 11]], axis=1, inplace=True)
        df = df.iloc[1:]

        df["VALOR_TOTAL"] = df["VALOR_TOTAL"].str.replace(".", "").str.replace(",", ".").astype(float)

        # df["VALOR_TOTAL"] = pd.to_numeric(df["VALOR_TOTAL"], downcast="float")

        # df['PERIODO_APURACAO'] = pd.to_datetime(df['PERIODO_APURACAO'], format="%m/%d/%Y")

        values_cod_receita = []

        for key, value in df['CODIGO_RECEITA'].iteritems():
            values_cod_receita.append(str(dbstyle.obtain_tipo_tributo(valor=str(value))))

        print(len(values_cod_receita))

        df.insert(7, "DESCR_RECEITA", values_cod_receita, True)

        if cnpj == 'NaN':
            pass
        else:
            values_cnpj = []
            for key, value in df['CODIGO_RECEITA'].iteritems():
                values_cnpj.append(str(cnpj))

            df.insert(0, "CNPJ", values_cnpj, True)

        if nome == 'NaN':
            pass
        else:
            values_nome = []
            for key, value in df['CODIGO_RECEITA'].iteritems():
                values_nome.append(str(nome))

            df.insert(1, "NOME", values_nome, True)

        if data_arrecadacao == 'NaN':
            pass
        else:
            values_data_arrecadacao = []
            for key, value in df['CODIGO_RECEITA'].iteritems():
                values_data_arrecadacao.append(str(data_arrecadacao))

            df.insert(2, "PERIODO_ARRECADACAO", values_data_arrecadacao, True)

        """writer = pd.ExcelWriter(path_file, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1')
        writer.save()"""

        writer = pd.ExcelWriter(path_file)
        df.to_excel(writer, sheet_name='Sheet1', index=False, na_rep='NaN')

        # Auto-adjust columns' width
        for column in df:
            column_width = max(df[column].astype(str).map(len).max(), len(column))
            col_idx = df.columns.get_loc(column)
            writer.sheets['Sheet1'].set_column(col_idx, col_idx, column_width)

        writer.save()

        # time.sleep(4554)
        # df.to_excel(path_file, index=False)

        print('\n\nOpening file: ', path_file)
        if open_auto:
            os.startfile(path_file)

    def run_program_table_iframe(self):

        browser = func_selenium.initialize_webdriver(webdriver_type='chrome')

        # remove this

        # browser.get('https://www.aliexpress.com/store/feedback-score/1665279.html')
        print('Aguarde ...')
        time.sleep(3)
        while True:
            clear = lambda: os.system('cls')
            clear()
            input('Pressione ENTER para iniciar.')
            clear = lambda: os.system('cls')
            clear()
            try:
                configs = config_functions.read_custom_configs()

                open_auto = configs.get('abrir_auto')

                print('Tentando capturar a tabela ..')

                # IFRAME SWITCH

                iframename = 'frmApp'

                iframe = browser.find_element_by_xpath('//iframe[@id="' + str(iframename) + '"]')

                browser.switch_to.frame(iframe)

                """ PARSING DAS INFOS """
                self.transform_to_data(html=browser.page_source,open_auto=open_auto)


                browser.switch_to.default_content()

            except BaseException:
                print('\n\n###### ERRO ####')
                msg = traceback.format_exc()
                print(msg)
                browser.switch_to.default_content()
                print('\n##############\n\nNão foi possível acessar a tabela')

    def run_program_table_iframe_automated(self):

        browser = func_selenium.initialize_webdriver(webdriver_type='chrome')

        # remove this

        # browser.get('https://www.aliexpress.com/store/feedback-score/1665279.html')
        print('Aguarde ...')
        time.sleep(3)
        while True:
            clear = lambda: os.system('cls')
            clear()
            input('Pressione ENTER para iniciar.')
            clear = lambda: os.system('cls')
            clear()
            try:

                configs = config_functions.read_custom_configs()

                start_date = configs.get('start_date')
                end_date = configs.get('end_date')
                open_auto = configs.get('abrir_auto')

                print(start_date, end_date)

                period_to_search = input_functions.dates_between_two_dates(start_date=start_date, end_date=end_date)

                print('Periodos para buscar: ', period_to_search)

                for i in range(len(period_to_search) - 1):
                    print('Buscando periodo: ', period_to_search[i], period_to_search[i + 1])

                    current_start_date = period_to_search[i]
                    current_end_date = period_to_search[i + 1]

                    browser.find_element_by_xpath('').send_keys(current_start_date)
                    browser.find_element_by_xpath('').send_keys(current_end_date)
                    browser.find_element_by_xpath('').click()

                    func_selenium.wait_loading(MAXTIME=20, XPATH='', browser=browser)

                    print('Tentando capturar a tabela ..')

                    # IFRAME SWITCH

                    iframename = 'frmApp'

                    iframe = browser.find_element_by_xpath('//iframe[@id="' + str(iframename) + '"]')

                    browser.switch_to.frame(iframe)

                    """ PARSING DAS INFOS """
                    number_data = self.count_data(html=browser.page_source)
                    if number_data >= 998:
                        new_period_search = input_functions.dates_between_two_dates(start_date=current_start_date,
                                                                                    end_date=current_end_date,
                                                                                    frequency='d')
                        browser.switch_to.default_content()
                        browser.back()
                        time.sleep(8)
                        for j in range(len(new_period_search) - 1):
                            print('Buscando periodo: ',new_period_search[j], new_period_search[j + 1])

                            current_start_date = new_period_search[j]
                            current_end_date = new_period_search[j + 1]

                            browser.find_element_by_xpath('').send_keys(current_start_date)
                            browser.find_element_by_xpath('').send_keys(current_end_date)
                            browser.find_element_by_xpath('').click()

                            func_selenium.wait_loading(MAXTIME=20, XPATH='', browser=browser)

                            print('Tentando capturar a tabela ..')

                            # IFRAME SWITCH

                            iframename = 'frmApp'

                            iframe = browser.find_element_by_xpath('//iframe[@id="' + str(iframename) + '"]')

                            browser.switch_to.frame(iframe)
                            self.transform_to_data(html=browser.page_source,open_auto=open_auto)

                    else:
                        self.transform_to_data(html=browser.page_source,open_auto=open_auto)
                        browser.switch_to.default_content()
                        browser.back()

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

                iframe = browser.find_element_by_xpath('//iframe[@id="' + str(iframename) + '"]')

                browser.switch_to.frame(iframe)

                # elements = browser.find_elements_by_xpath('//input[@id^="test-"]')
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

    def import_lista_tributos(self):
        print('listando tributos')
        file_errors_location = 'D:\\freela\\robot_six\\Lista de tributos.xlsx'
        df = pd.read_excel(file_errors_location)
        print(df)

        codigos_imposto = []

        for key, value in df['CODIGO_IMPOSTO'].iteritems():
            codigos_imposto.append(value)

        tipo_imposto = []

        for key, value in df['TIPO_IMPOSTO'].iteritems():
            tipo_imposto.append(value)

        print(len(codigos_imposto))
        print(len(tipo_imposto))

        tributos_dict = []

        for i in range(len(codigos_imposto)):
            tributos_dict.append({
                'codigo': codigos_imposto[i],
                'tipo': tipo_imposto[i]

            })

        print(tributos_dict)

    def test_tipo_tributos(self):
        tributo = dbstyle.obtain_tipo_tributo(valor=str(855))
        print(tributo)

    def count_data(self, html):
        soup = bs4_functions.make_soup(html)
        regex_torre = re.compile('.*dataGrid.*')
        table = soup.find("table", {"class": regex_torre})
        data = []

        for tr in table.find("tbody").find_all("tr"):
            data.append([td.get_text(strip=True) for td in tr.find_all("td")])

        return len(data)

    def transform_to_data(self, html,open_auto=True):

        soup = bs4_functions.make_soup(html)

        regex_torre = re.compile('.*dataGrid.*')

        table = soup.find("table", {"class": regex_torre})
        columns = [i.get_text(strip=True) for i in table.find_all("th")]
        data = []
        custom_columns = ['none', 'none', 'TIPO_DOCUMENTO', 'NUMERO_DOCUMENTO',
                          'DETALHAR_COMPOSICAO', 'PERIODO_APURACAO',
                          'DATA_ARRECADACAO', 'DATA_VENCIMENTO',
                          'CODIGO_RECEITA', 'NUMERO_REFERENCIA', 'VALOR_TOTAL',
                          'SALDO_DISPONIVEL']

        for tr in table.find("tbody").find_all("tr"):
            data.append([td.get_text(strip=True) for td in tr.find_all("td")])

        try:
            cnpj = 'NaN'
            nome = 'NaN'
            data_arrecadacao = 'NaN'

            params = soup.find('span', {'id': 'LabelParametros'}).text

            cnpj = params.split('Nome:')[0].split('CNPJ:')[1].strip().replace('.', '').replace('-', '').replace('/', '')

            print(cnpj)

            nome = params.split('Data de Arrecada')[0].split('Nome: ')[1].strip()

            print(nome)

            data_arrecadacao = params.split('Faixa de valores:')[0].split('Data de Arrecada')[1].split(':')[1].strip()

            print(data_arrecadacao)
            self.save_table(data=data, columns=custom_columns, cnpj=cnpj, nome=nome, data_arrecadacao=data_arrecadacao,
                            open_auto=open_auto)

        except:
            self.save_table(data=data, columns=custom_columns,open_auto=open_auto)


if __name__ == "__main__":
    # This application is responsible to get an argument and decides what runs.

    bot_name = 'ECAC'

    # Gets arguments from .bat or .sh file
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--to_execute', required=True, type=str, help="Program that will be initialized")
    args = parser.parse_args()

    execute_program = args.to_execute

    # Args treatment

    if execute_program == 'standard_initialization':
        botclass = Projetoecac()
        botclass.run_program_table_iframe()

    elif execute_program == 'auto_search':
        botclass = Projetoecac()
        botclass.run_program_table_iframe_automated()

    elif 'test_program' in execute_program:
        f = codecs.open("./source/assets/html elementos.html", 'r')
        html = f.read()
        botclass = Projetoecac()
        botclass.transform_to_data(html=html)

    elif 'anothercommand' in execute_program:
        print('anothercommand')

    else:
        print('cannot find a execution script')
