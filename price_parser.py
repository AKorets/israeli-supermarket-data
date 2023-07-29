from pprint import pprint
import glob
import os
import shutil
from pathlib import Path
from il_supermarket_scarper.scrappers_factory import ScraperFactory
from il_supermarket_scarper.main import ScarpingTask
from il_supermarket_scarper.utils.file_types import FileTypesFilters
import pandas as pd
from tools import load_conf
from xml_parser import get_root, parse_item_xml

PRICE_ENCODING = 'utf-8-sig'

def enumerate_scrapper_with_files(output_folder):
    """usage for scrapper, data_files in enumerate_scrapper_with_files(output_folder)"""
    for scrapper_class in ScraperFactory:
        ScarpingTask(dump_folder_name=output_folder, only_latest=True,
                                        files_types=FileTypesFilters.only_price(),
                                        enabled_scrapers=[scrapper_class],
                                        lookup_in_db=False).start()
        pattern = f'{FileTypesFilters.PRICE_FILE.value["should_contain"]}*.xml'
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

def download_all_prices(progress_bar=None, force=False, output_folder = "price_data",
                        data_prices_path = 'data/prices.csv'):
    """load or create dataframe based on prices from all providers (from all providers) """
    if os.path.isfile(data_prices_path) and not force:
        return load_all_prices(data_prices_path, progress_bar)

    #collect price_rows from all providers
    price_rows = []
    all_prices = load_conf('conf/all_prices.json')
    (tags, ignore, tags_dict) = (all_prices['tags'], all_prices['ignore'], all_prices['tags_dict'])
    failed_files = []
    for scrapper, data_files in enumerate_scrapper_with_files(output_folder):
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
            item_info_dict = {}
            parse_item_xml(root, scrapper.chain, tags, ignore, tags_dict,
                                item_info_dict, price_rows, 'itemcode')

        if progress_bar:
            progress_bar.value += 1
        shutil.rmtree(output_folder)
    if failed_files:
        print('failed files:')
        pprint(failed_files)

    return save_all_prices(price_rows, data_prices_path, all_prices)
