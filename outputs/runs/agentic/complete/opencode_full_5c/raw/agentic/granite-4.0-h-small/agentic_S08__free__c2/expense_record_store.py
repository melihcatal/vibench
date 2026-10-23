# [LATER-STEP] expense_record_store.py
# Persist normalized expense records in a managed document store (e.g., Amazon DocumentDB / MongoDB)

import pymongo
from document_models import NormalizedExpense

# Connection details - replace with real URI and credentials (could be env vars)
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "expense_tracker"
COLLECTION_NAME = "records"

client = pymongo.MongoClient(MONGO_URI)

collection = client[DB_NAME][COLLECTION_NAME]


def persist_expense(expense: NormalizedExpense) -> str:
    """Insert a normalized expense document into the collection and return its _id."""
    result = collection.insert_one(expense)
    return str(result.inserted_id)
