from tools import load_conf, save_conf
from pprint import pprint
import glob
import os
import shutil
from il_supermarket_scarper.scrappers_factory import ScraperFactory
from il_supermarket_scarper.main import ScarpingTask
from il_supermarket_scarper.utils.file_types import FileTypesFilters
from xml_parser import get_root
import pandas as pd
from pathlib import Path

def parse_price_xml(root, provider, tags, ignore, tags_dict, item_info_dict, price_rows):
    """analyse "price item" by going through the xml"""
    if root is None:
        return
    
    have_item_id = False

    for child in root.getchildren():
        if len(child.getchildren()) > 0:
            parse_price_xml(child, provider, tags, ignore, tags_dict, item_info_dict, price_rows)
        else:
            tag = child.tag.lower()
            if tag in ignore:
                continue
            tag_name = tags_dict.get(tag, tag)
            item_info_dict[tag_name] = child.text
            #print(tag_name, child.tag, child.text)
            if tag_name == 'itemcode':
                have_item_id = True
                #print("")


    if have_item_id:
        row = [provider]
        #print(item_info_dict)
        for tag in tags:
            row.append(item_info_dict[tag])
        price_rows.append(row)
        
    return

def download_all_prices(progress_bar=None, force=False):
    """load or create dataframe based on prices from all providers (from all providers) """
    data_prices_path = 'data/prices.csv'
    if os.path.isfile(data_prices_path) and not force:
        if progress_bar:
            progress_bar.value = progress_bar.max/2
        df = pd.read_csv(data_prices_path, low_memory=False)
        if progress_bar:
            progress_bar.value = progress_bar.max
        return df
    
    #collect price_rows from all providers
    price_rows = []
    all_prices = load_conf('conf/all_prices.json')
    (tags, ignore, tags_dict) = (all_prices['tags'], all_prices['ignore'], all_prices['tags_dict'])
    output_folder = "price_data"
    encoding = 'utf-8-sig'
    used_files = []
    failed_files = []
    for scrapper_class in ScraperFactory:
        ScarpingTask(dump_folder_name=output_folder, only_latest=True,
                                        files_types=FileTypesFilters.only_price(),
                                        enabled_scrapers=[scrapper_class],
                                        lookup_in_db=False).start()
        pattern = f'{FileTypesFilters.PRICE_FILE.value["should_contain"]}*.xml'
        scrapper = ScraperFactory.get(scrapper_class)(output_folder)
        data_files = list(file for file in
                            glob.iglob(os.path.join(scrapper.get_storage_path(), pattern)))
        if not data_files:
            print(f'Failed to find file for scrapper {scrapper.chain}')
            return
        print(scrapper.chain, encoding)
        for data_file in data_files:
            used_files.append(data_file)
            root = None
            try:
                root = get_root(data_file, encoding)
            except:
                print('failed to get root of '+data_file)
                failed_files.append(data_file)
                continue
            item_info_dict = {}
            parse_price_xml(root, scrapper.chain, tags, ignore, tags_dict, item_info_dict, price_rows)

        if progress_bar:
            progress_bar.value += 1
        shutil.rmtree(output_folder)
    if failed_files:
        print('failed files:')
        pprint(failed_files)

    #create dataframe based on price_rows
    header = ['provider'] + all_prices['tags']
    df = pd.DataFrame(price_rows, columns=header)
    filepath = Path(data_prices_path)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath, index=False)
    return df