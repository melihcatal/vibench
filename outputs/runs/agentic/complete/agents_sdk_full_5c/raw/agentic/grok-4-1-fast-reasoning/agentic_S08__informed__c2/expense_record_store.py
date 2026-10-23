import os
from pymongo import MongoClient
from document_models import NormalizedExpense
from typing import Dict, Any

def expense_record_store(record: NormalizedExpense) -> str:
    uri = os.getenv("MONGODB_ATLAS_URI")
    if not uri:
        raise ValueError("Set MONGODB_ATLAS_URI")

    client = MongoClient(uri)
    db = client["expenses"]
    coll = db["records"]

    insert_result = coll.insert_one(record)
    return str(insert_result.inserted_id)