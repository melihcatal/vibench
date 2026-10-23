"""
[LATER-STEP] Persist normalized expense records in a managed document store using MongoDB Atlas.

Uses the PyMongo SDK to store normalized expense records in a MongoDB Atlas cluster
as a managed NoSQL document database.
Provider: MongoDB Atlas
SDK: pymongo
Auth: MONGODB_ATLAS_URI
"""

from __future__ import annotations

import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from bson import ObjectId
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from document_models import NormalizedExpenseRecord


# MongoDB Atlas configuration
MONGODB_ATLAS_URI_ENV = "MONGODB_ATLAS_URI"
DEFAULT_DATABASE_NAME = "expense_management"
DEFAULT_COLLECTION_NAME = "expenses"


def _get_mongodb_client(uri: Optional[str] = None) -> MongoClient:
    """Create and return a MongoDB Atlas client."""
    connection_uri = uri or os.environ.get(MONGODB_ATLAS_URI_ENV)
    if not connection_uri:
        raise EnvironmentError(
            f"MongoDB Atlas URI not found. Set the {MONGODB_ATLAS_URI_ENV} environment variable."
        )
    client = MongoClient(connection_uri)
    # Verify connection
    client.admin.command("ping")
    return client


def _get_expense_collection(
    client: Optional[MongoClient] = None,
    database_name: str = DEFAULT_DATABASE_NAME,
    collection_name: str = DEFAULT_COLLECTION_NAME,
) -> Collection:
    """Get or create the expense records collection."""
    if client is None:
        client = _get_mongodb_client()
    db = client[database_name]
    return db[collection_name]


def _expense_to_document(expense: NormalizedExpenseRecord) -> Dict[str, Any]:
    """Convert a NormalizedExpenseRecord to a MongoDB document."""
    doc = {}
    if hasattr(expense, "model_dump"):
        doc = expense.model_dump()
    elif hasattr(expense, "dict"):
        doc = expense.dict()

    # Convert Decimal and date types for MongoDB BSON compatibility
    for key, value in doc.items():
        if value is not None:
            if hasattr(value, "__float__") and key in ("subtotal", "tax_amount", "tip_amount", "total_amount"):
                doc[key] = float(value)
            elif isinstance(value, datetime):
                doc[key] = value
            elif hasattr(value, "isoformat"):
                doc[key] = value.isoformat()

    return doc


def store_expense_record(
    expense: NormalizedExpenseRecord,
    uri: Optional[str] = None,
    database_name: str = DEFAULT_DATABASE_NAME,
    collection_name: str = DEFAULT_COLLECTION_NAME,
) -> str:
    """
    Store a normalized expense record in MongoDB Atlas.

    Inserts the expense record into the configured MongoDB Atlas collection
    and returns the inserted document ID.

    Args:
        expense: NormalizedExpenseRecord to store.
        uri: Optional MongoDB Atlas connection URI override.
        database_name: MongoDB database name.
        collection_name: MongoDB collection name.

    Returns:
        The inserted document ID as a string.
    """
    client = _get_mongodb_client(uri)
    collection = _get_expense_collection(client, database_name, collection_name)

    doc = _expense_to_document(expense)
    doc["stored_at"] = datetime.utcnow()
    doc["provider"] = "MongoDB Atlas"

    result = collection.insert_one(doc)
    client.close()

    return str(result.inserted_id)


def store_expense_records(
    expenses: List[NormalizedExpenseRecord],
    uri: Optional[str] = None,
    database_name: str = DEFAULT_DATABASE_NAME,
    collection_name: str = DEFAULT_COLLECTION_NAME,
) -> List[str]:
    """
    Bulk store multiple normalized expense records in MongoDB Atlas.

    Args:
        expenses: List of NormalizedExpenseRecord objects to store.
        uri: Optional MongoDB Atlas connection URI.
        database_name: MongoDB database name.
        collection_name: MongoDB collection name.

    Returns:
        List of inserted document IDs.
    """
    client = _get_mongodb_client(uri)
    collection = _get_expense_collection(client, database_name, collection_name)

    documents = []
    for expense in expenses:
        doc = _expense_to_document(expense)
        doc["stored_at"] = datetime.utcnow()
        doc["provider"] = "MongoDB Atlas"
        documents.append(doc)

    if documents:
        result = collection.insert_many(documents)
        inserted_ids = [str(oid) for oid in result.inserted_ids]
    else:
        inserted_ids = []

    client.close()
    return inserted_ids


