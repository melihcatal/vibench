import os
from pymongo import MongoClient


def store_expense_record(expense_record):
    client = MongoClient(os.getenv("MONGODB_ATLAS_URI"))
    db = client.expense_db
    collection = db.expenses
    collection.insert_one(expense_record)
