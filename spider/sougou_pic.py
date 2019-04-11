#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import os
from hashlib import md5
import re
import time
from requests.exceptions import ConnectionError
from multiprocessing import Pool
import pymongo

client = pymongo.MongoClient('localhost',connect=False)
db = client['sougoupic_db']


def get_page_index(word,page):
    base = 'https://pic.sogou.com/pics?query={keyword}&mode=1&start={start}&reqType=ajax&reqFrom=result&tn=0'
    url = base.format(keyword=word,start=48*page)

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None
    except ConnectionError:
        print('get_page_index error')
        return None

def parse_page_index(jsonData):
    if jsonData and 'items' in jsonData.keys():
        for item in jsonData.get('items'):
            image_title = item.get('title')
            image_url = item.get('pic_url')
            dic = {
                'title' : image_title,
                'url' : image_url
            }
            save_mongo(dic)

            yield dic

def save_mongo(result):
    if db['pic_table'].insert(result):
        print('insert mongo success')
    return None

def download_image(item):
    print(item.get('url'))
    try:
        response = requests.get(item.get('url'))

        if response.status_code == 200:
            save_image(response.content, item.get('title'))
        return None

    except ConnectionError:
        print('download_image error')
        return None

def save_image(content,title):
    img_path = 'sougou_imgs' + os.path.sep + title

    if not os.path.exists(img_path):
        os.makedirs(img_path)

    file_path = img_path + '/{0}.{1}'.format(md5(content).hexdigest(), 'jpg')

    print(file_path)

    if not os.path.exists(file_path):
        with open(file_path,'wb') as f:
            f.write(content)
            f.close()

def main():
    word = str(input('请输入关键字:'))
    page = int(input('请输入页数:'))

    jsonData = get_page_index(word,page)

    items = parse_page_index(jsonData)

    for item in items:
        download_image(item)

GROUP_START = 0
GROUP_END = 8

if __name__ == '__main__':
    pool = Pool()

    groups = ([x*20 for x in range(GROUP_START,GROUP_END)])

    pool.map(main(),groups)

    pool.close()

    pool.join()

    time.sleep(3)