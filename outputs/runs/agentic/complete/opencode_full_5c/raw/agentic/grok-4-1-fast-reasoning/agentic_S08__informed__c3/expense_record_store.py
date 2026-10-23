import os
import pymongo
from document_models import ExpenseRecord


def store_expense_record(expense_record: dict) -> str:
    """
    Persist normalized expense record to MongoDB Atlas.
    """
    uri = os.getenv("MONGODB_ATLAS_URI")
    if not uri:
        raise ValueError("MONGODB_ATLAS_URI required.")

    client = pymongo.MongoClient(uri)
    db = client["expense_db"]
    collection = db["records"]
    result = collection.insert_one(expense_record)
    client.close()
    return str(result.inserted_id)
