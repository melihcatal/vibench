import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from document_client import get_mongodb_client
from document_models import NormalizedExpense
from typing import Dict, Any

def persist_expense_record_mongodb(record: NormalizedExpense,
                                   db_name: str = "expense_records",
                                   collection_name: str = "normalized_expenses") -> Dict[str, Any]:
    """
    Persists a normalized expense record into a MongoDB Atlas collection.
    Requires MONGODB_URI environment variable.
    Returns the inserted document's ID and status.
    """
    client = get_mongodb_client()
    db = client[db_name]
    collection = db[collection_name]

    record_dict = record.model_dump(mode='json', exclude_unset=True)

    try:
        result = collection.insert_one(record_dict)
        return {
            "status": "success",
            "inserted_id": str(result.inserted_id),
            "db_name": db_name,
            "collection_name": collection_name
        }
    except PyMongoError as e:
        print(f"MongoDB insertion error: {e}")
        return {
            "status": "error",
            "message": str(e),
            "db_name": db_name,
            "collection_name": collection_name
        }
    finally:
        client.close()
