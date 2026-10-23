import os
import pymongo
from typing import Dict, Any
from document_models import NormalizedExpense

def expense_record_store(expense: NormalizedExpense) -> str:
    uri = os.getenv('MONGODB_ATLAS_URI')
    if not uri:
        raise ValueError('MONGODB_ATLAS_URI env var required')
    client = pymongo.MongoClient(uri)
    db = client['expense_db']
    collection = db['expenses']
    result = collection.insert_one(expense)
    client.close()
    return str(result.inserted_id)