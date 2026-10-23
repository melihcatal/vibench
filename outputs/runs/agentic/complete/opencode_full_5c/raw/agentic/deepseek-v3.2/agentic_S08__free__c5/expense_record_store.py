import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from document_models import ExpenseRecord


def store_expense_record(expense_record: ExpenseRecord) -> Dict[str, Any]:
    """
    Persist normalized expense records in MongoDB Atlas managed document store.
    """
    from pymongo import MongoClient
    from pymongo.errors import PyMongoError

    # MongoDB Atlas connection string
    connection_string = os.getenv("MONGODB_ATLAS_CONNECTION_STRING")

    if not connection_string:
        return {
            "stored": False,
            "error": "MongoDB Atlas connection string not configured",
            "record_id": None,
            "database": None,
            "collection": None,
        }

    try:
        # Connect to MongoDB Atlas
        client = MongoClient(connection_string)

        # Get database and collection
        db = client.get_database("expense_management")
        collection = db.get_collection("expense_records")

        # Convert expense record to dictionary
        record_dict = {
            "vendor_name": expense_record.vendor_name,
            "transaction_date": expense_record.transaction_date,
            "total_amount": expense_record.total_amount,
            "currency": expense_record.currency,
            "line_items": expense_record.line_items,
            "tax_amount": expense_record.tax_amount,
            "category": expense_record.category,
            "source_type": expense_record.source_type,
            "extraction_source": expense_record.extraction_source,
            "normalized_at": expense_record.normalized_at,
            "metadata": expense_record.metadata,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "status": "pending_review",
        }

        # Insert the record
        result = collection.insert_one(record_dict)

        # Create index for efficient querying if it doesn't exist
        collection.create_index([("vendor_name", 1)])
        collection.create_index([("transaction_date", -1)])
        collection.create_index([("category", 1)])
        collection.create_index([("status", 1)])

        storage_result = {
            "stored": True,
            "record_id": str(result.inserted_id),
            "database": "expense_management",
            "collection": "expense_records",
            "document_count": collection.count_documents({}),
            "storage_timestamp": datetime.utcnow().isoformat(),
            "mongodb_atlas_cluster": connection_string.split("@")[1].split("/")[0]
            if "@" in connection_string
            else "unknown",
        }

        # Close connection
        client.close()

        return storage_result

    except PyMongoError as e:
        return {
            "stored": False,
            "error": f"MongoDB error: {str(e)}",
            "record_id": None,
            "database": "expense_management",
            "collection": "expense_records",
            "storage_timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        return {
            "stored": False,
            "error": f"Unexpected error: {str(e)}",
            "record_id": None,
            "database": None,
            "collection": None,
            "storage_timestamp": datetime.utcnow().isoformat(),
        }


def batch_store_expense_records(records: List[ExpenseRecord]) -> Dict[str, Any]:
    """
    Store multiple expense records in batch.
    """
    from pymongo import MongoClient

    connection_string = os.getenv("MONGODB_ATLAS_CONNECTION_STRING")

    if not connection_string:
        return {
            "stored": False,
            "error": "MongoDB Atlas connection string not configured",
            "stored_count": 0,
            "failed_count": len(records),
        }

    try:
        client = MongoClient(connection_string)
        db = client.get_database("expense_management")
        collection = db.get_collection("expense_records")

        records_to_insert = []
        for record in records:
            record_dict = {
                "vendor_name": record.vendor_name,
                "transaction_date": record.transaction_date,
                "total_amount": record.total_amount,
                "currency": record.currency,
                "line_items": record.line_items,
                "tax_amount": record.tax_amount,
                "category": record.category,
                "source_type": record.source_type,
                "extraction_source": record.extraction_source,
                "normalized_at": record.normalized_at,
                "metadata": record.metadata,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
                "status": "pending_review",
            }
            records_to_insert.append(record_dict)

        # Insert in batch
        if records_to_insert:
            result = collection.insert_many(records_to_insert)
            stored_count = len(result.inserted_ids)
        else:
            stored_count = 0

        client.close()

        return {
            "stored": True,
            "stored_count": stored_count,
            "failed_count": len(records) - stored_count,
            "batch_size": len(records),
            "batch_timestamp": datetime.utcnow().isoformat(),
            "mongodb_atlas_cluster": connection_string.split("@")[1].split("/")[0]
            if "@" in connection_string
            else "unknown",
        }

    except Exception as e:
        return {
            "stored": False,
            "error": str(e),
            "stored_count": 0,
            "failed_count": len(records),
            "batch_timestamp": datetime.utcnow().isoformat(),
        }


def query_expense_records(
    query: Dict[str, Any] = None, limit: int = 100
) -> Dict[str, Any]:
    """
    Query expense records from MongoDB Atlas.
    """
    from pymongo import MongoClient

    connection_string = os.getenv("MONGODB_ATLAS_CONNECTION_STRING")

    if not connection_string:
        return {
            "success": False,
            "error": "MongoDB Atlas connection string not configured",
            "records": [],
            "count": 0,
        }

    try:
        client = MongoClient(connection_string)
        db = client.get_database("expense_management")
        collection = db.get_collection("expense_records")

        # Default query if none provided
        if query is None:
            query = {}

        # Execute query
        cursor = collection.find(query).limit(limit)
        records = list(cursor)

        # Convert ObjectId to string for JSON serialization
        for record in records:
            if "_id" in record:
                record["_id"] = str(record["_id"])

        client.close()

        return {
            "success": True,
            "records": records,
            "count": len(records),
            "query_executed": query,
            "limit_applied": limit,
            "query_timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "records": [],
            "count": 0,
            "query_timestamp": datetime.utcnow().isoformat(),
        }


def update_expense_record_status(
    record_id: str, status: str, update_data: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Update the status of an expense record.
    """
    from pymongo import MongoClient
    from bson import ObjectId

    connection_string = os.getenv("MONGODB_ATLAS_CONNECTION_STRING")

    if not connection_string:
        return {
            "updated": False,
            "error": "MongoDB Atlas connection string not configured",
            "record_id": record_id,
        }

    try:
        client = MongoClient(connection_string)
        db = client.get_database("expense_management")
        collection = db.get_collection("expense_records")

        update_query = {
            "$set": {"status": status, "updated_at": datetime.utcnow().isoformat()}
        }

        if update_data:
            update_query["$set"].update(update_data)

        result = collection.update_one({"_id": ObjectId(record_id)}, update_query)

        client.close()

        return {
            "updated": result.modified_count > 0,
            "matched_count": result.matched_count,
            "modified_count": result.modified_count,
            "record_id": record_id,
            "new_status": status,
            "update_timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        return {
            "updated": False,
            "error": str(e),
            "record_id": record_id,
            "update_timestamp": datetime.utcnow().isoformat(),
        }


if __name__ == "__main__":
    # Example usage
    from document_models import ExpenseRecord

    sample_record = ExpenseRecord(
        vendor_name="Office Supplies Inc.",
        transaction_date="2024-01-15",
        total_amount=1250.75,
        currency="USD",
        line_items=[
            {
                "description": "Desk chairs",
                "quantity": 5,
                "unit_price": 200,
                "amount": 1000,
            },
            {
                "description": "Desk lamps",
                "quantity": 3,
                "unit_price": 83.58,
                "amount": 250.75,
            },
        ],
        tax_amount=87.55,
        category="Office Equipment",
        source_type="invoice",
        extraction_source="azure_form_recognizer",
    )

    storage_result = store_expense_record(sample_record)
    print(json.dumps(storage_result, indent=2))
