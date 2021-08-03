import json
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client['test_db']
collection_currency = db['mainapp_sample']


with open('samples.json') as file:
    file_data = json.load(file)
    collection_currency.insert_one(file_data)

client.close()
