import os
from typing import Dict, Any, List, Optional
from datetime import datetime
from pymongo import MongoClient
from pymongo.collection import Collection

MONGODB_CONNECTION_STRING = os.environ.get(
    "MONGODB_CONNECTION_STRING",
    "mongodb+srv://<username>:<password>@cluster0.mongodb.net/",
)
MONGODB_DATABASE = os.environ.get("MONGODB_DATABASE", "expense_documents")
MONGODB_COLLECTION = os.environ.get("MONGODB_COLLECTION", "expense_records")


def get_mongo_client() -> MongoClient:
    client = MongoClient(MONGODB_CONNECTION_STRING)
    return client


def get_expense_collection(
    database_name: str = MONGODB_DATABASE, collection_name: str = MONGODB_COLLECTION
) -> Collection:
    client = get_mongo_client()
    db = client[database_name]
    collection = db[collection_name]
    return collection


def store_expense_record(
    expense_record: Dict[str, Any], collection: Optional[Collection] = None
) -> Dict[str, Any]:
    if collection is None:
        collection = get_expense_collection()

    record_to_store = expense_record.copy()
    record_to_store["stored_at"] = datetime.utcnow().isoformat()
    record_to_store["provider"] = "mongodb_atlas"

    result = collection.insert_one(record_to_store)

    return {
        "record_id": str(result.inserted_id),
        "stored": True,
        "stored_at": record_to_store["stored_at"],
        "document_id": expense_record.get("document_id", ""),
        "provider": "mongodb_atlas",
    }


def store_multiple_expense_records(
    expense_records: List[Dict[str, Any]], collection: Optional[Collection] = None
) -> List[Dict[str, Any]]:
    if collection is None:
        collection = get_expense_collection()

    results = []
    for record in expense_records:
        result = store_expense_record(record, collection)
        results.append(result)

    return results


def query_expense_records(
    filters: Optional[Dict[str, Any]] = None,
    limit: int = 100,
    collection: Optional[Collection] = None,
) -> List[Dict[str, Any]]:
    if collection is None:
        collection = get_expense_collection()

    query_filter = filters if filters else {}
    cursor = collection.find(query_filter).limit(limit)

    records = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        records.append(doc)

    return records


def get_expense_record_by_id(
    record_id: str, collection: Optional[Collection] = None
) -> Optional[Dict[str, Any]]:
    if collection is None:
        collection = get_expense_collection()

    from bson.objectid import ObjectId

    try:
        doc = collection.find_one({"_id": ObjectId(record_id)})
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc
    except Exception:
        return None


def delete_expense_record(
    record_id: str, collection: Optional[Collection] = None
) -> bool:
    if collection is None:
        collection = get_expense_collection()

    from bson.objectid import ObjectId

    try:
        result = collection.delete_one({"_id": ObjectId(record_id)})
        return result.deleted_count > 0
    except Exception:
        return False
