import os
import pymongo
from document_models import NormalizedExpense

def expense_record_store(expense: NormalizedExpense) -> str:
    uri = os.getenv("MONGODB_ATLAS_URI")
    client = pymongo.MongoClient(uri)
    db = client["expense_records"]
    collection = db["expenses"]
    result = collection.insert_one(expense.model_dump())
    return str(result.inserted_id)