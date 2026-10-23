import os
from typing import Dict, Any
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from document_models import NormalizedExpense

def persist_expense_record(expense_record: NormalizedExpense, config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    
    # MongoDB Atlas connection string from environment or config
    mongodb_uri = config.get('MONGODB_URI') or os.environ.get('MONGODB_URI')
    if not mongodb_uri:
        raise ValueError("MONGODB_URI must be provided to connect to MongoDB Atlas.")

    database_name = config.get('MONGODB_DATABASE') or os.environ.get('MONGODB_DATABASE') or "expense_db"
    collection_name = config.get('MONGODB_COLLECTION') or os.environ.get('MONGODB_COLLECTION') or "expense_records"

    try:
        client = MongoClient(mongodb_uri)
        # The ping command is cheap and does not require auth.
        client.admin.command('ping')
        db = client[database_name]
        collection = db[collection_name]
        
        # Convert Pydantic model to dictionary for MongoDB insertion
        record_dict = expense_record.dict(by_alias=True)
        
        result = collection.insert_one(record_dict)
        return {"status": "success", "inserted_id": str(result.inserted_id)}
    except ConnectionFailure as e:
        print(f"MongoDB connection failed: {e}")
        return {"status": "error", "message": f"MongoDB connection error: {e}"}
    except Exception as e:
        print(f"An error occurred while persisting expense record: {e}")
        return {"status": "error", "message": f"Failed to persist record: {e}"}
    finally:
        if 'client' in locals() and client:
            client.close()
