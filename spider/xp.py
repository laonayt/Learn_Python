# -*- coding: utf-8 -*-
#!/usr/bin/env python


import requests
from bs4 import BeautifulSoup
import re , os, time
from multiprocessing import Pool, cpu_count

class CrawlXP():
    def __init__(self,fileType):
        self.homeURl = 'http://k6.csnmdcjnx.pw/pw/'
        self.fileType = fileType #1=小说 2=图片

        if fileType == 1:
            self.fileFloder = 'xp_txt/'
        elif fileType == 2:
            self.fileFloder = 'xp_img/'

    def get_parse_list(self,params):
        response = requests.get(params['url'])
        response.encoding = 'utf-8'

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            result = soup.find_all('a', attrs={'href': re.compile('html_data/(.*).html', re.S),
                                               'id': re.compile('a_ajax_(.*)', re.S)})
            for item in result:
                url = self.homeURl + item.get('href')
                title = item.get_text().split(']')[1]

                if self.fileType == 1:
                    self.floderDir = self.fileFloder + params['title']
                    self.make_floder(str(params['page']))
                    self.get_parse_detail_txt(url)

                elif self.fileType == 2:
                    self.floderDir = self.fileFloder + params['title'] + '/' + title
                    self.make_floder(str(params['page']))
                    self.get_parse_detail_img(url)

        else:
            print('get_parse_list error')


    def get_parse_detail_txt(self,url):
        response = requests.get(url)
        response.encoding = 'utf8'

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            title = soup.find('title').get_text().split('|')[0]
            print(title)

            textName = '{0}.{1}'.format(title, 'txt')
            text = soup.find('div', id='read_tpc').get_text()
            with open(textName, 'w', encoding='utf-8') as f:
                f.write(text)
                f.close()
        else:
            print('get_parse_detail_txt error')

    def get_parse_detail_img(self,url):
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text,'lxml')
            urls = [item.get('src') for item in soup.find('div',id='read_tpc').find_all('img')]

            for url in urls:
                self.get_save_img(url)
        else:
            print('get_parse_detail_img error')

    def get_save_img(self,url):
        try:
            response = requests.get(url)
            if response.status_code == 200:

                img_name = "{}.jpg".format(url.split('/')[-1])
                with open(img_name, 'wb') as f:
                    f.write(response.content)
                    f.close()

        except Exception as e:
            print('save_img error')


    def make_floder(self,name):
        path = os.path.join(self.floderDir,name)
        if not os.path.exists(path):
            os.makedirs(path)
            os.chdir(path)  # 切换为当前目录
            print('当前下载目录：' + path)


def get_xiaoshuo_type():
    xiaosuoUrl = 'http://k6.csnmdcjnx.pw/pw/thread.php?fid=17'
    response = requests.get(xiaosuoUrl)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text,'lxml')
    results = soup.find('span',id='t_typedb').find_all('a')

    types = []
    for a in results[1:]:
        dic = {
            'href' : a.get('href')[:-2],
            'title' : a.get_text()
        }
        types.append(dic)

    return types

def get_img_type():
    imgUrl = 'http://k6.csnmdcjnx.pw/pw/thread.php?fid=13'
    response = requests.get(imgUrl)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text,'lxml')
    results = soup.find('tbody',id='cate_children').find_all('a', class_ ='fnamecolor a1')

    types = []
    for item in results:
        dic = {
            'title' : item.find('b').get_text(),
            'href' : item.get('href')
        }
        types.append(dic)

    return types


def run_oneType(fileType):
    crawl = CrawlXP(fileType=fileType)

    types = []
    if fileType == 1:
        types = get_xiaoshuo_type()
    elif fileType ==2:
        types = get_img_type()

    for typeDic in types:
        print(str(types.index(typeDic) + 1) + ':' + typeDic['title'] + '\n')

    select = int(input('请输入类型：')) - 1
    page = int(input('请输入页数：'))

    href = types[select].get('href')[:-2]
    indexUrl = crawl.homeURl + href + '&page={}'
    title = types[select].get('title')

    params = []
    for page in range(1,page+1):
        dic = {
            'url' : indexUrl.format(page),
            'page' : page,
            'title' : title
        }
        params.append(dic)

    pool = Pool(10)
    pool.map(crawl.get_parse_list, params)
    pool.close()
    pool.join()


def run_AllType(fileType):
    crawl = CrawlXP(fileType=fileType)

    types = []
    if fileType == 1:
        types = get_xiaoshuo_type()
    elif fileType == 2:
        types = get_img_type()

    page = int(input('请输入页数：'))
    params = []
    for typeDic in types:
        title = typeDic.get('title')
        href = typeDic.get('href')

        for page in range(1,page+1):
            indexUrl = crawl.homeURl + href + '&page={}'.format(page)
            dic = {
                'url' : indexUrl,
                'page' : page,
                'title' : title
            }
            params.append(dic)

    pool = Pool(10)
    pool.map(crawl.get_parse_list, params)
    pool.close()
    pool.join()

if __name__ == '__main__':
    fileType = int(input('请输入文件类型(小说：1 图片：2)：'))

    oneOrMore = int(input('请选择爬取一种主题还是所有（一种：1 所有：2）：'))

    if oneOrMore == 1:
        run_oneType(fileType)
    elif oneOrMore == 2:
        run_AllType(fileType)