def get_expense_record(
    expense_id: str,
    uri: Optional[str] = None,
    database_name: str = DEFAULT_DATABASE_NAME,
    collection_name: str = DEFAULT_COLLECTION_NAME,
) -> Optional[Dict[str, Any]]:
    """
    Retrieve a single expense record from MongoDB Atlas by ID.

    Args:
        expense_id: The MongoDB document ID.
        uri: Optional MongoDB Atlas connection URI.
        database_name: MongoDB database name.
        collection_name: MongoDB collection name.

    Returns:
        The expense document as a dictionary, or None if not found.
    """
    client = _get_mongodb_client(uri)
    collection = _get_expense_collection(client, database_name, collection_name)

    try:
        doc = collection.find_one({"_id": ObjectId(expense_id)})
    except Exception:
        doc = collection.find_one({"expense_id": expense_id})

    client.close()
    return doc


def query_expenses(
    uri: Optional[str] = None,
    database_name: str = DEFAULT_DATABASE_NAME,
    collection_name: str = DEFAULT_COLLECTION_NAME,
    vendor_name: Optional[str] = None,
    category: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    min_total: Optional[float] = None,
    max_total: Optional[float] = None,
    limit: int = 100,
) -> List[Dict[str, Any]]:
    """
    Query expense records from MongoDB Atlas with filters.

    Args:
        uri: Optional MongoDB Atlas connection URI.
        database_name: MongoDB database name.
        collection_name: MongoDB collection name.
        vendor_name: Filter by vendor name (case-insensitive).
        category: Filter by expense category.
        date_from: Filter expenses on or after this date.
        date_to: Filter expenses on or before this date.
        min_total: Filter expenses with total >= this amount.
        max_total: Filter expenses with total <= this amount.
        limit: Maximum number of results.

    Returns:
        List of matching expense documents.
    """
    client = _get_mongodb_client(uri)
    collection = _get_expense_collection(client, database_name, collection_name)

    query: Dict[str, Any] = {}

    if vendor_name:
        query["vendor_name"] = {"$regex": vendor_name, "$options": "i"}

    if category:
        query["category"] = category

    if date_from or date_to:
        date_query = {}
        if date_from:
            date_query["$gte"] = date_from
        if date_to:
            date_query["$lte"] = date_to
        query["document_date"] = date_query

    if min_total is not None:
        query["total_amount"] = {"$gte": min_total}
    if max_total is not None:
        query.setdefault("total_amount", {})["$lte"] = max_total

    cursor = collection.find(query).limit(limit).sort("document_date", -1)
    results = list(cursor)

    client.close()
    return results


def update_expense_record(
    expense_id: str,
    updates: Dict[str, Any],
    uri: Optional[str] = None,
    database_name: str = DEFAULT_DATABASE_NAME,
    collection_name: str = DEFAULT_COLLECTION_NAME,
) -> bool:
    """
    Update an existing expense record in MongoDB Atlas.

    Args:
        expense_id: The expense record ID to update.
        updates: Dictionary of field updates.
        uri: Optional MongoDB Atlas connection URI.
        database_name: MongoDB database name.
        collection_name: MongoDB collection name.

    Returns:
        True if a document was updated, False otherwise.
    """
    client = _get_mongodb_client(uri)
    collection = _get_expense_collection(client, database_name, collection_name)

    updates["updated_at"] = datetime.utcnow()

    try:
        result = collection.update_one(
            {"_id": ObjectId(expense_id)},
            {"$set": updates},
        )
    except Exception:
        result = collection.update_one(
            {"expense_id": expense_id},
            {"$set": updates},
        )

    client.close()
    return result.modified_count > 0


def delete_expense_record(
    expense_id: str,
    uri: Optional[str] = None,
    database_name: str = DEFAULT_DATABASE_NAME,
    collection_name: str = DEFAULT_COLLECTION_NAME,
) -> bool:
    """
    Delete an expense record from MongoDB Atlas.

    Args:
        expense_id: The expense record ID to delete.
        uri: Optional MongoDB Atlas connection URI.
        database_name: MongoDB database name.
        collection_name: MongoDB collection name.

    Returns:
        True if a document was deleted, False otherwise.
    """
    client = _get_mongodb_client(uri)
    collection = _get_expense_collection(client, database_name, collection_name)

    try:
        result = collection.delete_one({"_id": ObjectId(expense_id)})
    except Exception:
        result = collection.delete_one({"expense_id": expense_id})

    client.close()
    return result.deleted_count > 0
