import os
from typing import Dict, List, Any, Optional
import json
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import PyMongoError


def store_expense_record(expense_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Persist normalized expense records in MongoDB Atlas.
    """
    connection_string = os.getenv("MONGODB_ATLAS_CONNECTION_STRING")

    if not connection_string:
        raise ValueError("MongoDB Atlas connection string not configured")

    try:
        client = MongoClient(connection_string)

        db_name = os.getenv("MONGODB_DATABASE", "expense_tracker")
        collection_name = os.getenv("MONGODB_COLLECTION", "expenses")

        db = client[db_name]
        collection = db[collection_name]

        record_id = expense_data.get("id")
        if not record_id:
            record_id = f"exp_{datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')}"
            expense_data["id"] = record_id

        expense_data["stored_at"] = datetime.utcnow().isoformat()
        expense_data["database"] = db_name
        expense_data["collection"] = collection_name

        if "_id" not in expense_data:
            expense_data["_id"] = record_id

        result = collection.insert_one(expense_data)

        stored_record = collection.find_one({"_id": result.inserted_id})

        if stored_record and "_id" in stored_record:
            stored_record["id"] = str(stored_record["_id"])

        storage_result = {
            "success": True,
            "record_id": record_id,
            "mongodb_id": str(result.inserted_id),
            "database": db_name,
            "collection": collection_name,
            "stored_at": expense_data["stored_at"],
            "provider": "mongodb_atlas",
            "record_summary": {
                "vendor": expense_data.get("vendor_name"),
                "amount": expense_data.get("total_amount"),
                "currency": expense_data.get("currency"),
                "date": expense_data.get("transaction_date"),
            },
        }

        client.close()

        return storage_result

    except PyMongoError as e:
        return {
            "success": False,
            "error": str(e),
            "provider": "mongodb_atlas",
            "attempted_at": datetime.utcnow().isoformat(),
        }


def batch_store_expense_records(
    expense_records: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Store multiple expense records in batch.
    """
    connection_string = os.getenv("MONGODB_ATLAS_CONNECTION_STRING")

    if not connection_string:
        raise ValueError("MongoDB Atlas connection string not configured")

    try:
        client = MongoClient(connection_string)

        db_name = os.getenv("MONGODB_DATABASE", "expense_tracker")
        collection_name = os.getenv("MONGODB_COLLECTION", "expenses")

        db = client[db_name]
        collection = db[collection_name]

        processed_records = []
        for record in expense_records:
            if "id" not in record:
                record["id"] = f"exp_{datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')}"

            record["stored_at"] = datetime.utcnow().isoformat()
            record["batch_processed"] = True

            if "_id" not in record:
                record["_id"] = record["id"]

            processed_records.append(record)

        if processed_records:
            result = collection.insert_many(processed_records)

            inserted_ids = [str(id) for id in result.inserted_ids]

            batch_result = {
                "success": True,
                "records_inserted": len(processed_records),
                "inserted_ids": inserted_ids,
                "database": db_name,
                "collection": collection_name,
                "batch_processed_at": datetime.utcnow().isoformat(),
                "provider": "mongodb_atlas",
                "batch_summary": {
                    "total_amount": sum(
                        r.get("total_amount", 0) for r in processed_records
                    ),
                    "record_count": len(processed_records),
                    "vendors": list(
                        set(
                            r.get("vendor_name")
                            for r in processed_records
                            if r.get("vendor_name")
                        )
                    ),
                },
            }
        else:
            batch_result = {
                "success": False,
                "error": "No records to store",
                "records_inserted": 0,
            }

        client.close()

        return batch_result

    except PyMongoError as e:
        return {
            "success": False,
            "error": str(e),
            "provider": "mongodb_atlas",
            "attempted_at": datetime.utcnow().isoformat(),
            "records_attempted": len(expense_records),
        }


def query_expense_records(
    query: Dict[str, Any] = None, limit: int = 100
) -> List[Dict[str, Any]]:
    """
    Query expense records from MongoDB.
    """
    connection_string = os.getenv("MONGODB_ATLAS_CONNECTION_STRING")

    if not connection_string:
        raise ValueError("MongoDB Atlas connection string not configured")

    try:
        client = MongoClient(connection_string)

        db_name = os.getenv("MONGODB_DATABASE", "expense_tracker")
        collection_name = os.getenv("MONGODB_COLLECTION", "expenses")

        db = client[db_name]
        collection = db[collection_name]

        query = query or {}

        cursor = collection.find(query).limit(limit)

        results = []
        for doc in cursor:
            if "_id" in doc:
                doc["id"] = str(doc["_id"])
                del doc["_id"]
            results.append(doc)

        client.close()

        return results

    except PyMongoError as e:
        raise Exception(f"MongoDB query failed: {e}")
