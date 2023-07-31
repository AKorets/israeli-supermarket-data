import re
from store_parser import download_all_stores, get_city_stat

def test_online_list():
    """test if list of online stores are same"""
    stores_data = download_all_stores()
    url_list = set()
    for key in stores_data:
        address = stores_data[key]['Address']
        if address and 'co.il' in address.lower():
            url_list.add(re.findall("www.*.il",address.lower())[0])
    expected_urls = {'www.shufersal.co.il',
                     'www.rami-levy.co.il',     #Rami Levy
                     'www.carrefour.co.il',     #mega
                     'www.mega.co.il',          #mega
                     'www.m2000.co.il',         #Maayan2000
                     'www.keshet-teamim.co.il',
                     'www.shukcity.co.il',
                     'www.edenteva.co.il',
                     'www.ybitan.co.il',
                     'www.tivtaam.co.il'        #Tiv Taam
                    }
    difference = url_list ^ expected_urls
    assert not difference

def test_top_cities():
    """test top cities (arranged by store in city count)"""
    city_stat = get_city_stat()
    del city_stat['unknown']
    del city_stat['None']
    city_stat_sorter = sorted(city_stat.items(), key=lambda x:x[1], reverse=True)
    top_city_set = set([k for (k,v) in city_stat_sorter][:8])
    expected_top_city = {'תל אביב יפו',
                         'ירושלים',
                         'חיפה',
                         'באר שבע',
                         'נתניה',
                         'ראשון לציון',
                         'פתח תקווה',
                         'אשדוד'}
    difference = top_city_set ^ expected_top_city
    assert not difference
