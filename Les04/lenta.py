from pprint import pprint
from lxml import html
import requests

header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}

req = requests.get('https://lenta.ru',
                            headers=header)
root = html.fromstring(req.text)

hrefs = root.xpath('//div[contains(@class, "span8 js-main__content")]/section/div/div[contains(@class, "item")]/a/@href')

print(hrefs)
print(len(hrefs))

names = root.xpath('//div[contains(@class, "span8 js-main__content")]/section/div/div[contains(@class, "first-item")]/h2/a/text() |'
    '//div[contains(@class, "span8 js-main__content")]/section/div/div[contains(@class, "item")]/a/text()')

names = [el.replace('\xa0', ' ') for el in names ]

print(names)
print(len(names))

dates = root.xpath('//div[contains(@class, "span8 js-main__content")]/section/div/div[contains(@class, "first-item")]/h2/a/time/@datetime |'
    '//div[contains(@class, "span8 js-main__content")]/section/div/div[contains(@class, "item")]/a/time/@datetime')

print(dates)
print(len(dates))

news =[]

for i in range(0, len(hrefs)):
    news_data = {}
    news_data['site'] = 'lenta.ru'
    news_data['link'] = 'https://lenta.ru' + hrefs[i]
    news_data['name'] = names[i]
    news_data['date'] = dates[i]
    news.append(news_data)
    i += 1

for new in news:
    print(new)
