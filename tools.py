# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 00:34:19 2017

@author: Avi
"""
import json

def save_conf(file_name, data):
    """save data by json format"""
    with open(file_name, 'wt', encoding="utf-8") as outfile:
        json.dump(data, outfile, sort_keys = False, indent = 4)

def load_conf(file_name):
    """load data from json"""
    with open(file_name, encoding="utf-8") as data_file:
        data = json.load(data_file)
    return data
