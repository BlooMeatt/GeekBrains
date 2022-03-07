from lxml import html
import requests
from pymongo import MongoClient

url = 'https://yandex.ru/news/region/moscow'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}

response = requests.get(url, headers=headers)

client = MongoClient('127.0.0.1', 27017)
client.drop_database('Yandex_News')
db = client['Yandex_News']
collection = db.news

dom = html.fromstring(response.text)

items = dom.xpath("//div[contains(@class,'mg-card mg-card_flexible-half mg-card_type_image mg-grid__item') or "
                  "contains(@class,'mg-card mg-card_flexible-single mg-card_media-fixed-height mg-card_type_image mg-grid__item') or "
                  "contains(@class,'mg-card mg-card_flexible-single mg-card_type_image mg-grid__item') or "
                  "contains(@class,'mg-card mg-card_type_image mg-card_stretching mg-card_flexible-double mg-grid__item')]")

news = []
for i in items:
    news_data = {}
    title = i.xpath(".//h2[@class='mg-card__title']//text()")[0]
    link = i.xpath(".//a/@href")[0]
    source = i.xpath(".//div[@class='mg-card-footer mg-card__footer mg-card__footer_type_image']//a/text() ")[0]
    data = i.xpath(".//span[@class='mg-card-source__time']/text()")[0]
    news_data['title'] = str(title)
    news_data['link'] = str(link)
    news_data['source'] = source
    news_data['data'] = data
    news.append(news_data)
    print(title)
collection.insert_many(news)
