import base64
import json
import re
import operator

import jieba
import requests
from lxml import etree
from matplotlib import pyplot as plt
from wordcloud import WordCloud



contents = []
url = "https://segmentfault.com/questions?page=%s"

for i in range(1, 5):
    print(i)
    response = requests.get(url % i, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "}, )
    html = response.content.decode()
    # html = open('test.html', 'r', encoding='utf-8').read()
    # print(html)
    tree = etree.HTML(html)
    titles = tree.xpath('//*[@id="__next"]/div[5]/div/div[1]/div[2]/ul/li[2]/div/div[2]/div[1]/h3/a')
    print(titles)
    for title in titles:
        try:
            title = title.text.strip()
        except Exception as e:
            print(e)
            continue
            pass
        if len(title) > 0: contents.append(title)