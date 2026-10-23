from pymongo import MongoClient

# MongoDB Atlas connection URI
client = MongoClient('mongodb+srv://<username>:<password>@cluster0.mongodb.net/test?retryWrites=true&w=majority')

db = client['expense_records']
collection = db['expenses']

def store_expense_record(record):
    collection.insert_one(record)