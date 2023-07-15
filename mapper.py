# -*- coding: utf-8 -*-
"""
Created on Fri Jan 06 23:06:51 2017

Mapper is a class that can help you, to analyse the xml first time,
The class is printing python table code, to the output

@author: avi k
"""
import glob
import os
import shutil
import il_supermarket_scarper.scrappers as all_scrappers
from il_supermarket_scarper.utils.file_types import FileTypesFilters
from il_supermarket_scarper.main import ScarpingTask
from store_parser import get_root, generate_store_dictionary
from store_parser import generate_store_dictionary_lower_case, save_store_conf



class Mapper:
    """class that creates mapper from original xml files to unified xml (in stores and items)"""
    def __init__(self):
        pass

    def all_value_tags(self, root, tag_set):
        """collect all tag names that doesn't have children (tag that contains only value)"""
        if root is None:
            return
        if len(root.getchildren())==0:
            tag_set.add(root.tag)
            return
        for child in root.getchildren():
            self.all_value_tags(child, tag_set)


    def smart_print(self, root, ignore_dict, name_dict):
        """search and print tags that doesn't support by ignore or 'name dict' dictionaries"""
        name_dict = name_dict.copy()
        tag_set = set()
        self.all_value_tags(root, tag_set)
        unknown = []
        for tag_name in tag_set:
            if tag_name in ignore_dict:
                continue
            if tag_name in name_dict:
                del name_dict[tag_name]
            else:
                unknown.append(tag_name)
                continue
        if unknown:
            print (f'Unknown {unknown}')
            return False
        if name_dict:
            print(f'still existing values in name_dict {name_dict}')
            return False

        return True


    def parse_items(self, xml_path, name_dict, ignore_dict, encoding="utf-8"):
        """parse items xml, and create report which xml tag still unsupported"""

        #d = {'InternalChainId':'name','LastUpdateDate':'name', 'StoreId':'name' ,
        #            'BikoretNo':'name','StoreType':'name','StoreName':'name',
        #            'Address':'name' , 'City':'name' , 'ZipCode':'name'}

        print ('choose  , ', ",".join(iter(name_dict)))
        root = get_root(xml_path, encoding)

        self.smart_print(root, ignore_dict, name_dict)

    def parse_store(self, xml_path, name_dict, ignore_dict, encoding="utf-8"):
        """parse store xml, and create report which xml tag still unsupported"""
        #func_dict = {'LastUpdateDate':'parseStoreUpdateDate','InternalChainId':'parseIChainId',
        #            'StoreName':'parseText','Address':'parseText','City':'parseText',
        #            'ZipCode':'parseText'}
        #index_dict = {'InternalChainId':0,'LastUpdateDate':1, 'StoreId':2 , 'BikoretNo':3,
        #                'StoreType':4,'StoreName':5,'Address':6 , 'City':7 , 'ZipCode':8}
        root = get_root(xml_path, encoding)

        if self.smart_print(root, ignore_dict, name_dict):
            print (f'The format of {xml_path} is parsed')

def delete_files(path, pattern):
    """delete files by pattern"""
    for file in glob.iglob(os.path.join(path, pattern)):
        os.remove(file)

def generate_conf(scrapper, my_mapper, name_dict, ignore_dict,
                    encoding, ignore_file='ignore'):
    """generate store configuration from name dictionary and xml dictionary and other parameter"""
    delete_files(scrapper.get_storage_path(), ignore_file+'*.xml')
    pattern = f'{FileTypesFilters.STORE_FILE.value["should_contain"]}*.xml'
    data_files = list(file for file in
                        glob.iglob(os.path.join(scrapper.get_storage_path(), pattern)))
    if not data_files:
        print(f'Failed to find file for scrapper {scrapper.chain}')
        return
    my_mapper.parse_store(data_files[0], name_dict, ignore_dict, encoding)
    conf_path = save_store_conf(scrapper.chain, encoding, name_dict, ignore_dict, ignore_file)
    print(f'Saving to     {conf_path}\n')

