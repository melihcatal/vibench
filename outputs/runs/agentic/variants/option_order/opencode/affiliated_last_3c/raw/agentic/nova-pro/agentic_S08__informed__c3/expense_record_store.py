from pymongo import MongoClient

import os


def expense_record_store(expense_record):
    client = MongoClient(os.getenv("MONGODB_ATLAS_URI"))
    db = client.expenses
    collection = db.records
    collection.insert_one(expense_record)
