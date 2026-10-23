import os
import pymongo


def store_expense_record(expense_record: dict) -> str:
    uri = os.getenv("MONGODB_ATLAS_URI")
    client = pymongo.MongoClient(uri)
    db = client["expenses_db"]
    collection = db["normalized_expenses"]
    result = collection.insert_one(expense_record)
    return str(result.inserted_id)
