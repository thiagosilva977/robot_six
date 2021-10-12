import json
import os
from pathlib import Path


def read_custom_configs():
    """
    This function gets custom configs.
    :return: dict
    """
    current_path = Path(__file__).parent.parent.parent
    string_path = str(current_path) + '/configuracoes_programa.json'

    # Getting credentials
    with open(Path(string_path), 'r') as myfile:
        credential_json = json.load(myfile)

    json_inputs = {
        'input_pasta': credential_json['PASTAS_FUNCIONAMENTO']['PASTA_DOWNLOAD_ARQUIVOS'],
        'start_date': credential_json['BUSCA_AUTOMATIZADA']['DATA_INICIO'],
        'end_date': credential_json['BUSCA_AUTOMATIZADA']['DATA_FIM'],
        'abrir_auto': credential_json['CONTROLE']['ABRIR_AUTOMATICAMENTE_XLSX'],

    }
    return json_inputs


def create_paths(bot_name='default'):
    """
    Creates default download path.
    :param bot_name:
    :return: path to downloads
    """
    REPOSITORY_PATH = Path(__file__).parent.parent.parent

    download_path = Path(str(REPOSITORY_PATH) + "/source/working_directory")
    if not os.path.exists(os.path.dirname(download_path)):
        os.mkdir(os.path.dirname(download_path))

    download_path = Path(str(REPOSITORY_PATH) + "/source/working_directory/test.txt")
    if not os.path.exists(os.path.dirname(download_path)):
        os.mkdir(os.path.dirname(download_path))

    download_path = Path(str(REPOSITORY_PATH) + "/source/working_directory/downloads/test.txt")
    if not os.path.exists(os.path.dirname(download_path)):
        os.mkdir(os.path.dirname(download_path))

    download_path = Path(str(REPOSITORY_PATH) + "/source/working_directory/downloads/" + bot_name + "/test.txt")
    if not os.path.exists(os.path.dirname(download_path)):
        os.mkdir(os.path.dirname(download_path))

    download_path = Path(str(REPOSITORY_PATH) + "/source/working_directory/downloads/" + bot_name)

    return download_path


def organize_custom_path(bot_name='default',cnpj='desconhecido'):
    """
    Creates default download path.
    :param cnpj:
    :param bot_name:
    :return: path to downloads
    """
    REPOSITORY_PATH = read_custom_configs()

    custom_download_path = REPOSITORY_PATH.get('input_pasta')

    download_path = Path(str(custom_download_path) + '/' + bot_name + "/test.txt")
    if not os.path.exists(os.path.dirname(download_path)):
        os.mkdir(os.path.dirname(download_path))

    custom_download_path = Path(str(custom_download_path) + '/' + bot_name)


    download_path = Path(str(custom_download_path) + '/' + cnpj + "/test.txt")
    if not os.path.exists(os.path.dirname(download_path)):
        os.mkdir(os.path.dirname(download_path))

    download_path = Path(str(custom_download_path) + '/' + cnpj)

    return download_path
