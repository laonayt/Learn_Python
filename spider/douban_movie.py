#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=0

import requests
import time
from requests.exceptions import ConnectionError

class Douban():
    def __init__(self,tag):
        self.tag = tag
        self.url = 'https://movie.douban.com/j/search_subjects'
        pass

    def get_index(self,page_start):
        params = {
            'type': 'movie',
            'tag': self.tag,
            'sort': 'recommend',
            'page_limit': '20',
            'page_start': page_start
        }
        try:
            response = requests.get(url=self.url,params=params)
            if response.status_code == 200:
                return response.json()
            return None
        except ConnectionError:
            print('get_index error')
            return None


    def parse_index(self,jsonData):
        if jsonData and 'subjects' in jsonData.keys():
            for item in jsonData.get('subjects'):
                yield {
                    'title' : item.get('title'),
                    'rate'  : item['rate'],
                    'url'   : item['url'],
                    'id'    : item['id'],
                    'cover' : item.get('cover')
                }

    def save_items(self,items):
        for item in items:
            with open('douban.csv','a',encoding='utf-8') as f:
                f.write("{},{},{},{},{}\n".format(item['id'],item['title'],item['rate'],item['cover'],item['url']))
                f.close()

    def run(self):
        for page_start in range(0,40,20):

            response = self.get_index(page_start=page_start)
            print(response)

            items = self.parse_index(response)

            self.save_items(items)

            time.sleep(2)

if __name__ == '__main__':
    spider = Douban('热门')
    spider.run()
