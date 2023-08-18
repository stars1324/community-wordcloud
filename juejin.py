import base64
import json
import re
import operator

import jieba
import requests
from matplotlib import pyplot as plt
from wordcloud import WordCloud

contents = []

url = "https://api.juejin.cn/recommend_api/v1/article/recommend_all_feed?aid=2608&uuid=6896764480194545166&spider=0"

for i in range(0, 10):
    print(i)
    cursor = base64.b64encode(json.dumps({"v": "7268293542971277349", "i": (i - 1) * 20}).encode("utf-8"))
    data = {
        "client_type": 2608,
        "cursor": cursor.decode(),
        "id_type": 2,
        "limit": 20,
        "sort_type": 200,
    }

    response = requests.post(url,
                             headers={
                                 "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "},
                             data=json.dumps(data))
    results = response.json()
    for result in results["data"]:
        if result["item_type"] != 2:
            continue
        contents.append(result["item_info"]["article_info"]['title'])
        contents.append(result["item_info"]["article_info"]['brief_content'])

space_list = ' '.join(contents)
# 把数据存起来
text_path = "./content.txt"
open(text_path, "w").write(space_list)
text_path = "./content.txt"
sentence = open(text_path, 'r', encoding='utf-8').read()

# 结巴拆词代码抄的：https://zhuanlan.zhihu.com/p/393516515
# 去掉标点符号
r = "[_.!+-=——,$%^，。？、~@#￥%……&*《》<>「」{}【】()/] "
text = re.sub(r, ' ', sentence)
wordlist_after_jieba = jieba.lcut(text)
words_dropped_sapce = [i.strip() for i in wordlist_after_jieba]

stopwords = [line.strip() for line in open('stop_words_base.txt').readlines()]
words_dropped_stopwords = [i for i in words_dropped_sapce if i not in stopwords]

words_count = {}  # 字典类型
for word in words_dropped_stopwords:
    words_count[word] = words_count.get(word, 0) + 1
sorted_words_count = sorted(words_count.items(), key=operator.itemgetter(1), reverse=True)  # 降序排序
sorted_words_count = dict([(w[0], w[1]) for w in sorted_words_count])

wc = WordCloud(width=600, height=400,
               background_color='white',
               mode='RGB',
               max_words=500,
               font_path="STHeiti Light.ttc",
               max_font_size=150,
               relative_scaling=0.6,
               random_state=50,
               scale=2
               ).generate_from_frequencies(sorted_words_count)

plt.imshow(wc)
plt.axis('off')
plt.show()
wc.to_file('juejin.jpg')
