from typing import Dict, Any
import os
from pymongo import MongoClient
from pymongo.collection import Collection
from document_models import NormalizedExpense


def persist_expense_record(expense: NormalizedExpense) -> str:
    """
    Persists normalized expense records in MongoDB Atlas.
    """
    client = MongoClient(os.getenv("MONGODB_ATLAS_URI"))
    db = client[os.getenv("MONGODB_DATABASE_NAME", "expenses")]
    collection: Collection = db[os.getenv("MONGODB_COLLECTION_NAME", "records")]

    result = collection.insert_one(expense.dict())
    return str(result.inserted_id)