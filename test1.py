
from il_supermarket_scarper.main import ScarpingTask
from il_supermarket_scarper.scrappers_factory import ScraperFactory
from il_supermarket_scarper.utils.file_types import FileTypesFilters

if __name__ == "__main__":
    expected = ScraperFactory.all_scrapers_name()
    output_folder = "data"
    scrapper_done = ScarpingTask(dump_folder_name=output_folder, only_latest=True, files_types=[FileTypesFilters.STORE_FILE.name], lookup_in_db=False).start()
    print(scrapper_done)
    folders_from_scraper = list(map(lambda x: x.split("/")[1], scrapper_done))

    time.sleep(5)
    folders_in_dump_folder = os.listdir(output_folder)
    folders_in_dump_folder = [
        name for name in folders_in_dump_folder if not name.startswith(".")
    ]
    assert len(folders_in_dump_folder) == len(expected)
    assert sorted(folders_from_scraper) == sorted(folders_in_dump_folder)

    shutil.rmtree(output_folder)