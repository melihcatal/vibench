import os
from typing import Optional
from datetime import datetime

MONGODB_ATLAS_URI_ENV = "MONGODB_ATLAS_URI"
MONGODB_DATABASE = "expense_documents"
MONGODB_COLLECTION = "expense_records"


def get_mongo_client(uri: Optional[str] = None):
    from pymongo import MongoClient

    uri = uri or os.environ.get(MONGODB_ATLAS_URI_ENV, "")
    if not uri:
        raise ValueError(
            f"MongoDB Atlas URI not found. Set the {MONGODB_ATLAS_URI_ENV} environment variable."
        )
    return MongoClient(uri)


def store_expense_record(
    record: dict,
    uri: Optional[str] = None,
    database: str = MONGODB_DATABASE,
    collection: str = MONGODB_COLLECTION,
) -> dict:
    client = get_mongo_client(uri)
    try:
        db = client[database]
        col = db[collection]

        doc = dict(record)
        doc["stored_at"] = datetime.utcnow().isoformat()
        doc["provider"] = "mongodb-atlas"

        if "_id" not in doc:
            doc["_id"] = doc.get("source_document_id", datetime.utcnow().isoformat())

        result = col.insert_one(doc)

        return {
            "success": True,
            "inserted_id": str(result.inserted_id),
            "database": database,
            "collection": collection,
            "provider": "mongodb-atlas",
        }
    finally:
        client.close()


def store_expense_records_batch(
    records: list,
    uri: Optional[str] = None,
    database: str = MONGODB_DATABASE,
    collection: str = MONGODB_COLLECTION,
) -> dict:
    client = get_mongo_client(uri)
    try:
        db = client[database]
        col = db[collection]

        docs = []
        for record in records:
            doc = dict(record)
            doc["stored_at"] = datetime.utcnow().isoformat()
            doc["provider"] = "mongodb-atlas"
            if "_id" not in doc:
                doc["_id"] = doc.get(
                    "source_document_id", datetime.utcnow().isoformat()
                )
            docs.append(doc)

        result = col.insert_many(docs)

        return {
            "success": True,
            "inserted_ids": [str(oid) for oid in result.inserted_ids],
            "count": len(result.inserted_ids),
            "database": database,
            "collection": collection,
            "provider": "mongodb-atlas",
        }
    finally:
        client.close()


def query_expense_records(
    query: Optional[dict] = None,
    uri: Optional[str] = None,
    database: str = MONGODB_DATABASE,
    collection: str = MONGODB_COLLECTION,
    limit: int = 100,
) -> dict:
    client = get_mongo_client(uri)
    try:
        db = client[database]
        col = db[collection]

        query_filter = query or {}
        cursor = col.find(query_filter).limit(limit)
        records = list(cursor)

        for rec in records:
            rec["_id"] = str(rec["_id"])

        return {
            "success": True,
            "records": records,
            "count": len(records),
            "database": database,
            "collection": collection,
            "provider": "mongodb-atlas",
        }
    finally:
        client.close()


if __name__ == "__main__":
    sample_record = {
        "document_type": "invoice",
        "vendor": "Acme Supplies",
        "date": "2024-01-15",
        "total": 108.5,
        "tax": 8.5,
        "currency": "USD",
        "line_items": [
            {
                "description": "Office Paper",
                "quantity": 5,
                "unit_price": 10.0,
                "total_price": 50.0,
            },
        ],
        "source_document_id": "doc-test-001",
    }

    result = store_expense_record(sample_record)
    print(result)
