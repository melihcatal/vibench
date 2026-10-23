from typing import Any, Dict
from pymongo import MongoClient
from document_client import require_env


def expense_record_store(record: Dict[str, Any]) -> str:
    client = MongoClient(require_env('MONGODB_ATLAS_URI'))
    collection = client.get_default_database().expense_records
    result = collection.insert_one(record)
    return str(result.inserted_id)
