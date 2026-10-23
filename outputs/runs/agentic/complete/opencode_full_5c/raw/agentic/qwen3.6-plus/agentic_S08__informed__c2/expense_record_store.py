import os
from typing import List, Optional, Dict, Any
from datetime import datetime

from pymongo import MongoClient
from pymongo.errors import PyMongoError
from document_models import NormalizedExpenseRecord

MONGODB_ATLAS_URI = os.environ.get("MONGODB_ATLAS_URI", "mongodb://localhost:27017")
MONGODB_DB_NAME = os.environ.get("MONGODB_DB_NAME", "expense_db")
MONGODB_COLLECTION_NAME = os.environ.get("MONGODB_COLLECTION_NAME", "expense_records")


def get_mongo_client() -> MongoClient:
    if not MONGODB_ATLAS_URI:
        raise ValueError("MONGODB_ATLAS_URI environment variable is required")
    client = MongoClient(MONGODB_ATLAS_URI)
    return client


def get_expense_collection(collection_name: Optional[str] = None):
    client = get_mongo_client()
    db = client[MONGODB_DB_NAME]
    col_name = collection_name or MONGODB_COLLECTION_NAME
    return db[col_name]


def store_expense_record(
    record: NormalizedExpenseRecord,
    collection_name: Optional[str] = None,
) -> str:
    collection = get_expense_collection(collection_name)
    doc = record.to_dict()
    doc["stored_at"] = datetime.utcnow().isoformat()
    result = collection.insert_one(doc)
    return str(result.inserted_id)


def store_expense_records_batch(
    records: List[NormalizedExpenseRecord],
    collection_name: Optional[str] = None,
) -> List[str]:
    collection = get_expense_collection(collection_name)
    docs = []
    for record in records:
        doc = record.to_dict()
        doc["stored_at"] = datetime.utcnow().isoformat()
        docs.append(doc)
    result = collection.insert_many(docs)
    return [str(oid) for oid in result.inserted_ids]


def get_expense_record_by_id(
    record_id: str,
    collection_name: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    from bson.objectid import ObjectId

    collection = get_expense_collection(collection_name)
    try:
        doc = collection.find_one({"_id": ObjectId(record_id)})
    except Exception:
        doc = collection.find_one({"document_id": record_id})
    if doc:
        doc["_id"] = str(doc["_id"])
    return doc


def query_expense_records(
    vendor: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    min_total: Optional[float] = None,
    max_total: Optional[float] = None,
    collection_name: Optional[str] = None,
) -> List[Dict[str, Any]]:
    collection = get_expense_collection(collection_name)
    query = {}
    if vendor:
        query["vendor_or_merchant"] = {"$regex": vendor, "$options": "i"}
    if date_from or date_to:
        date_filter = {}
        if date_from:
            date_filter["$gte"] = date_from
        if date_to:
            date_filter["$lte"] = date_to
        query["date"] = date_filter
    if min_total is not None or max_total is not None:
        total_filter = {}
        if min_total is not None:
            total_filter["$gte"] = min_total
        if max_total is not None:
            total_filter["$lte"] = max_total
        query["total"] = total_filter

    cursor = collection.find(query)
    results = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        results.append(doc)
    return results


def delete_expense_record(
    record_id: str,
    collection_name: Optional[str] = None,
) -> bool:
    from bson.objectid import ObjectId

    collection = get_expense_collection(collection_name)
    try:
        result = collection.delete_one({"_id": ObjectId(record_id)})
    except Exception:
        result = collection.delete_one({"document_id": record_id})
    return result.deleted_count > 0
