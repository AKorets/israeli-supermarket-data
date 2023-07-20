from store_parser import download_all_stores
from tools import load_conf
import re

def test_online_list():
    download_all_stores()
    url_list = set()
    stores_data = load_conf('conf/all_stores.json')
    for key in stores_data:
        address = stores_data[key]['Address']
        if address and 'co.il' in address.lower():
            url_list.add(re.findall("www.*.il",address.lower())[0])
    expected_urls = {'www.shufersal.co.il', 'www.rami-levy.co.il', 'www.carrefour.co.il',
                     'www.m2000.co.il', 'www.keshet-teamim.co.il', 'www.shukcity.co.il',
                     'www.edenteva.co.il', 'www.ybitan.co.il', 'www.mega.co.il', 'www.tivtaam.co.il'}
    difference = url_list ^ expected_urls
    assert not difference
