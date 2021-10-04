import datetime
import hashlib
import json
from pathlib import Path
from unicodedata import normalize


def remove_special_characters(text):
    """Remove special characters in some text
    :returns str """
    return normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')


def create_hash_id(var1,var2):
    """
    This function creates HASH ID to use in database table column.
    :return: hash id MD5 32 char
    """

    string_hashcode = str(var1) + str(var2)
    hash_id = hashlib.md5(string_hashcode.encode("utf-8")).hexdigest()

    return hash_id


def parse_state_to_uf(estado):
    """
    Transforms some state name to UF
    :param estado: state to transform
    :return: UF
    """
    estado = estado.upper()
    var = {
        'AC': 'ACRE',
        'AL': 'ALAGOAS',
        'AP': 'AMAPÁ',
        'AM': 'AMAZONAS',
        'BA': 'BAHIA',
        'CE': 'CEARÁ',
        'DF': 'DISTRITO FEDERAL',
        'ES': 'ESPÍRITO SANTO',
        'GO': 'GOIÁS',
        'MA': 'MARANHÃO',
        'MT': 'MATO GROSSO',
        'MS': 'MATO GROSSO DO SUL',
        'MG': 'MINAS GERAIS',
        'PA': 'PARÁ',
        'PB': 'PARAÍBA',
        'PR': 'PARANÁ',
        'PE': 'PERNAMBUCO',
        'PI': 'PIAUÍ',
        'RJ': 'RIO DE JANEIRO',
        'RN': 'RIO GRANDE DO NORTE',
        'RS': 'RIO GRANDE DO SUL',
        'RO': 'RONDÔNIA',
        'RR': 'RORAIMA',
        'SC': 'SANTA CATARINA',
        'SP': 'SÃO PAULO',
        'SE': 'SERGIPE',
        'TO': 'TOCANTINS'
    }
    if estado in var.values():
        uf = (list(var.keys())[list(var.values()).index(estado)])
    else:
        uf = estado

    return uf


def parse_empty(value):
    if value == '' or value == '{}' or value == ' ' or value == 'None' or value is None:
        return None
    else:
        return value


def print_dict_items(_dict):
    for k, v in _dict.items():
        print(k, ' || ', v)


def left_split_dot(string):
    try:
        string = string.split('.')[0]
    except:
        pass
    return string
