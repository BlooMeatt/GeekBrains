# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        client.drop_database('Labirint')
        self.db = client.Labirint

    def process_item(self, item, spider):
        item['_id'] = int(item['_id'].split(' ')[2])
        try:
            item['price'] = int(item['price'])
        except:
            item['price_new'] = int(item['price_new'])
            item['price_old'] = int(item['price_old'])
        item['rating'] = float(item['rating'])

        collection = self.db['Labirint']
        collection.insert_one(item)

        print(item)
