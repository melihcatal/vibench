from pymongo import MongoClient
from document_client import get_mongodb_atlas_credentials
from typing import Dict, Any

def persist_expense_record(expense_record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Persists normalized expense records in a MongoDB Atlas managed document store.
    """
    creds = get_mongodb_atlas_credentials()
    client = None
    try:
        client = MongoClient(creds["connection_string"])
        db = client[creds["database_name"]]
        collection = db[creds["collection_name"]]
        
        result = collection.insert_one(expense_record)
        return {"status": "success", "inserted_id": str(result.inserted_id)}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        if client:
            client.close()
