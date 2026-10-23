from pymongo import MongoClient


def persist_expense_record(expense_record):
    client = MongoClient(os.getenv("MONGODB_ATLAS_URI"))
    db = client["expenses"]
    collection = db["records"]
    collection.insert_one(expense_record)
