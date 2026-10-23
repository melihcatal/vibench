import os
from pymongo import MongoClient
from dataclasses import asdict
from document_models import NormalizedExpense
from document_client import validate_env

validate_env("mongodb")


def expense_record_store(expense: NormalizedExpense) -> str:
    uri = os.getenv("MONGODB_ATLAS_URI")
    client = MongoClient(uri)
    db = client["expense_db"]
    collection = db["expenses"]
    result = collection.insert_one(asdict(expense))
    return str(result.inserted_id)
