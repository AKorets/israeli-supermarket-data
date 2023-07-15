# -*- coding: utf-8 -*-
"""
Created on Fri Jan 06 23:06:51 2017

Mapper is a class that can help you, to analyse the xml first time,
The class is printing python table code, to the output

@author: avi k
"""
import il_supermarket_scarper.scrappers as all_scrappers
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


def generate_conf(scrapper, my_mapper, xml_path, name_dict, ignore_dict,
                    encoding, ignore_file='ignore'):
    """generate store configuration from name dictionary and xml dictionary and other parameter"""
    my_mapper.parse_store(xml_path, name_dict, ignore_dict, encoding)
    data = {
        "encoding": encoding,
        "nameDict":name_dict,
        "ignore":ignore_dict,
        "ignoreFile":ignore_file
    }
    conf_path = save_store_conf(scrapper.chain, data)
    print(f'Saving to    {conf_path}\n')

def generate_stores_configurations1():
    """generate all stores configuration in conf folder"""

    my_mapper = Mapper()
    output_folder = "data"

    names = generate_store_dictionary()
    ignore = ['Latitude','Longitude','ChainName','SubChainName', 'Branches', 'XmlDocVersion',
                'SubChains', 'LastUpdateTime']
    generate_conf(all_scrappers.Bareket(output_folder), my_mapper,
                    'data/bareket/StoresFull7290875100001-000-202307130502-000.xml',
                    names, ignore, "utf-8")

    names = generate_store_dictionary_lower_case()
    generate_conf(all_scrappers.DorAlon(output_folder), my_mapper,
                    'data/Dor Alon/Stores7290492000005-202307130200.xml',names , ignore, "utf-16")

    generate_conf(all_scrappers.GoodPharm(output_folder), my_mapper,
                    'data/GoodPharm/StoresFull7290058197699-000-202307131301.xml',names ,
                    ignore, "utf-8")

    generate_conf(all_scrappers.HaziHinam(output_folder), my_mapper,
                    'data/Hazi Hinam/Stores7290700100008-202307130505.xml',names ,
                    ignore, 'UTF-16')

    generate_conf(all_scrappers.Keshet(output_folder), my_mapper,
                    'data/Keshet Taamim/Stores7290785400000-202307131810.xml',names ,
                    ignore, 'UTF-16')

    generate_conf(all_scrappers.KingStore(output_folder), my_mapper,
                    'data/King Store/StoresFull7290058108879-000-202307131001.xml',names ,
                    ignore, 'UTF-8')

    generate_conf(all_scrappers.Maayan2000(output_folder), my_mapper,
                    'data/Maayan2000/StoresFull7290058159628-000-202307131001.xml',names ,
                    ignore, 'UTF-8')

    names = generate_store_dictionary()
    generate_conf(all_scrappers.MahsaniAShuk(output_folder), my_mapper,
                    'data/mahsani a shuk/StoresFull7290661400001-000-202307130600-000.xml',names ,
                    ignore, 'UTF-8')

    names = generate_store_dictionary_lower_case()
    generate_conf(all_scrappers.Mega(output_folder), my_mapper,
                    'data/mega/Stores7290055700007-202307130001.xml',names ,
                    ignore, 'UTF-16')

    generate_conf(all_scrappers.MegaMarket(output_folder), my_mapper,
                    'data/mega-market/Stores7290055700014-202307130001.xml',names ,
                    ignore, 'UTF-16')

    generate_conf(all_scrappers.NetivHasef(output_folder), my_mapper,
                    'data/Netiv Hasef/StoresFull7290058160839-000-202307130511.xml',names ,
                    ignore, 'UTF-8')

    generate_conf(all_scrappers.Osherad(output_folder), my_mapper,
                    'data/Osher Ad/Stores7290103152017-202307130805.xml',names ,
                    ignore, 'UTF-16')

    generate_conf(all_scrappers.Polizer(output_folder), my_mapper,
                    'data/Polizer/Stores7291059100008-202307130515.xml',names ,
                    ignore, 'UTF-16')

    generate_conf(all_scrappers.RamiLevy(output_folder), my_mapper,
                    'data/Rami Levy/Stores7290058140886-202307110505.xml',names ,
                    ignore, 'UTF-16', 'storesfull')

    #names = generate_store_dictionary_lower_case()
    #my_mapper.parseStore('data/Rami Levy/storesfull7290058140886-000-202303150655.xml',
    #                      d, ignore, 'UTF-8')

    generate_conf(all_scrappers.SalachDabach(output_folder), my_mapper,
                     'data/salachdabach/Stores7290526500006-202307130900.xml',names ,
                     ignore, 'UTF-16')

    names = generate_store_dictionary_lower_case()
    generate_conf(all_scrappers.ShefaBarcartAshem(output_folder), my_mapper,
                    'data/ShefaBarcartAshem/StoresFull7290058134977-000-202307131001.xml',names ,
                    ignore, 'UTF-8')

    shufersal_ignore = ['SUBCHAINNAME', 'CHAINNAME']
    names = {'SUBCHAINID':'SubChainID','CHAINID':'ChainID','LASTUPDATEDATE':'LastUpdateDate',
            'STOREID':'StoreID' , 'BIKORETNO':'BikoretNo','STORETYPE':'StoreType',
            'STORENAME':'StoreName','ADDRESS':'Address' , 'CITY':'City' , 'ZIPCODE':'ZIPCode'}
    generate_conf(all_scrappers.Shufersal(output_folder), my_mapper,
                    'data/Shufersal/Stores7290027600007-000-202307130201.xml',names ,
                    shufersal_ignore, 'UTF-8-sig')

    names = generate_store_dictionary_lower_case()
    generate_conf(all_scrappers.ShukAhir(output_folder), my_mapper,
                    'data/Shuk Ahir/StoresFull7290058148776-000-202307131001.xml',names ,
                    ignore, 'UTF-8')

    generate_conf(all_scrappers.StopMarket(output_folder), my_mapper,
                    'data/Stop Market/Stores7290639000004-202307130730.xml',names ,
                    ignore, 'UTF-16')

    generate_conf(all_scrappers.SuperPharm(output_folder), my_mapper,
                    'data/Super-Pharm/StoresFull7290172900007--202307130200.xml',names ,
                    ignore, 'ISO-8859-8')

    generate_conf(all_scrappers.SuperYuda(output_folder), my_mapper,
                    'data/SuperYuda/StoresFull7290058177776-000-202307131001.xml',names ,
                    ignore, 'UTF-8')

    generate_conf(all_scrappers.TivTaam(output_folder), my_mapper,
                    'data/Tiv Taam/Stores7290873255550-202307130505.xml',names ,
                    ignore, 'UTF-16')

    names = generate_store_dictionary()
    generate_conf(all_scrappers.Victory(output_folder), my_mapper,
                    'data/Victory/StoresFull7290696200003-000-202307130600-000.xml',names ,
                    ignore, 'UTF-8')

    names = generate_store_dictionary_lower_case()
    generate_conf(all_scrappers.YaynotBitan(output_folder), my_mapper,
                    'data/ybitan/Stores7290725900003-202307130001.xml',names ,
                    ignore, 'UTF-16')

    generate_conf(all_scrappers.Yellow(output_folder), my_mapper,
                    'data/Yellow/Stores7290644700005-202307130600.xml',names ,
                    ignore, 'UTF-16')

    generate_conf(all_scrappers.Yohananof(output_folder), my_mapper,
                    'data/Yohananof/Stores7290803800003-202307130100.xml',names ,
                    ignore, 'UTF-16')

    generate_conf(all_scrappers.ZolVeBegadol(output_folder), my_mapper,
                    'data/ZolVeBegadol/StoresFull7290058173198-000-202307130506.xml',names ,
                    ignore, 'UTF-8')

if __name__ == "__main__":
    generate_stores_configurations1()
