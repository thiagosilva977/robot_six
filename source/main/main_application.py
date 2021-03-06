import argparse
import codecs
import datetime
import glob
import os
import random
import re
import string
import time
import traceback

import pandas as pd
import progress.bar
from tika import parser as tikaparser

import source.common.bs4_functions as bs4_functions
import source.common.configuration_functions as config_functions
import source.common.input_functions as input_functions
import source.common.selenium_functions as func_selenium
import source.main.dbstyle as dbstyle


class Projetoecac:

    def generate_filename(self):

        now = datetime.datetime.now()  # current date and time
        S = 6  # number of characters in the string.
        # call random.choices() string module to find the string in Uppercase + numeric data.
        ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))

        return str('ecac_') + str(ran)

    def generate_filename_pdf(self):

        now = datetime.datetime.now()  # current date and time
        S = 6  # number of characters in the string.
        # call random.choices() string module to find the string in Uppercase + numeric data.
        ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))

        return str('pdf_handler_') + str(ran)

    def save_table(self, data, columns, cnpj='NaN', nome='NaN', data_arrecadacao='NaN', open_auto=False):
        print('Saving Table')

        download_path = config_functions.organize_custom_path(bot_name='Programa e-CAC', cnpj=cnpj)

        data_name = str(cnpj + '_' + str(data_arrecadacao).replace('a', '_')).replace(' ', '').replace('/', '-')

        path_file = str(str(download_path) + '\\' + str(data_name) + str(".xlsx"))

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

        print('\n\nArquivo Salvo em: ', path_file)
        if open_auto:
            os.startfile(path_file)

    def verify_documento_existente(self, valor, lista_items):
        flag = False

        principal = 0.0
        juros = 0.0
        multa = 0.0

        for i in range(len(lista_items)):

            if lista_items[i].get('documento') in valor:
                flag = True
                principal = lista_items[i].get('principal')
                juros = lista_items[i].get('juros')
                multa = lista_items[i].get('multa')

            else:
                pass

        return flag, principal, juros, multa

    def save_table_v2(self, data, columns, cnpj='NaN', nome='NaN', data_arrecadacao='NaN', open_auto=False,
                      values_pdf='[]'):

        print('Agrupando Informações ...')
        download_path = config_functions.organize_custom_path(bot_name='Programa e-CAC', cnpj=cnpj)

        data_name = str(cnpj + '_' + str(data_arrecadacao).replace('a', '_')).replace(' ', '').replace('/', '-')

        path_file = str(str(download_path) + '\\' + str(data_name) + str(".xlsx"))

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

        # NOVOS CAMPOS
        values_principal = []
        values_juros = []
        values_multas = []

        for key, value in df['NUMERO_DOCUMENTO'].iteritems():
            exists, principal, juros, multa = self.verify_documento_existente(valor=value, lista_items=values_pdf)
            values_principal.append(principal)
            values_juros.append(juros)
            values_multas.append(multa)

        df.insert(12, "PRINCIPAL", values_principal, True)
        df.insert(13, "JUROS", values_juros, True)
        df.insert(14, "MULTA", values_multas, True)

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

        print('\n\nArquivo Salvo em: ', path_file)
        if open_auto:
            os.startfile(path_file)

    def run_program_table_iframe(self):

        browser = func_selenium.initialize_webdriver(webdriver_type='chrome')

        # remove this

        # browser.get('https://www.aliexpress.com/store/feedback-score/1665279.html')
        print('Aguarde ...')
        time.sleep(3)
        clear = lambda: os.system('cls')
        clear()
        while True:
            input('\n\n\nPressione ENTER para iniciar.')
            try:
                configs = config_functions.read_custom_configs()

                open_auto = configs.get('abrir_auto')

                print('Tentando capturar a tabela ..')

                # IFRAME SWITCH

                iframename = 'frmApp'

                iframe = browser.find_element_by_xpath('//iframe[@id="' + str(iframename) + '"]')

                browser.switch_to.frame(iframe)

                """ PARSING DAS INFOS """
                self.transform_to_data(html=browser.page_source, open_auto=open_auto)

                browser.switch_to.default_content()

            except BaseException:
                print('\n\n###### ERRO ####')
                msg = traceback.format_exc()
                print(msg)
                browser.switch_to.default_content()
                print('\n##############\n\nNão foi possível acessar a tabela')

    def run_program_table_iframe_maisdados(self, browser_download_pdf):

        browser = func_selenium.initialize_webdriver(webdriver_type='chrome', download_path=browser_download_pdf)

        # remove this

        # browser.get('https://www.aliexpress.com/store/feedback-score/1665279.html')
        print('Aguarde ...')
        time.sleep(3)
        clear = lambda: os.system('cls')
        clear()
        while True:
            input('\n\n\nPressione ENTER para iniciar.')
            try:
                configs = config_functions.read_custom_configs()

                open_auto = configs.get('abrir_auto')
                tempo_download = configs.get('tempo_download')

                print('Tentando capturar a tabela ..')

                # IFRAME SWITCH

                iframename = 'frmApp'
                iframe = browser.find_element_by_xpath('//iframe[@id="' + str(iframename) + '"]')
                browser.switch_to.frame(iframe)
                html_inicial_pagina = browser.page_source

                """ HANDLING DE PDFs """

                botao_download = browser.find_element_by_xpath('//input[@id="BtnImprimirConprovante"]')

                checkboxes = browser.find_elements_by_xpath('//input[contains(@id,"_CheckBoxPagamentos")]')

                print('Número de Checkboxes: ' + str(len(checkboxes)))
                print('\nInicializando Download de PDFs\n')

                bar = progress.bar.ChargingBar(str('Download PDFs'), max=len(checkboxes))

                range_checkboxes = int(len(checkboxes) / 10) + 1

                current_checkbox = 0
                last_checkbox = 0
                list_last_checked = []
                for i in range(range_checkboxes):
                    # check
                    for j in range(10):
                        try:
                            checkboxes[current_checkbox].click()
                            list_last_checked.append(checkboxes[current_checkbox])
                            current_checkbox = current_checkbox + 1
                            bar.next()
                        except:
                            pass

                    time.sleep(1)
                    botao_download.click()
                    time.sleep(int(tempo_download))
                    # uncheck
                    for j in range(len(list_last_checked)):
                        list_last_checked[j].click()
                    list_last_checked.clear()

                """"""""""""""""""

                print('\nAguardando por Downloads não concluídos...\nAguarde 10 segundos...')
                time.sleep(10)

                """ PARSING DAS INFOS """
                self.transform_to_data_v2(html=html_inicial_pagina, open_auto=open_auto,
                                          pdf_download_path=browser_download_pdf)

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

                    current_start_date = str(period_to_search[i]).replace('-', '/')
                    current_end_date = str(period_to_search[i + 1]).replace('-', '/')

                    browser.find_element_by_xpath('//input[@id="campoDataArrecadacaoInicial"]').send_keys(
                        current_start_date)
                    browser.find_element_by_xpath('//input[@id="campoDataArrecadacaoFinal"]').send_keys(
                        current_end_date)
                    browser.find_element_by_xpath('//input[@id="botaoConsultar"]').click()
                    time.sleep(5)

                    func_selenium.wait_loading(MAXTIME=15, XPATH='//div[@id="conteudo"]', browser=browser)

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
                        time.sleep(5)
                        for j in range(len(new_period_search) - 1):
                            print('Buscando periodo: ', new_period_search[j], new_period_search[j + 1])

                            current_start_date = str(new_period_search[j]).replace('-', '/')
                            current_end_date = str(new_period_search[j + 1]).replace('-', '/')

                            browser.find_element_by_xpath('//input[@id="campoDataArrecadacaoInicial"]').send_keys(
                                current_start_date)
                            browser.find_element_by_xpath('//input[@id="campoDataArrecadacaoFinal"]').send_keys(
                                current_end_date)
                            browser.find_element_by_xpath('//input[@id="botaoConsultar"]').click()

                            time.sleep(5)

                            func_selenium.wait_loading(MAXTIME=15, XPATH='//div[@id="conteudo"]', browser=browser)

                            print('Tentando capturar a tabela ..')

                            # IFRAME SWITCH

                            iframename = 'frmApp'

                            iframe = browser.find_element_by_xpath('//iframe[@id="' + str(iframename) + '"]')

                            browser.switch_to.frame(iframe)
                            self.transform_to_data(html=browser.page_source, open_auto=open_auto)

                            browser.switch_to.default_content()
                            browser.back()
                            time.sleep(8)

                    else:
                        self.transform_to_data(html=browser.page_source, open_auto=open_auto)
                        browser.switch_to.default_content()
                        browser.back()
                        time.sleep(5)


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
        file_errors_location = 'D:\\freela\\robot_six\\lista_tributos.xlsx'

        print(file_errors_location)
        df = pd.read_excel(file_errors_location, engine='openpyxl')
        print(df)

        codigos_imposto = []

        for key, value in df['CODIGO_IMPOSTO'].iteritems():
            if len(str(value)) < 4:
                while len(str(value)) < 4:
                    value = '0' + str(value)

            codigos_imposto.append(str(value))

        tipo_imposto = []

        for key, value in df['TIPO_IMPOSTO'].iteritems():
            tipo_imposto.append(value)

        print(len(codigos_imposto))
        print(len(tipo_imposto))

        tributos_dict = []

        for i in range(len(codigos_imposto)):
            tributos_dict.append({
                'codigo': str(codigos_imposto[i]),
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

    def transform_to_data(self, html, open_auto=False):

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
            self.save_table(data=data, columns=custom_columns, open_auto=open_auto)

    def pdf_to_text(self, path):
        """
        Function responsible for parse pdf to text.
        :param path:
        :return:
        """
        raw = tikaparser.from_file(path)
        text = raw['content']

        try:
            os.remove(path=path)
        except:
            pass

        return text

    def parse_pdf(self, pdf_text):

        list_tributos = []

        cards = pdf_text.split('Data de Vencimento')

        json_cars = []

        for i in range(len(cards) - 1):
            try:
                documento_id = None
                principal = None
                multa = None
                juros = None
                total = None

                current_card = cards[i + 1]

                documento_id = current_card.split('\nCNPJ\n')[0].split(' ')

                documento_id = str(documento_id[len(documento_id) - 1]).strip()

                cards_numeros = current_card.split('\nComprovante emitido às')[0].split('\nTotais ')[1]

                principal = cards_numeros.split(' ')[0]
                multa = cards_numeros.split(' ')[1]
                juros = cards_numeros.split(' ')[2]
                total = cards_numeros.split(' ')[3]

                """print('\n\n------------- \n\n')

                print(current_card)
                print('\n----TEXTTOPARSE------ \n')
                print('Num doc extraido: ', documento_id)
                print('Valor Principal: ', principal)
                print('Valor Multa: ', multa)
                print('Valor Juros: ', juros)
                print('Valor Total: ', total)"""

                current_file = {
                    "documento": str(documento_id.replace(' ', '').replace('\n', '')),
                    "principal": float(principal.replace(' ', '').replace('\n', '').replace(".", "").replace(",", ".")),
                    "multa": float(multa.replace(' ', '').replace('\n', '').replace(".", "").replace(",", ".")),
                    "juros": float(juros.replace(' ', '').replace('\n', '').replace(".", "").replace(",", ".")),
                    "total": float(total.replace(' ', '').replace('\n', '').replace(".", "").replace(",", "."))
                }

                json_cars.append(current_file)
            except:
                print('Obteve um erro na extração: valor individual do pdf')

        """print('Finished')
        time.sleep(5415)"""

        return json_cars

    def obtain_values_pdf(self, download_pdf_path):

        pdf_files = glob.glob(str(download_pdf_path) + "\\*.pdf")
        list_pdf_parseds = []
        print('\n')
        bar = progress.bar.ChargingBar(str('Lendo PDFs'), max=len(pdf_files))
        for i in range(len(pdf_files)):
            parsed_pdf = 0
            try:
                text_pdf = self.pdf_to_text(path=pdf_files[i])
                try:
                    parsed_pdf = self.parse_pdf(pdf_text=text_pdf)
                except:
                    print('\nObteve um erro: Não foi possivel extrair as informações do PDF: ', pdf_files[i])
            except:
                print('\nObteve um erro: Não foi possivel transformar PDF para texto: ', pdf_files[i])
            bar.next()

            if len(parsed_pdf) == 0:
                pass
            else:
                list_pdf_parseds = list_pdf_parseds + parsed_pdf

        return list_pdf_parseds

    def transform_to_data_v2(self, html, open_auto=False, pdf_download_path=None):

        values_pdf = self.obtain_values_pdf(download_pdf_path=pdf_download_path)

        print('\nNúmero de Informações de PDFs capturados: ' + str(len(values_pdf)))

        if len(values_pdf) == 0:
            print('\nSalvando da forma padrão')
            self.transform_to_data(html=html, open_auto=open_auto)
        else:

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

                cnpj = params.split('Nome:')[0].split('CNPJ:')[1].strip().replace('.', '').replace('-', '').replace('/',
                                                                                                                    '')

                nome = params.split('Data de Arrecada')[0].split('Nome: ')[1].strip()

                data_arrecadacao = params.split('Faixa de valores:')[0].split('Data de Arrecada')[1].split(':')[
                    1].strip()

                self.save_table_v2(data=data, columns=custom_columns, cnpj=cnpj, nome=nome,
                                   data_arrecadacao=data_arrecadacao,
                                   open_auto=open_auto, values_pdf=values_pdf)

            except:
                self.save_table_v2(data=data, columns=custom_columns, open_auto=open_auto, values_pdf=values_pdf)


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

    if execute_program == 'run_more_data':
        botclass = Projetoecac()

        pdf_download_path = config_functions.path_to_pdf(bot_name=botclass.generate_filename_pdf())
        botclass.run_program_table_iframe_maisdados(browser_download_pdf=pdf_download_path)

    elif execute_program == 'auto_search':
        botclass = Projetoecac()
        botclass.run_program_table_iframe_automated()

    elif 'test_program' in execute_program:
        f = codecs.open("./source/assets/html elementos.html", 'r')
        html = f.read()
        botclass = Projetoecac()
        botclass.transform_to_data(html=html, open_auto=True)

    elif 'testar_program_v2' in execute_program:
        f = codecs.open("./source/assets/html elementos.html", 'r')
        html = f.read()
        botclass = Projetoecac()

        pdf_download_path = config_functions.path_to_pdf(bot_name='testé_pdf')
        print(pdf_download_path)

        botclass.transform_to_data_v2(html=html, open_auto=True, pdf_download_path=pdf_download_path)
        # botclass.run_program_table_iframe_maisdados(browser_download_pdf=pdf_download_path)

    elif 'anothercommand' in execute_program:
        print('anothercommand')

    else:
        print('cannot find a execution script')
