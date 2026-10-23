from pymongo import MongoClient


def expense_record_store(expense_record):
    client = MongoClient(MONGODB_ATLAS_URI)
    db = client["expense_db"]
    collection = db["expenses"]
    collection.insert_one(expense_record)
