import os
from datetime import datetime, timezone
from typing import Optional

from pymongo import MongoClient
from pymongo.collection import Collection

from document_models import NormalizedExpense

MONGODB_ATLAS_URI = os.environ.get("MONGODB_ATLAS_URI", "mongodb://localhost:27017")
MONGODB_DATABASE = os.environ.get("MONGODB_DATABASE", "expense_db")
MONGODB_COLLECTION = os.environ.get("MONGODB_COLLECTION", "expenses")


def get_mongo_client() -> MongoClient:
    return MongoClient(MONGODB_ATLAS_URI)


def get_expense_collection(collection_name: str = None) -> Collection:
    client = get_mongo_client()
    db = client[MONGODB_DATABASE]
    return db[collection_name or MONGODB_COLLECTION]


def store_expense_record(
    expense: NormalizedExpense, collection: Collection = None
) -> str:
    if collection is None:
        collection = get_expense_collection()
    doc = expense.to_dict()
    doc["created_at"] = datetime.now(timezone.utc).isoformat()
    doc["updated_at"] = datetime.now(timezone.utc).isoformat()
    if expense.source_document_id:
        doc["_id"] = expense.source_document_id
    result = collection.insert_one(doc)
    return str(result.inserted_id)


def store_expense_records(
    expenses: list[NormalizedExpense], collection: Collection = None
) -> list[str]:
    if collection is None:
        collection = get_expense_collection()
    ids = []
    for expense in expenses:
        record_id = store_expense_record(expense, collection=collection)
        ids.append(record_id)
    return ids


def get_expense_record(
    document_id: str, collection: Collection = None
) -> Optional[dict]:
    if collection is None:
        collection = get_expense_collection()
    doc = collection.find_one({"_id": document_id})
    if doc:
        doc["_id"] = str(doc["_id"])
    return doc


def query_expenses_by_vendor(vendor: str, collection: Collection = None) -> list[dict]:
    if collection is None:
        collection = get_expense_collection()
    docs = list(collection.find({"vendor_or_merchant": vendor}))
    for doc in docs:
        doc["_id"] = str(doc["_id"])
    return docs


def query_expenses_by_date_range(
    start_date: str, end_date: str, collection: Collection = None
) -> list[dict]:
    if collection is None:
        collection = get_expense_collection()
    docs = list(
        collection.find(
            {
                "document_date": {"$gte": start_date, "$lte": end_date},
            }
        )
    )
    for doc in docs:
        doc["_id"] = str(doc["_id"])
    return docs


def update_expense_record(
    document_id: str, updates: dict, collection: Collection = None
) -> bool:
    if collection is None:
        collection = get_expense_collection()
    updates["updated_at"] = datetime.now(timezone.utc).isoformat()
    result = collection.update_one({"_id": document_id}, {"$set": updates})
    return result.modified_count > 0


def delete_expense_record(document_id: str, collection: Collection = None) -> bool:
    if collection is None:
        collection = get_expense_collection()
    result = collection.delete_one({"_id": document_id})
    return result.deleted_count > 0
