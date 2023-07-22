# -*- coding: utf-8 -*-
"""
Used to parse all store file formats
@author: Avi
"""
import codecs
import os
import shutil
from lxml import objectify
from il_supermarket_scarper.main import ScarpingTask
from il_supermarket_scarper.scrappers_factory import ScraperFactory
from il_supermarket_scarper.utils.file_types import FileTypesFilters
from tools import save_conf, load_conf

def get_root(xml_file, encoding):
    """get store xml root, in lxml format"""
    with codecs.open(xml_file, encoding=encoding, errors="ignore") as store_file:
        xml = store_file.read()
        #print(xml[:90])
        xml = xml.replace('<?xml version="1.0" encoding="ISO-8859-8" standalone="no" ?>\r\n','')
        xml = xml.encode("UTF-16")

    return objectify.fromstring(xml)

def save_store_conf(chain_name, encoding, name_dict, ignore_dict, ignore_file):
    """save store configuration"""
    conf_path = f'conf/{chain_name}Store.json'
    data = {
        "encoding": encoding,
        "nameDict":name_dict,
        "ignore":ignore_dict,
        "ignoreFile":ignore_file
    }
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

def get_store_conf_path(chain_name):
    """get store configuration path"""
    return f'conf/{chain_name}Store.json'

def analyse_store(conf, file, stores_data, provider_name):
    """analyse store using given configuration path"""
    root = get_root(file, conf['encoding'])
    store_data = {'ProviderName':provider_name}
    store_count = analyse_store_xml(root, store_data, conf['nameDict'], conf['ignore'], stores_data)
    return store_count

def analyse_store_xml(root, tag_dict, tag_name_dict, ignore, stores_data):
    """analyse store by going through the xml"""
    if root is None:
        return 0

    have_store_id = False
    store_count = 0

    for child in root.getchildren():
        if len(child.getchildren()) > 0:
            store_count += analyse_store_xml(child, tag_dict, tag_name_dict, ignore, stores_data)
        else:
            if child.tag in ignore:
                continue
            tag_name = tag_name_dict[child.tag]
            #print(tag_name, child.tag, child.text)
            tag_dict[tag_name] = child.text
            if tag_name == 'StoreID':
                have_store_id = True
                #print("")

    if have_store_id:
        key = f'{tag_dict["ChainID"]}_{tag_dict["SubChainID"]}_{tag_dict["StoreID"]}'
        stores_data[key] = tag_dict.copy()
        store_count += 1
    return store_count

def analyse_store_folder(folder_path, chain_name, stores_data):
    """returns store count inside the chain name"""
    total_stores = 0
    conf_path = get_store_conf_path(chain_name)
    if os.path.isfile(conf_path):
        store_conf = load_conf(conf_path)
        for file in os.listdir(folder_path):
            if store_conf['ignoreFile'] in file:
                print(f'ignored file {file}')
            else:
                full_path = os.path.join(folder_path, file)
                store_count = analyse_store(store_conf, full_path, stores_data, chain_name)
                total_stores += store_count
                print(f'analysing {full_path} stores:{store_count}')
    else:
        print(f'skipping {chain_name}')
    return total_stores

def clean_city_name(city_name):
    """clean city name"""
    if not city_name:
        return 'None'
    return city_name.replace('-',' ')

def download_all_stores(progress_bar=None, force=False):
    """create unified store data inside all_stores.json"""
    all_stores_path = 'conf/all_stores.json'
    if os.path.isfile(all_stores_path) and not force:
        stores_data = load_conf(all_stores_path)
        return stores_data

    if progress_bar:
        progress_bar.value = progress_bar.max
    output_folder = "data"
    for scrapper in ScraperFactory:
        ScarpingTask(dump_folder_name=output_folder, only_latest=True,
                                        files_types=[FileTypesFilters.STORE_FILE.name],
                                        enabled_scrapers=[scrapper],
                                        lookup_in_db=False).start()
        if progress_bar:
            progress_bar.value += 1

    all_scrapers = ScraperFactory.all_scrapers()
    scrappers = [s(output_folder) for s in all_scrapers]
    stores_data = {}
    total_stores = 0
    for scrapper in scrappers:
        total_stores += analyse_store_folder(scrapper.get_storage_path(),
                                                scrapper.chain, stores_data)
    save_conf(all_stores_path, stores_data)
    shutil.rmtree(output_folder)
    return stores_data

def get_city_stat(progress_bar=None):
    """get statistics of stores count per city name"""
    stores_data = download_all_stores(progress_bar)
    city_stat = {}
    city_name_correction = load_conf('conf/city_name_correction.json')
    #save_conf('conf/city_name_correction.json', city_name_correction)

    for key in stores_data:
        city_name_temp = stores_data[key]['City']
        city_name_temp = clean_city_name(city_name_temp)
        city_name = city_name_correction.get(city_name_temp, city_name_temp)
        city_stat[city_name] = city_stat.get(city_name, 0) + 1
    #city_stat_sorter = sorted(city_stat.items(), key=lambda x:x[1])
    return city_stat
