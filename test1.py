from il_supermarket_scarper.main import ScarpingTask
from il_supermarket_scarper.utils.file_types import FileTypesFilters
from parsers.store_parser import download_all_stores

def download_store_data(output_folder):
    """download store data from providers"""
    scrapper_done = ScarpingTask(dump_folder_name=output_folder, only_latest=True,
                                    files_types=[FileTypesFilters.STORE_FILE.name]).start()
    print(scrapper_done)
    return True

if __name__ == "__main__":
    download_all_stores()
