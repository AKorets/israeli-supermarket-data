# -*- coding: utf-8 -*-
"""
Used to parse all store file formats
@author: Avi
"""
import codecs
from lxml import objectify
from tools import save_conf

def get_root(xml_file, encoding):
    """get store xml root, in lxml format"""
    with codecs.open(xml_file, encoding=encoding, errors="ignore") as store_file:
        xml = store_file.read()
        #print(xml[:90])
        xml = xml.replace('<?xml version="1.0" encoding="ISO-8859-8" standalone="no" ?>\r\n','')
        xml = xml.encode("UTF-16")

    return objectify.fromstring(xml)

def save_store_conf(chain_name, data):
    """save store configuration"""
    conf_path = f'conf/{chain_name}Store.json'
    save_conf(conf_path, data)
    return conf_path

def generate_store_dictionary():
    """generate store dictionary for xml that contains upercase names"""
    return {'SubChainID':'SubChainID', 'ChainID':'ChainID','LastUpdateDate':'LastUpdateDate',
            'StoreID':'StoreID', 'BikoretNo':'BikoretNo','StoreType':'StoreType',
            'StoreName':'StoreName','Address':'Address', 'City':'City' , 'ZIPCode':'ZipCode'}

def generate_store_dictionary_lower_case():
    """generate store dictionary for xml that contains lower names"""
    return {'SubChainId':'SubChainID', 'ChainId':'ChainID','LastUpdateDate':'LastUpdateDate',
            'StoreId':'StoreID', 'BikoretNo':'BikoretNo','StoreType':'StoreType',
            'StoreName':'StoreName','Address':'Address', 'City':'City' , 'ZipCode':'ZipCode'}
