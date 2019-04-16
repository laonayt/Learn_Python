#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from requests.exceptions import ConnectionError
import os
from hashlib import md5
from multiprocessing import Pool

def get_page_index(word,page):
    base = 'https://unsplash.com/napi/search/photos?query={word}&xp=&per_page=20&page={page}'
    url =  base.format(word=word,page=page)

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None
    except ConnectionError:
        print('get_page_index error')
        return None

def parse_page_index(jsonData):
    if jsonData and 'results' in jsonData.keys():
        for item in jsonData.get('results'):
            dic = {
                'description' : item.get('description'),
                'download' : item.get('links').get('download')
            }
            yield dic

def save_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            download_img(response.content)
        return None
    except ConnectionError:
        print('save_image error')
        return None

def download_img(content):
    path = 'unsplash_img'
    if not os.path.exists(path):
        os.makedirs(path)
    file_path = path + '/{0}.jpg'.format(md5(content).hexdigest())
    print(file_path)
    with open(file_path,'wb') as f:
        f.write(content)
        f.close()

def main(word,page):
    for x in range(1,page):
        jsonData = get_page_index(word, x)

        items = parse_page_index(jsonData)

        for item in items:
            print(item['download'])
            save_image(item['download'])

if __name__ == '__main__':
    word = str(input('请输入关键词：'))
    page = int(input('请输入页数：'))

    pool = Pool()
    groups = ([x * 20 for x in range(0, 8)])
    pool.map(main(word,page),groups)
    pool.close()
    pool.join()