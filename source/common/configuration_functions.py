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
        'input_pasta': credential_json['PASTA_DE_DOWNLOADS'],

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
