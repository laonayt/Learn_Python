#!/usr/bin/env python
# -*- coding: utf-8 -*-

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""
from bs4 import BeautifulSoup
import re

# soup = BeautifulSoup(html_doc,'lxml')
# print(soup.prettify())
# print(soup.title)
# print(soup.title.get_text())
# print(soup.title.string)
# print(soup.p)
# print(soup.p['class'])
# print(soup.find_all('a'))
# print(soup.find(id='link3'))

# for link in soup.find_all('a'):
#     print(link['href'])
#     print(link.get('href'))

f = open('meizitu.html',encoding='utf-8')
html = f.read()
soup = BeautifulSoup(html,'lxml')
result = soup.find('ul',id='pins')

# str = ' <a href="https://www.mzitu.com/176144" target="_blank">'
result2 = re.findall('(?<=href=)\S+',str(result))

img_urls = []
img_url = [url.replace('"', "") for url in result2]
img_urls.extend(img_url)
print(set(img_urls))





