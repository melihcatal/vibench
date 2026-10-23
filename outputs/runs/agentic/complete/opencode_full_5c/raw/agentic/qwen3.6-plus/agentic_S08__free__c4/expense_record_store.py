import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson import ObjectId
from document_client import get_mongodb_config
from document_models import NormalizedExpense


MONGODB_ATLAS_CLUSTER = "mongodb-atlas"
MONGODB_DATABASE = "expense_documents"
MONGODB_COLLECTION = "normalized_expenses"


def store_expense_record(expense: NormalizedExpense) -> Dict[str, Any]:
    config = get_mongodb_config()
    connection_string = config["connection_string"]
    database_name = config.get("database_name", MONGODB_DATABASE)
    collection_name = config.get("collection_name", MONGODB_COLLECTION)

    client = MongoClient(connection_string)
    db = client[database_name]
    collection = db[collection_name]

    expense_dict = {
        "document_type": expense.document_type,
        "vendor": expense.vendor,
        "date": expense.date,
        "total": expense.total,
        "tax": expense.tax,
        "currency": expense.currency,
        "line_items": expense.line_items,
        "source_document_id": expense.source_document_id,
        "normalized_at": expense.normalized_at,
        "schema_version": expense.schema_version,
        "stored_at": datetime.utcnow().isoformat(),
        "storage_backend": MONGODB_ATLAS_CLUSTER,
    }

    try:
        result = collection.insert_one(expense_dict)
        return {
            "success": True,
            "document_id": str(result.inserted_id),
            "source_document_id": expense.source_document_id,
            "database": database_name,
            "collection": collection_name,
            "stored_at": expense_dict["stored_at"],
        }
    except PyMongoError as e:
        return {
            "success": False,
            "error": str(e),
            "source_document_id": expense.source_document_id,
        }
    finally:
        client.close()


def store_expense_records_batch(expenses: List[NormalizedExpense]) -> Dict[str, Any]:
    config = get_mongodb_config()
    connection_string = config["connection_string"]
    database_name = config.get("database_name", MONGODB_DATABASE)
    collection_name = config.get("collection_name", MONGODB_COLLECTION)

    client = MongoClient(connection_string)
    db = client[database_name]
    collection = db[collection_name]

    documents = []
    for expense in expenses:
        doc = {
            "document_type": expense.document_type,
            "vendor": expense.vendor,
            "date": expense.date,
            "total": expense.total,
            "tax": expense.tax,
            "currency": expense.currency,
            "line_items": expense.line_items,
            "source_document_id": expense.source_document_id,
            "normalized_at": expense.normalized_at,
            "schema_version": expense.schema_version,
            "stored_at": datetime.utcnow().isoformat(),
            "storage_backend": MONGODB_ATLAS_CLUSTER,
        }
        documents.append(doc)

    try:
        result = collection.insert_many(documents)
        return {
            "success": True,
            "inserted_count": len(result.inserted_ids),
            "document_ids": [str(oid) for oid in result.inserted_ids],
            "database": database_name,
            "collection": collection_name,
        }
    except PyMongoError as e:
        return {"success": False, "error": str(e), "attempted_count": len(documents)}
    finally:
        client.close()


def query_expense_records(
    vendor: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    min_total: Optional[float] = None,
    document_type: Optional[str] = None,
    limit: int = 100,
) -> List[Dict[str, Any]]:
    config = get_mongodb_config()
    connection_string = config["connection_string"]
    database_name = config.get("database_name", MONGODB_DATABASE)
    collection_name = config.get("collection_name", MONGODB_COLLECTION)

    client = MongoClient(connection_string)
    db = client[database_name]
    collection = db[collection_name]

    query = {}
    if vendor:
        query["vendor"] = {"$regex": vendor, "$options": "i"}
    if document_type:
        query["document_type"] = document_type
    if min_total is not None:
        query["total"] = {"$gte": min_total}
    if date_from or date_to:
        date_query = {}
        if date_from:
            date_query["$gte"] = date_from
        if date_to:
            date_query["$lte"] = date_to
        query["date"] = date_query

    cursor = collection.find(query).limit(limit).sort("stored_at", -1)
    results = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        results.append(doc)

    client.close()
    return results


def get_expense_record_by_id(record_id: str) -> Optional[Dict[str, Any]]:
    config = get_mongodb_config()
    connection_string = config["connection_string"]
    database_name = config.get("database_name", MONGODB_DATABASE)
    collection_name = config.get("collection_name", MONGODB_COLLECTION)

    client = MongoClient(connection_string)
    db = client[database_name]
    collection = db[collection_name]

    try:
        doc = collection.find_one({"_id": ObjectId(record_id)})
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc
    except PyMongoError:
        return None
    finally:
        client.close()


if __name__ == "__main__":
    sample_expense = NormalizedExpense(
        document_type="invoice",
        vendor="Test Vendor",
        date="2024-01-15",
        total=500.0,
        tax=50.0,
        currency="USD",
        source_document_id="test-doc-001",
        normalized_at=datetime.utcnow().isoformat(),
    )
    result = store_expense_record(sample_expense)
    print(json.dumps(result, indent=2))
