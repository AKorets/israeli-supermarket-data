# -*- coding: utf-8 -*-
"""
Used to parse all store file formats
@author: Avi
"""
import codecs
from lxml import objectify

def get_root(xml_file, encoding):
    """get store xml root, in lxml format"""
    with codecs.open(xml_file, encoding=encoding, errors="ignore") as store_file:
        xml = store_file.read()
        #print(xml[:90])
        xml = xml.replace('<?xml version="1.0" encoding="ISO-8859-8" standalone="no" ?>\r\n','')
        if len(xml)==0:
            return None
        xml = xml.encode("UTF-16")

    return objectify.fromstring(xml)

def parse_item_xml(root, provider, tags, ignore, tags_dict, item_info_dict,
                    item_rows, stop_tag):
    """aggregate item (like store or price) to item_rows by going through the xml"""
    if root is None:
        return

    have_stop_tag = False

    for child in root.getchildren():
        if len(child.getchildren()) > 0:
            parse_item_xml(child, provider, tags, ignore, tags_dict, item_info_dict,
                            item_rows, stop_tag)
        else:
            tag = child.tag.lower()
            if tag in ignore:
                continue
            tag_name = tags_dict.get(tag, tag)
            item_info_dict[tag_name] = child.text
            #print(tag_name, child.tag, child.text)
            if tag_name == stop_tag:
                have_stop_tag = True
                #print("")


    if have_stop_tag:
        row = [provider]
        #print(item_info_dict)
        for tag in tags:
            row.append(item_info_dict[tag])
        item_rows.append(row)

    return
