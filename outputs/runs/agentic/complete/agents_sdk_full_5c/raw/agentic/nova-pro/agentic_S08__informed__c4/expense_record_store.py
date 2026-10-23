import os
from pymongo import MongoClient

def store_expense_record(expense):
    client = MongoClient(os.getenv('MONGODB_ATLAS_URI'))
    db = client['expenses']
    collection = db['records']
    collection.insert_one(expense)