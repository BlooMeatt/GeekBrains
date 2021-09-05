from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['Products']

all_coll = db.list_collection_names()

rating = int(input('Введите минимальное значение для общего рейтинга или качества: '))

for i in all_coll:
    print(i)
    collection = db[i]
    docs = collection.find(
        {'$or': [
            {'Общий рейтинг': {'$gt': rating}},
            {'Качество': {'$gt': rating}}

        ]
        }
    )
    for n in docs:
        print(n)
