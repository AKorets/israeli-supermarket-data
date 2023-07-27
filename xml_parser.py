# -*- coding: utf-8 -*-
"""
Used to parse all store file formats
@author: Avi
"""
from lxml import objectify
import codecs

def get_root(xml_file, encoding):
    """get store xml root, in lxml format"""
    with codecs.open(xml_file, encoding=encoding, errors="ignore") as store_file:
        xml = store_file.read()
        #print(xml[:90])
        xml = xml.replace('<?xml version="1.0" encoding="ISO-8859-8" standalone="no" ?>\r\n','')
        xml = xml.encode("UTF-16")

    return objectify.fromstring(xml)