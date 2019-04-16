#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests,re, os
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
from multiprocessing import Pool, cpu_count

indexUrl = 'https://www.mzitu.com/xinggan/'

HEADERS = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Referer': 'http://www.mzitu.com'
}

def get_parse_index():
    response = requests.get(indexUrl)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text,'lxml')
        result = soup.find('ul',id='pins')
        hrefs = re.findall('(?<=href=)\S+', str(result))
        img_urls = [url.replace('"', "") for url in hrefs]

        new_urls = []
        for url in img_urls:
            if url not in new_urls:
                new_urls.append(url)
        return new_urls
    return None

def get_parse_detail(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        title = soup.title.get_text()
        print(title)
        max_count = soup.find('div', class_='pagenavi').find_all('span')[-2].get_text()
        page_urls = [url + '/' + str(i) for i in range(1, int(max_count) + 1)]
        return page_urls
    return None


def get_parse_page(url,idx):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text,'lxml')
        img = soup.find('div',class_='main-image').find('img')

        img_url = img.get('src')
        floderName = img.get('alt')

        save_page_image(img_url,floderName,idx)


def save_page_image(url,floderName,idx):
    print(url)
    response = requests.get(url,headers=HEADERS)
    if response.status_code == 200:

        floderPath = 'image/' + floderName

        if not os.path.exists(floderPath):
            os.makedirs(floderPath)

        filePath = floderPath + '/' + idx + '.jpg'

        print(filePath)

        with open(filePath, 'wb') as f:
            f.write(response.content)
            f.close()
    return None

if __name__ == '__main__':
    urls = get_parse_index()

    for url in urls:
        page_urls = get_parse_detail(url)
        for page_url in page_urls:
            get_parse_page(page_url,str(page_urls.index(page_url)))

