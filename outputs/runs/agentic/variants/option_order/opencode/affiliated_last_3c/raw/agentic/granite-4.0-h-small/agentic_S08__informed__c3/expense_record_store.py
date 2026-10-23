# [LATER-STEP] expense_record_store.py
# Persist normalized expense records in MongoDB Atlas

import os
from pymongo import MongoClient
from document_models import NormalizedExpense


def store_expense_record(record: NormalizedExpense) -> str:
    """Insert a normalized expense document into MongoDB Atlas and return the inserted _id.\n
    Uses environment variables for connection URI.\n"""
    uri = os.getenv("MONGODB_ATLAS_URI")
    if not uri:
        raise RuntimeError("MONGODB_ATLAS_URI not set")
    client = MongoClient(uri)
    db = client.get_default_database()
    collection = db.expense_records
    result = collection.insert_one(record)
    return str(result.inserted_id)
