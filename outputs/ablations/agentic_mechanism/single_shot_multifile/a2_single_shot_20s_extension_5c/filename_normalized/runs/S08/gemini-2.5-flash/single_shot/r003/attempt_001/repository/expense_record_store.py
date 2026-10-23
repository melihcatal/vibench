import os
from datetime import datetime
from document_client import get_mongodb_client
from document_models import ExpenseRecord, NormalizedExpense, LineItem, ValidationResult, SummaryRequest
from typing import Dict, Any, Optional
from bson.objectid import ObjectId

def persist_expense_record(record: ExpenseRecord) -> Dict[str, Any]:
    client = get_mongodb_client()
    db_name = os.environ.get("MONGODB_DATABASE_NAME", "expense_records_db")
    collection_name = os.environ.get("MONGODB_COLLECTION_NAME", "expenses")
    
    db = client[db_name]
    collection = db[collection_name]

    record_data = record.model_dump(by_alias=True, exclude_none=True)
    if not record_data.get("created_at"):
        record_data["created_at"] = datetime.utcnow().isoformat() + "Z"

    try:
        result = collection.insert_one(record_data)
        record_data["_id"] = str(result.inserted_id)
        return {"status": "success", "inserted_id": str(result.inserted_id), "record": record_data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_expense_record(record_id: str) -> Optional[ExpenseRecord]:
    client = get_mongodb_client()
    db_name = os.environ.get("MONGODB_DATABASE_NAME", "expense_records_db")
    collection_name = os.environ.get("MONGODB_COLLECTION_NAME", "expenses")
    
    db = client[db_name]
    collection = db[collection_name]

    try:
        record_data = collection.find_one({"_id": ObjectId(record_id)})
        if record_data:
            record_data["record_id"] = str(record_data["_id"])
            del record_data["_id"]
            return ExpenseRecord(**record_data)
        return None
    except Exception as e:
        print(f"Error retrieving record {record_id}: {e}")
        return None