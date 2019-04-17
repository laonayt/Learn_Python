#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests,re, os, time
from bs4 import BeautifulSoup
from multiprocessing import Pool

save_dir = 'meizi_img'

HEADERS = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Referer': 'http://www.mzitu.com'
}

#解析首页
def get_parse_index(page):
    base_url = 'https://www.mzitu.com/xinggan/page/'
    page_urls = ['{base}{num}'.format(base=base_url, num=num) for num in range(1,page+1)]
    img_urls = []

    for page_url in page_urls:
        try:
            response = requests.get(page_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text,'lxml')
                result = soup.find('ul',id='pins')
                hrefs = re.findall('(?<=href=)\S+', str(result))
                img_url = [url.replace('"', "") for url in hrefs]
                img_urls.extend(img_url)

        except Exception as e:
            print('get_parse_index error:' + e)

    return set(img_urls)#利用set去重

#解析图片预览页
def get_parse_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')

            title = soup.title.get_text().split('-')[0]
            if make_dir(title):
                max_count = soup.find('div', class_='pagenavi').find_all('span')[-2].get_text()
                img_pages = [url + '/' + str(i) for i in range(1, int(max_count) + 1)]

                print('downloading: {0} count: {1} '.format(title, max_count))

                for idx, url in enumerate(img_pages):
                    parse_img_page(url, idx)


    except Exception as e:
        print('get_parse_detail:' + e)


#解析图片分页
def parse_img_page(url,idx):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            img_url = soup.find('div', class_='main-image').find('img').get('src')
            get_save_image(img_url, idx)

    except Exception as e:
        print('parse_img_page' + e)


#从图片分页中下载保存图片
def get_save_image(url,idx):
    try:
        response = requests.get(url,headers=HEADERS,timeout=10)
        if response.status_code == 200:
            img_name = "pic_{}.jpg".format(idx+1)
            path = os.getcwd()
            with open(img_name, 'wb') as f:
                f.write(response.content)
                f.close()
    except Exception as e:
        print('get_save_image' + e)


#根据 title 创建文件夹
def make_dir(folder_name):
    path = os.path.join(save_dir,folder_name)
    if not os.path.exists(path):
        os.makedirs(path)
        os.chdir(path)#切换当前工作路径
        return True
    return False

def run():
    urls = get_parse_index(page)
    for url in urls:
        get_parse_detail(url)


if __name__ == '__main__':
    page = int(input('请输入爬取页数：'))

    save_dir = os.path.join(os.getcwd(),save_dir)

    pool = Pool()
    groups = ([x * 20 for x in range(0, 8)])
    pool.map(run(), groups)
    pool.close()
    pool.join()
    time.sleep(3)

