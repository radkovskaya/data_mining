from pprint import pprint
from lxml import html
import requests
import datetime
now = datetime.datetime.now()

header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}

req = requests.get('https://mail.ru',
                            headers=header)
root = html.fromstring(req.text)

hrefs = root.xpath('//div[contains(@class,"news-item o-media news-item_media news-item_main")]/a/@href | '
                   '//div[contains(@class, "news-item__inner")]/a[last()]/@href')

names = root.xpath('//div[contains(@class,"news-item o-media news-item_media news-item_main")]//h3/text() | '
                   '//div[contains(@class, "news-item__inner")]/a[last()]/text()')
names = [el.replace('\xa0', ' ') for el in names ]

month = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля',
         'августа', 'сентября', 'октября', 'ноября', 'декабря' ]

news =[]

for i in range(0, len(names)):
    news_data = {}
    news_data['site'] = 'mail.ru'
    news_data['link'] = hrefs[i]
    news_data['name'] = names[i]
    news_data['date'] = now.strftime("%H:%M, %d ") + month[int(now.strftime('%m'))-1] + now.strftime(" %Y")
    print(news_data)
    news.append(news_data)
    i += 1

for new in news:
    print(new)
