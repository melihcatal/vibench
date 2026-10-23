import os
from pymongo import MongoClient

client = MongoClient(os.getenv('MONGODB_ATLAS_URI'))
db = client['expense_records']
expenses_collection = db['expenses']

def store_expense_record(expense):
    expenses_collection.insert_one(expense)