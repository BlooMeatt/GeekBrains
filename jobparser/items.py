# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobparserItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    price_old = scrapy.Field()
    price_new = scrapy.Field()
    author = scrapy.Field()
    url = scrapy.Field()
    _id = scrapy.Field()
    rating = scrapy.Field()
    pass
