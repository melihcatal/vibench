"""Persist normalized expense records in MongoDB Atlas.

Uses pymongo SDK to connect to MongoDB Atlas and store normalized
expense records in a managed document collection.
Auth env var: MONGODB_ATLAS_URI
"""

import os
import json
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from document_models import NormalizedExpense, StandardExpenseSchema


DEFAULT_DB_NAME = "expense_tracker"
DEFAULT_COLLECTION_NAME = "expenses"


def get_mongo_client() -> MongoClient:
    """Create and return a MongoDB Atlas client.

    Uses the MONGODB_ATLAS_URI environment variable for connection.
    """
    uri = os.environ.get("MONGODB_ATLAS_URI", "")
    if not uri:
        raise EnvironmentError("MONGODB_ATLAS_URI environment variable is not set")
    return MongoClient(uri)


def store_expense_record(
    expense: NormalizedExpense,
    db_name: str = DEFAULT_DB_NAME,
    collection_name: str = DEFAULT_COLLECTION_NAME,
) -> Dict[str, Any]:
    """Store a normalized expense record in MongoDB Atlas.

    Inserts the expense document into the specified collection with
    an added _id, stored_at timestamp, and document_version.

    Args:
        expense: NormalizedExpense to persist.
        db_name: MongoDB database name.
        collection_name: MongoDB collection name.

    Returns:
        Dictionary with inserted document ID and metadata.
    """
    client = get_mongo_client()

    try:
        db = client[db_name]
        collection = db[collection_name]

        document = expense.model_dump()
        document["_id"] = str(uuid.uuid4())
        document["stored_at"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        document["document_version"] = 1

        result = collection.insert_one(document)

        return {
            "inserted_id": str(result.inserted_id),
            "acknowledged": result.acknowledged,
            "document_id": document["_id"],
            "stored_at": document["stored_at"],
        }
    finally:
        client.close()


def store_multiple_expenses(
    expenses: List[NormalizedExpense],
    db_name: str = DEFAULT_DB_NAME,
    collection_name: str = DEFAULT_COLLECTION_NAME,
) -> Dict[str, Any]:
    """Store multiple normalized expense records in MongoDB Atlas.

    Args:
        expenses: List of NormalizedExpense objects to persist.
        db_name: MongoDB database name.
        collection_name: MongoDB collection name.

    Returns:
        Dictionary with insertion metadata.
    """
    client = get_mongo_client()

    try:
        db = client[db_name]
        collection = db[collection_name]

        documents = []
        for expense in expenses:
            document = expense.model_dump()
            document["_id"] = str(uuid.uuid4())
            document["stored_at"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            document["document_version"] = 1
            documents.append(document)

        result = collection.insert_many(documents)

        return {
            "inserted_ids": [str(iid) for iid in result.inserted_ids],
            "inserted_count": len(result.inserted_ids),
            "acknowledged": result.acknowledged,
        }
    finally:
        client.close()


def query_expenses(
    vendor: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    min_confidence: float = 0.0,
    db_name: str = DEFAULT_DB_NAME,
    collection_name: str = DEFAULT_COLLECTION_NAME,
    limit: int = 100,
) -> List[Dict[str, Any]]:
    """Query stored expense records from MongoDB Atlas with filters.

    Args:
        vendor: Filter by vendor name (case-insensitive regex).
        date_from: Filter by date range start (ISO format).
        date_to: Filter by date range end (ISO format).
        min_confidence: Minimum extraction confidence threshold.
        db_name: MongoDB database name.
        collection_name: MongoDB collection name.
        limit: Maximum number of results.

    Returns:
        List of matching expense documents.
    """
    client = get_mongo_client()

    try:
        db = client[db_name]
        collection = db[collection_name]

        query: Dict[str, Any] = {}

        if vendor:
            query["standard_schema.vendor"] = {"$regex": vendor, "$options": "i"}

        if date_from or date_to:
            date_query = {}
            if date_from:
                date_query["$gte"] = date_from
            if date_to:
                date_query["$lte"] = date_to
            query["standard_schema.date"] = date_query

        if min_confidence > 0:
            query["standard_schema.confidence"] = {"$gte": min_confidence}

        cursor = collection.find(query).limit(limit).sort("stored_at", -1)

        results = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            results.append(doc)

        return results
    finally:
        client.close()


def delete_expense_record(
    document_id: str,
    db_name: str = DEFAULT_DB_NAME,
    collection_name: str = DEFAULT_COLLECTION_NAME,
) -> Dict[str, Any]:
    """Delete a stored expense record from MongoDB Atlas.

    Args:
        document_id: The stored document _id to delete.
        db_name: MongoDB database name.
        collection_name: MongoDB collection name.

    Returns:
        Dictionary with deletion metadata.
    """
    client = get_mongo_client()

    try:
        db = client[db_name]
        collection = db[collection_name]

        result = collection.delete_one({"_id": document_id})

        return {
            "deleted_count": result.deleted_count,
            "acknowledged": result.acknowledged,
        }
    finally:
        client.close()


if __name__ == "__main__":
    from normalize_expense import normalize_expense

    sample_data = {
        "vendor_name": "Acme Supplies",
        "invoice_date": "2024-01-15",
        "total_amount": 250.00,
        "tax_amount": 20.00,
        "line_items": [
            {"description": "Office supplies", "quantity": 5, "unit_price": 40.00, "amount": 200.00},
            {"description": "Shipping", "quantity": 1, "unit_price": 50.00, "amount": 50.00},
        ],
        "confidence": 0.95,
        "raw_fields": {"VendorName": "Acme Supplies", "InvoiceTotal": 250.0},
    }

    expense = normalize_expense(sample_data, source="invoice")
    result = store_expense_record(expense)
    print(json.dumps(result, indent=2))
