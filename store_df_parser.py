import glob
import os
import shutil
from pathlib import Path
from pprint import pprint
import pandas as pd
from il_supermarket_scarper.main import ScarpingTask
from il_supermarket_scarper.scrappers_factory import ScraperFactory
from il_supermarket_scarper.utils.file_types import FileTypesFilters
from tools import load_conf
from xml_parser import get_root, parse_item_xml


def load_all_stores(data_stores_path = 'data/stores.csv', progress_bar=None):
    """load all prices from data_stores_path"""
    if progress_bar:
        progress_bar.value = progress_bar.max/2
    data_frame = pd.read_csv(data_stores_path)
    if progress_bar:
        progress_bar.value = progress_bar.max
    return data_frame

def enumerate_scrapper_with_files(output_folder, all_stores):
    """usage for scrapper, data_files in enumerate_scrapper_with_files(output_folder)"""
    ignore_file_dict = all_stores['ignore_file_dict']
    for scrapper_class in ScraperFactory:
        ScarpingTask(dump_folder_name=output_folder, only_latest=True,
                                        files_types=[FileTypesFilters.STORE_FILE.name],
                                        enabled_scrapers=[scrapper_class],
                                        lookup_in_db=False).start()
        pattern = f'{FileTypesFilters.STORE_FILE.value["should_contain"]}*.xml'
        scrapper = ScraperFactory.get(scrapper_class)(output_folder)
        data_files = list(file for file in
                            glob.iglob(os.path.join(scrapper.get_storage_path(), pattern)))
        if scrapper.chain in ignore_file_dict:
            file_part = ignore_file_dict[scrapper.chain]
            data_files = [file for file in data_files if file_part not in file]
        if not data_files:
            print(f'Failed to find file for scrapper {scrapper.chain}')
            continue
        yield (scrapper, data_files)

def save_all_stores(store_rows, data_stores_path, tags):
    """create dataframe based on store_rows"""
    header = ['provider'] + tags
    data_frame = pd.DataFrame(store_rows, columns=header)
    filepath = Path(data_stores_path)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    data_frame.to_csv(filepath, index=False)
    return data_frame

def parse_item_xml_extension(root, chain_name, all_stores, item_info_dict, store_rows, stop_tag):
    """wrapper around parse_item_xml, to reduce number of download_all_stores variables"""
    (tags, ignore, tags_dict) = (all_stores['tags'], all_stores['ignore'], all_stores['tags_dict'])
    parse_item_xml(root, chain_name, tags, ignore, tags_dict,
                                item_info_dict, store_rows, stop_tag)

def advance_progress_bar(progress_bar):
    """handle advance progress bar logic"""
    if progress_bar:
        progress_bar.value += 1

def download_all_stores(progress_bar=None, force=False, output_folder = "stores_data",
                        data_stores_path = 'data/stores.csv'):
    """load or create dataframe based on stores from all providers """
    if os.path.isfile(data_stores_path) and not force:
        return load_all_stores(data_stores_path, progress_bar)

    #collect store_rows from all providers
    store_rows = []
    all_stores = load_conf('conf/all_df_stores.json')
    encodings = all_stores['encoding']
    failed_files = []
    for scrapper, data_files in enumerate_scrapper_with_files(output_folder, all_stores):
        print(scrapper.chain, encodings[scrapper.chain])
        for data_file in data_files:
            root = get_root(data_file, encodings[scrapper.chain])
            if root is None:
                failed_files.append(data_file)
                continue
            item_info_dict = {}
            parse_item_xml_extension(root, scrapper.chain, all_stores,
                                item_info_dict, store_rows, 'storeid')

        advance_progress_bar(progress_bar)
        shutil.rmtree(output_folder)

    if failed_files:
        print('failed files:')
        pprint(failed_files)

    return save_all_stores(store_rows, data_stores_path, all_stores['tags'])
