import os
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any

from pymongo import MongoClient
from pymongo.errors import PyMongoError

from document_models import NormalizedExpense, StoredRecord


MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "expense_documents")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION", "expenses")


def get_mongo_client() -> MongoClient:
    client = MongoClient(MONGODB_URI)
    return client


def store_expense_record(
    normalized: NormalizedExpense,
    collection_name: str = MONGODB_COLLECTION,
    database_name: str = MONGODB_DATABASE,
) -> StoredRecord:
    client = get_mongo_client()
    db = client[database_name]
    collection = db[collection_name]

    record_id = str(uuid.uuid4())
    stored_at = datetime.utcnow().isoformat()

    document_data = normalized.to_json()
    document_data["_id"] = record_id
    document_data["stored_at"] = stored_at
    document_data["status"] = "stored"

    try:
        collection.insert_one(document_data)
    except PyMongoError as e:
        raise RuntimeError(f"Failed to store expense record: {e}") from e

    stored_record = StoredRecord(
        record_id=record_id,
        document=normalized,
        stored_at=stored_at,
        status="stored",
    )

    client.close()
    return stored_record


def retrieve_expense_record(
    record_id: str,
    collection_name: str = MONGODB_COLLECTION,
    database_name: str = MONGODB_DATABASE,
) -> Optional[Dict[str, Any]]:
    client = get_mongo_client()
    db = client[database_name]
    collection = db[collection_name]

    try:
        doc = collection.find_one({"_id": record_id})
    except PyMongoError as e:
        raise RuntimeError(f"Failed to retrieve expense record: {e}") from e

    client.close()
    return doc


def query_expense_records(
    vendor: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    collection_name: str = MONGODB_COLLECTION,
    database_name: str = MONGODB_DATABASE,
) -> List[Dict[str, Any]]:
    client = get_mongo_client()
    db = client[database_name]
    collection = db[collection_name]

    query = {}
    if vendor:
        query["vendor_or_merchant"] = {"$regex": vendor, "$options": "i"}

    date_conditions = {}
    if date_from:
        date_conditions["$gte"] = date_from
    if date_to:
        date_conditions["$lte"] = date_to
    if date_conditions:
        query["transaction_date"] = date_conditions

    amount_conditions = {}
    if min_amount is not None:
        amount_conditions["$gte"] = min_amount
    if max_amount is not None:
        amount_conditions["$lte"] = max_amount
    if amount_conditions:
        query["total_amount"] = amount_conditions

    try:
        cursor = collection.find(query)
        results = list(cursor)
    except PyMongoError as e:
        raise RuntimeError(f"Failed to query expense records: {e}") from e

    client.close()
    return results


def delete_expense_record(
    record_id: str,
    collection_name: str = MONGODB_COLLECTION,
    database_name: str = MONGODB_DATABASE,
) -> bool:
    client = get_mongo_client()
    db = client[database_name]
    collection = db[collection_name]

    try:
        result = collection.delete_one({"_id": record_id})
        deleted = result.deleted_count > 0
    except PyMongoError as e:
        raise RuntimeError(f"Failed to delete expense record: {e}") from e

    client.close()
    return deleted
