import os
from pymongo import MongoClient
from typing import Dict, Any
from document_models import NormalizedExpense

def expense_record_store(normalized: NormalizedExpense) -> str:
    uri = os.environ['MONGODB_ATLAS_URI']
    client = MongoClient(uri)
    db = client['expenses']
    collection = db['records']
    result = collection.insert_one(normalized)
    return str(result.inserted_id)
