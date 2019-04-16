# -*- coding: utf-8 -*-
#!/usr/bin/env python


import requests
from bs4 import BeautifulSoup
import re , os
from multiprocessing import Pool

baseURl = 'http://k6.csnmdcjnx.pw/pw/'
floderNme = 'xp_txt'

def get_index():
    url = 'http://k6.csnmdcjnx.pw/pw/thread.php?fid=17'
    response = requests.get(url)
    response.encoding = 'utf-8'
    if response.status_code == 200:
        return response.text
    return None

def parse_index(html):
    soup = BeautifulSoup(html,'lxml')
    result = soup.find_all('a',attrs={'href' : re.compile('html_data/(.*).html',re.S),'id' : re.compile('a_ajax_(.*)',re.S)})
    for item in result:
        url = baseURl +item.get('href')
        print(url)
        yield url

def get_detail(url):
    response = requests.get(url)
    response.encoding = 'utf8'
    if response.status_code == 200:
        parse_detail(response.text)
    return None


def parse_detail(html):
    soup = BeautifulSoup(html,'lxml')
    title = soup.find('title').get_text().split('|')[0]
    print(title)

    filePath = floderNme + '/{0}.{1}'.format(title,'txt')

    text = soup.find('div',id='read_tpc').get_text()

    with open(filePath,'w',encoding='utf-8') as f:
        f.write(text)
        f.close()

def run():
    if not os.path.exists(floderNme):
        os.makedirs(floderNme)

    html = get_index()
    urls = parse_index(html)
    for url in urls:
        get_detail(url)


if __name__ == '__main__':
    run()