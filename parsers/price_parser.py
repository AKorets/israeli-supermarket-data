from pprint import pprint
import glob
import os
import shutil
from pathlib import Path
from typing import Any
from dataclasses import dataclass
from il_supermarket_scarper.scrappers_factory import ScraperFactory
from il_supermarket_scarper.main import ScarpingTask
from il_supermarket_scarper.utils.file_types import FileTypesFilters
from il_supermarket_scarper.utils import Logger
import pandas as pd
from tools import load_conf
from .xml_parser import get_root, parse_item_xml

PRICE_ENCODING = 'utf-8-sig'

@dataclass
class DownloadTypeData:
    """Info for ScarpingTask and find the files inside"""
    pattern: str
    files_types: Any

def enumerate_scrapper_with_files(output_folder,
                                    download_type_data:DownloadTypeData=None):
    """usage for scrapper, data_files in enumerate_scrapper_with_files(output_folder)"""
    if download_type_data is None:
        pattern = f'{FileTypesFilters.PRICE_FILE.value["should_contain"]}*.xml'
        files_types = FileTypesFilters.only_price()
        download_type_data = DownloadTypeData(pattern, files_types)
    for scrapper_class in ScraperFactory:
        ScarpingTask(dump_folder_name=output_folder, only_latest=True,
                                        files_types=download_type_data.files_types,
                                        enabled_scrapers=[scrapper_class],
                                        lookup_in_db=False).start()
        pattern = download_type_data.pattern
        scrapper = ScraperFactory.get(scrapper_class)(output_folder)
        data_files = list(file for file in
                            glob.iglob(os.path.join(scrapper.get_storage_path(), pattern)))
        yield (scrapper, data_files)

def load_all_prices(data_prices_path = 'data/prices.csv', progress_bar=None):
    """load all prices from data_prices_path"""
    if progress_bar:
        progress_bar.value = progress_bar.max/2
    data_frame = pd.read_csv(data_prices_path, low_memory=False)
    if progress_bar:
        progress_bar.value = progress_bar.max
    return data_frame

def save_all_prices(price_rows, data_prices_path, all_prices):
    """create dataframe based on price_rows"""
    header = ['provider'] + all_prices['tags']
    data_frame = pd.DataFrame(price_rows, columns=header)
    filepath = Path(data_prices_path)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    data_frame.to_csv(filepath, index=False)
    return data_frame

def download_all_promo_prices(progress_bar=None, force=False, output_folder = "promo_data",
                        data_prices_path = 'data/promo.csv',
                        conf='conf/all_promotions.json',
                        download_type_data:DownloadTypeData=None):
    """load or create dataframe based on promo from all providers """
    pattern = f'{FileTypesFilters.PROMO_FILE.value["should_contain"]}*.xml'
    files_types = FileTypesFilters.only_promo()
    download_type_data = DownloadTypeData(pattern, files_types)
    download_all_prices(progress_bar, force, output_folder,
                        data_prices_path, conf, download_type_data)

def parse_item_xml_extension(root, chain_name, all_prices, item_info_dict,
                             price_rows, stop_tag):
    """wrapper around parse_item_xml, to reduce number of download_all_prices variables"""
    (tags, ignore, tags_dict) = (all_prices['tags'], all_prices['ignore'], all_prices['tags_dict'])
    parse_item_xml(root, chain_name, tags, ignore, tags_dict,
                        item_info_dict, price_rows, stop_tag)

def download_all_prices(progress_bar=None, force=False,
                        output_folder = "price_data",
                        data_prices_path = 'data/prices.csv',
                        conf='conf/all_prices.json',
                        download_type_data:DownloadTypeData=None):
    """load or create dataframe based on prices from all providers (from all providers) """
    if os.path.isfile(data_prices_path) and not force:
        return load_all_prices(data_prices_path, progress_bar)

    #collect price_rows from all providers
    price_rows = []
    all_prices = load_conf(conf)
    failed_files = []
    for scrapper, data_files in enumerate_scrapper_with_files(output_folder, download_type_data):
        if not data_files:
            print(f'Failed to find file for scrapper {scrapper.chain}')
            continue
        print(scrapper.chain, PRICE_ENCODING)
        for data_file in data_files:
            root = get_root(data_file, PRICE_ENCODING)
            if root is None:
                print('failed to get root of '+data_file)
                failed_files.append(data_file)
                continue
            Logger.info(f"Parsing file : {data_file}")
            item_info_dict = {}
            parse_item_xml_extension(root, scrapper.chain, all_prices, item_info_dict,
                                     price_rows, 'itemcode')

        if progress_bar:
            progress_bar.value += 1
        shutil.rmtree(output_folder)
    if failed_files:
        print('failed files:')
        pprint(failed_files)

    return save_all_prices(price_rows, data_prices_path, all_prices)
