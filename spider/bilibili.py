#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, urllib

class BiLiBiLi():
    def __init__(self,keyword):
        self.keyword = keyword

        self.searchHeader = {
            'Referer' : 'https://search.bilibili.com/all?keyword=%s' %urllib.parse.quote(keyword),
            'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
        }
        print(self.searchHeader)

    def get_parse_index(self):
        baseUrl = 'https://api.bilibili.com/x/web-interface/search/all'
        'https://api.bilibili.com/x/web-interface/search/type?jsonp=jsonp&search_type=video&highlight=1&keyword=%E9%92%93%E9%B1%BC&page=2&callback=__jp3'
        params = {
            'jsonp': 'jsonp',
            'highlight': '1',
            'keyword': urllib.parse.quote(self.keyword),
            'callback': '__jp2'
        }
        response = requests.get(url=baseUrl, params=params, headers=self.searchHeader)
        # response = requests.get(url=baseUrl)

        # response.encoding = 'utf-8'
        print(response.url)
        if response.status_code == 200:
            print(response.text)
        print(response.raise_for_status())

def run():
    bili = BiLiBiLi('钓鱼')
    bili.get_parse_index()

if __name__ == '__main__':
    run()