def generate_stores_configurations(output_folder):
    """generate all stores configuration in conf folder"""

    my_mapper = Mapper()

    names = generate_store_dictionary()
    ignore = ['Latitude','Longitude','ChainName','SubChainName', 'Branches', 'XmlDocVersion',
                'SubChains', 'LastUpdateTime']
    generate_conf(all_scrappers.Bareket(output_folder), my_mapper,
                    names, ignore, "utf-8")

    names = generate_store_dictionary_lower_case()
    generate_conf(all_scrappers.DorAlon(output_folder), my_mapper,
                    names, ignore, "utf-16")

    generate_conf(all_scrappers.GoodPharm(output_folder), my_mapper,
                    names, ignore, "utf-8")

    generate_conf(all_scrappers.HaziHinam(output_folder), my_mapper,
                    names, ignore, 'UTF-16')

    generate_conf(all_scrappers.Keshet(output_folder), my_mapper,
                    names, ignore, 'UTF-16')

    generate_conf(all_scrappers.KingStore(output_folder), my_mapper,
                    names, ignore, 'UTF-8')

    generate_conf(all_scrappers.Maayan2000(output_folder), my_mapper,
                    names, ignore, 'UTF-8')

    names = generate_store_dictionary()
    generate_conf(all_scrappers.MahsaniAShuk(output_folder), my_mapper,
                    names, ignore, 'UTF-8')

    names = generate_store_dictionary_lower_case()
    generate_conf(all_scrappers.Mega(output_folder), my_mapper,
                    names, ignore, 'UTF-16')

    generate_conf(all_scrappers.MegaMarket(output_folder), my_mapper,
                    names, ignore, 'UTF-16')

    generate_conf(all_scrappers.NetivHasef(output_folder), my_mapper,
                    names, ignore, 'UTF-8')

    generate_conf(all_scrappers.Osherad(output_folder), my_mapper,
                    names, ignore, 'UTF-16')

    generate_conf(all_scrappers.Polizer(output_folder), my_mapper,
                    names, ignore, 'UTF-16')

    generate_conf(all_scrappers.RamiLevy(output_folder), my_mapper,
                    names, ignore, 'UTF-16', 'storesfull')

    #names = generate_store_dictionary_lower_case()
    #my_mapper.parseStore('data/Rami Levy/storesfull7290058140886-000-202303150655.xml',
    #                      d, ignore, 'UTF-8')

    generate_conf(all_scrappers.SalachDabach(output_folder), my_mapper,
                     names, ignore, 'UTF-16')

    names = generate_store_dictionary_lower_case()
    generate_conf(all_scrappers.ShefaBarcartAshem(output_folder), my_mapper,
                    names, ignore, 'UTF-8')

    shufersal_ignore = ['SUBCHAINNAME', 'CHAINNAME']
    names = {'SUBCHAINID':'SubChainID','CHAINID':'ChainID','LASTUPDATEDATE':'LastUpdateDate',
            'STOREID':'StoreID' , 'BIKORETNO':'BikoretNo','STORETYPE':'StoreType',
            'STORENAME':'StoreName','ADDRESS':'Address' , 'CITY':'City' , 'ZIPCODE':'ZIPCode'}
    generate_conf(all_scrappers.Shufersal(output_folder), my_mapper,
                    names, shufersal_ignore, 'UTF-8-sig')

    names = generate_store_dictionary_lower_case()
    generate_conf(all_scrappers.ShukAhir(output_folder), my_mapper,
                    names, ignore, 'UTF-8')

    generate_conf(all_scrappers.StopMarket(output_folder), my_mapper,
                    names, ignore, 'UTF-16')

    generate_conf(all_scrappers.SuperPharm(output_folder), my_mapper,
                    names, ignore, 'ISO-8859-8')

    generate_conf(all_scrappers.SuperYuda(output_folder), my_mapper,
                    names, ignore, 'UTF-8')

    generate_conf(all_scrappers.TivTaam(output_folder), my_mapper,
                    names, ignore, 'UTF-16')

    names = generate_store_dictionary()
    generate_conf(all_scrappers.Victory(output_folder), my_mapper,
                    names, ignore, 'UTF-8')

    names = generate_store_dictionary_lower_case()
    generate_conf(all_scrappers.YaynotBitan(output_folder), my_mapper,
                    names, ignore, 'UTF-16')

    generate_conf(all_scrappers.Yellow(output_folder), my_mapper,
                    names, ignore, 'UTF-16')

    generate_conf(all_scrappers.Yohananof(output_folder), my_mapper,
                    names, ignore, 'UTF-16')

    generate_conf(all_scrappers.ZolVeBegadol(output_folder), my_mapper,
                    names, ignore, 'UTF-8')

def generate_stores_configurations_base():
    """start generate_stores_configurations"""
    output_folder = "data"
    ScarpingTask(dump_folder_name=output_folder, only_latest=True,
                                    files_types=[FileTypesFilters.STORE_FILE.name]).start()
    generate_stores_configurations(output_folder)
    shutil.rmtree(output_folder)

if __name__ == "__main__":
    generate_stores_configurations_base()
