"""Persist normalized expense records in a managed document store using MongoDB Atlas."""

import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime

from pymongo import MongoClient, errors
from bson import ObjectId

from document_models import NormalizedExpense


MONGODB_ATLAS_CONNECTION_STRING = os.environ.get(
    "MONGODB_ATLAS_CONNECTION_STRING", "mongodb://localhost:27017"
)
MONGODB_ATLAS_DATABASE = os.environ.get("MONGODB_ATLAS_DATABASE", "expenses_db")
MONGODB_ATLAS_COLLECTION = os.environ.get("MONGODB_ATLAS_COLLECTION", "expense_records")


def get_mongo_client(
    connection_string: str = MONGODB_ATLAS_CONNECTION_STRING
) -> MongoClient:
    """Create a MongoDB Atlas client connection."""
    return MongoClient(connection_string)


def store_expense_record(
    expense: NormalizedExpense,
    connection_string: str = MONGODB_ATLAS_CONNECTION_STRING,
    database_name: str = MONGODB_ATLAS_DATABASE,
    collection_name: str = MONGODB_ATLAS_COLLECTION
) -> Dict[str, Any]:
    """
    Store a single normalized expense record in MongoDB Atlas.
    Returns the stored document with its MongoDB ObjectId.
    """
    client = get_mongo_client(connection_string)
    db = client[database_name]
    collection = db[collection_name]

    doc = expense.model_dump()
    doc["stored_at"] = datetime.utcnow().isoformat()
    doc["provider"] = "mongodb_atlas"

    try:
        result = collection.insert_one(doc)
        return {
            "stored": True,
            "document_id": str(result.inserted_id),
            "database": database_name,
            "collection": collection_name,
            "provider": "mongodb_atlas",
            "entity_name": expense.entity_name,
            "total_amount": expense.total_amount
        }
    except errors.PyMongoError as e:
        return {
            "stored": False,
            "error": str(e),
            "provider": "mongodb_atlas"
        }


def store_expense_records_batch(
    expenses: List[NormalizedExpense],
    connection_string: str = MONGODB_ATLAS_CONNECTION_STRING,
    database_name: str = MONGODB_ATLAS_DATABASE,
    collection_name: str = MONGODB_ATLAS_COLLECTION
) -> Dict[str, Any]:
    """
    Store multiple normalized expense records in MongoDB Atlas using bulk insert.
    Returns summary of the batch operation.
    """
    client = get_mongo_client(connection_string)
    db = client[database_name]
    collection = db[collection_name]

    documents = []
    for expense in expenses:
        doc = expense.model_dump()
        doc["stored_at"] = datetime.utcnow().isoformat()
        doc["provider"] = "mongodb_atlas"
        documents.append(doc)

    try:
        result = collection.insert_many(documents, ordered=False)
        return {
            "stored": True,
            "inserted_count": len(result.inserted_ids),
            "document_ids": [str(oid) for oid in result.inserted_ids],
            "database": database_name,
            "collection": collection_name,
            "provider": "mongodb_atlas"
        }
    except errors.BulkWriteError as bwe:
        return {
            "stored": False,
            "error": str(bwe),
            "details": bwe.details,
            "provider": "mongodb_atlas"
        }
    except errors.PyMongoError as e:
        return {
            "stored": False,
            "error": str(e),
            "provider": "mongodb_atlas"
        }


def query_expense_records(
    query: Dict[str, Any] = {},
    limit: int = 100,
    connection_string: str = MONGODB_ATLAS_CONNECTION_STRING,
    database_name: str = MONGODB_ATLAS_DATABASE,
    collection_name: str = MONGODB_ATLAS_COLLECTION
) -> List[Dict[str, Any]]:
    """Query stored expense records from MongoDB Atlas."""
    client = get_mongo_client(connection_string)
    db = client[database_name]
    collection = db[collection_name]

    results = []
    for doc in collection.find(query).limit(limit):
        doc["_id"] = str(doc["_id"])
        results.append(doc)

    return results


def update_expense_record(
    document_id: str,
    updates: Dict[str, Any],
    connection_string: str = MONGODB_ATLAS_CONNECTION_STRING,
    database_name: str = MONGODB_ATLAS_DATABASE,
    collection_name: str = MONGODB_ATLAS_COLLECTION
) -> Dict[str, Any]:
    """Update an existing expense record in MongoDB Atlas."""
    client = get_mongo_client(connection_string)
    db = client[database_name]
    collection = db[collection_name]

    updates["updated_at"] = datetime.utcnow().isoformat()

    try:
        result = collection.update_one(
            {"_id": ObjectId(document_id)},
            {"$set": updates}
        )
        return {
            "matched": result.matched_count,
            "modified": result.modified_count,
            "provider": "mongodb_atlas"
        }
    except errors.PyMongoError as e:
        return {
            "matched": 0,
            "modified": 0,
            "error": str(e),
            "provider": "mongodb_atlas"
        }


def delete_expense_record(
    document_id: str,
    connection_string: str = MONGODB_ATLAS_CONNECTION_STRING,
    database_name: str = MONGODB_ATLAS_DATABASE,
    collection_name: str = MONGODB_ATLAS_COLLECTION
) -> Dict[str, Any]:
    """Delete an expense record from MongoDB Atlas."""
    client = get_mongo_client(connection_string)
    db = client[database_name]
    collection = db[collection_name]

    try:
        result = collection.delete_one({"_id": ObjectId(document_id)})
        return {
            "deleted": result.deleted_count > 0,
            "deleted_count": result.deleted_count,
            "provider": "mongodb_atlas"
        }
    except errors.PyMongoError as e:
        return {
            "deleted": False,
            "error": str(e),
            "provider": "mongodb_atlas"
        }


def create_expense_search_index(
    index_name: str = "expense_search",
    connection_string: str = MONGODB_ATLAS_CONNECTION_STRING,
    database_name: str = MONGODB_ATLAS_DATABASE,
    collection_name: str = MONGODB_ATLAS_COLLECTION
) -> Dict[str, Any]:
    """Create an Atlas Search index for full-text search on expense records."""
    client = get_mongo_client(connection_string)
    db = client[database_name]
    collection = db[collection_name]

    index_definition = {
        "mappings": {
            "dynamic": False,
            "fields": {
                "entity_name": {"type": "string"},
                "document_type": {"type": "string"},
                "total_amount": {"type": "number"},
                "transaction_date": {"type": "date"},
                "validation_status": {"type": "string"},
                "currency": {"type": "string"}
            }
        }
    }

    try:
        collection.create_search_index(
            name=index_name,
            definition=index_definition
        )
        return {
            "created": True,
            "index_name": index_name,
            "provider": "mongodb_atlas"
        }
    except errors.PyMongoError as e:
        return {
            "created": False,
            "error": str(e),
            "provider": "mongodb_atlas"
        }


if __name__ == "__main__":
    expense = NormalizedExpense(
        entity_name="Test Vendor LLC",
        document_type="invoice",
        transaction_date="2024-11-15",
        total_amount=1250.00,
        tax_amount=125.00,
        currency="USD",
        line_items=[
            {"description": "Office chairs", "quantity": 5, "unit_price": 200.0, "total": 1000.0},
            {"description": "Desk lamps", "quantity": 10, "unit_price": 25.0, "total": 250.0}
        ],
        metadata={"source": "test"},
        validation_status="pending",
        created_at=datetime.utcnow().isoformat()
    )
    result = store_expense_record(expense)
    print(json.dumps(result, indent=2, default=str))
