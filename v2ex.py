import xml.etree.ElementTree as ET

import requests
from matplotlib import pyplot as plt
from wordcloud import WordCloud

# v2ex 提供了rss
feeds = (
    "https://www.v2ex.com/feed/tab/tech.xml",
    "https://www.v2ex.com/feed/tab/creative.xml",
    "https://www.v2ex.com/feed/tab/play.xml",
    "https://www.v2ex.com/feed/tab/apple.xml",
    "https://www.v2ex.com/feed/tab/jobs.xml",
    "https://www.v2ex.com/feed/tab/deals.xml",
    "https://www.v2ex.com/feed/tab/city.xml",
    "https://www.v2ex.com/feed/tab/qna.xml",
    "https://www.v2ex.com/feed/tab/hot.xml",
    "https://www.v2ex.com/feed/tab/all.xml",
    "https://www.v2ex.com/feed/tab/r2.xml",
)

contents = []
for feed in feeds:
    try:
        print(feed)
        response = requests.get(feed, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "})
        xml_data = response.content
        root = ET.fromstring(xml_data)

        for title in root.findall('.//{http://www.w3.org/2005/Atom}title'):
            contents.append(title.text)
    except:
        continue
        pass


space_list = ' '.join(contents)
wc = WordCloud(width=1400, height=2200,
               background_color='white',
               mode='RGB',
               max_words=500,
               font_path="STHeiti Light.ttc",
               max_font_size=150,
               relative_scaling=0.6,  # 设置字体大小与词频的关联程度为0.4
               random_state=50,
               scale=2
               ).generate(space_list)

plt.imshow(wc)
plt.axis('off')
plt.show()
wc.to_file('v2ex.jpg')
