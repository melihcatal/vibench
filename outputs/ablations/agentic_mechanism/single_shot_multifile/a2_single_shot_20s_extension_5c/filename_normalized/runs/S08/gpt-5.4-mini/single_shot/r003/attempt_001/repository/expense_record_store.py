import os
from typing import Any

import pymongo

from document_models import normalize_expense_record


def persist_normalized_expense(record: dict[str, Any]) -> dict[str, Any]:
    mongo_uri = os.getenv("MONGODB_URI")
    mongo_db = os.getenv("MONGODB_DATABASE", "expenses")
    mongo_collection = os.getenv("MONGODB_COLLECTION", "records")
    if not mongo_uri:
        raise ValueError("MONGODB_URI is required for MongoDB Atlas storage")
    client = pymongo.MongoClient(mongo_uri)
    collection = client[mongo_db][mongo_collection]
    normalized = normalize_expense_record(record)
    result = collection.insert_one(normalized)
    normalized["_id"] = str(result.inserted_id)
    return normalized
