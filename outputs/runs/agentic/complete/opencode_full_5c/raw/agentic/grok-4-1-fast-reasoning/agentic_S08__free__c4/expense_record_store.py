from document_client import get_mongo_client
from document_models import NormalizedExpense
import json


def store_expense_record(normalized: NormalizedExpense, record_id: str):
    client = get_mongo_client()
    db = client["expense_db"]
    collection = db["expense_records"]
    record_data = normalized.model_dump()
    record_data["record_id"] = record_id
    result = collection.insert_one(record_data)
    return result.inserted_id
