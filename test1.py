from pprint import pprint
import codecs
import shutil
from il_supermarket_scarper.main import ScarpingTask
from il_supermarket_scarper.scrappers_factory import ScraperFactory
from il_supermarket_scarper.utils.file_types import FileTypesFilters
from tools import save_conf
from store_parser import analyse_store_folder

def download_store_data(output_folder):
    """download store data from providers"""
    scrapper_done = ScarpingTask(dump_folder_name=output_folder, only_latest=True,
                                    files_types=[FileTypesFilters.STORE_FILE.name]).start()
    print(scrapper_done)

def create_all_stores_data():
    """create unified store data inside all_stores.json"""
    all_scrapers = ScraperFactory.all_scrapers()
    output_folder = "data"
    download_store_data(output_folder)
    #print([repr(s) for s in all_scrapers])
    scrappers = [s(output_folder) for s in all_scrapers]
    #mapper_prototype(output_folder)

    stores_data = {}
    total_stores = 0
    for scrapper in scrappers:
        total_stores += analyse_store_folder(scrapper.get_storage_path(),
                                                scrapper.chain, stores_data)
        #break

    conf_path = 'conf/all_stores.json'
    print(f'Save all stores to {conf_path} total_stores:{total_stores}'+
                            f' uniqueStores:{len(stores_data)}')
    save_conf(conf_path, stores_data)
    with codecs.open('all_stores_output.txt', 'w', encoding='utf-16', errors="ignore") as file:
        pprint(stores_data, file)

    shutil.rmtree(output_folder)

if __name__ == "__main__":
    create_all_stores_data()
