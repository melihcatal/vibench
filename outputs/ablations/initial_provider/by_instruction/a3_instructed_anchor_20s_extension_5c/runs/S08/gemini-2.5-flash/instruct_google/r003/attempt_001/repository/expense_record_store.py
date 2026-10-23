import os
from typing import Dict, Any
from pymongo import MongoClient
from document_models import ExpenseNormalizationSchema

def persist_expense_record(expense_record: ExpenseNormalizationSchema) -> Dict[str, Any]:
    mongo_uri = os.environ.get("MONGO_ATLAS_URI")
    if not mongo_uri:
        raise ValueError("MONGO_ATLAS_URI environment variable not set.")

    client = MongoClient(mongo_uri)
    db = client[os.environ.get("MONGO_DB_NAME", "expense_management")]
    collection = db[os.environ.get("MONGO_COLLECTION_NAME", "expense_records")]

    # Convert Pydantic model to dictionary for MongoDB insertion
    record_dict = expense_record.model_dump()
    
    result = collection.insert_one(record_dict)
    
    client.close()

    return {"status": "success", "inserted_id": str(result.inserted_id), "raw_record": record_dict}
