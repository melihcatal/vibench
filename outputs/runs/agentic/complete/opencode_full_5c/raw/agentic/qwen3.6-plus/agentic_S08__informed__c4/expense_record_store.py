import os
from datetime import datetime
from pymongo import MongoClient
from document_models import NormalizedExpense


MONGODB_ATLAS_URI = os.environ.get("MONGODB_ATLAS_URI", "mongodb://localhost:27017")
MONGODB_DB_NAME = os.environ.get("MONGODB_DB_NAME", "expense_documents")
MONGODB_COLLECTION_NAME = os.environ.get("MONGODB_COLLECTION_NAME", "expenses")


def get_mongo_client():
    client = MongoClient(MONGODB_ATLAS_URI)
    return client


def get_expense_collection():
    client = get_mongo_client()
    db = client[MONGODB_DB_NAME]
    collection = db[MONGODB_COLLECTION_NAME]
    return collection


def store_expense_record(normalized_expense: NormalizedExpense) -> dict:
    collection = get_expense_collection()

    expense_data = normalized_expense.to_dict()
    expense_data["_id"] = (
        f"{normalized_expense.document_type}_{normalized_expense.date}_{datetime.utcnow().timestamp()}"
    )
    expense_data["stored_at"] = datetime.utcnow().isoformat()
    expense_data["source_document"] = normalized_expense.source_document

    result = collection.insert_one(expense_data)
    return {
        "inserted_id": str(result.inserted_id),
        "acknowledged": result.acknowledged,
        "document": expense_data,
    }


def store_expense_from_dict(expense_dict: dict) -> dict:
    normalized = NormalizedExpense(
        document_type=expense_dict.get("document_type", ""),
        vendor_or_merchant=expense_dict.get("vendor_or_merchant", ""),
        date=expense_dict.get("date", ""),
        subtotal=expense_dict.get("subtotal", 0.0),
        tax=expense_dict.get("tax", 0.0),
        total=expense_dict.get("total", 0.0),
        line_items=expense_dict.get("line_items", []),
        currency=expense_dict.get("currency", "USD"),
        confidence=expense_dict.get("confidence", 0.0),
        source_document=expense_dict.get("source_document", ""),
    )
    return store_expense_record(normalized)


def query_expenses(
    vendor_or_merchant: str = None, document_type: str = None, limit: int = 50
) -> list:
    collection = get_expense_collection()
    query = {}
    if vendor_or_merchant:
        query["vendor_or_merchant"] = vendor_or_merchant
    if document_type:
        query["document_type"] = document_type

    cursor = collection.find(query).limit(limit)
    return list(cursor)


def delete_expense_record(document_id: str) -> dict:
    collection = get_expense_collection()
    result = collection.delete_one({"_id": document_id})
    return {
        "deleted_count": result.deleted_count,
        "acknowledged": result.acknowledged,
    }
