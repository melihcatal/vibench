import os
import pymongo
from document_models import NormalizedExpense


def expense_record_store(normalized: NormalizedExpense) -> str:
    mongodb_uri = os.getenv("MONGODB_ATLAS_URI")
    if not mongodb_uri:
        raise ValueError("MONGODB_ATLAS_URI not set")
    client = pymongo.MongoClient(mongodb_uri)
    db = client["expense_db"]
    collection = db["normalized_expenses"]
    doc_data = normalized.model_dump(exclude_unset=True)
    result = collection.insert_one(doc_data)
    return str(result.inserted_id)
