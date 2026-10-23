import os
from pymongo import MongoClient
from document_models import NormalizedExpense


def store_expense_record(expense: NormalizedExpense) -> dict:
    connection_string = os.environ.get(
        "MONGODB_ATLAS_URI", "mongodb+srv://<username>:<password>@cluster0.mongodb.net/"
    )
    database_name = os.environ.get("MONGODB_DATABASE", "expense_documents")
    collection_name = os.environ.get("MONGODB_COLLECTION", "expenses")

    client = MongoClient(connection_string)
    db = client[database_name]
    collection = db[collection_name]

    record = expense.to_dict()

    result = collection.insert_one(record)

    return {
        "inserted_id": str(result.inserted_id),
        "acknowledged": result.acknowledged,
        "document_type": expense.document_type,
        "vendor": expense.vendor,
        "source_document_id": expense.source_document_id,
        "provider": "mongodb_atlas",
        "database": database_name,
        "collection": collection_name,
    }


def query_expense_records(vendor: str = None, limit: int = 10) -> list:
    connection_string = os.environ.get(
        "MONGODB_ATLAS_URI", "mongodb+srv://<username>:<password>@cluster0.mongodb.net/"
    )
    database_name = os.environ.get("MONGODB_DATABASE", "expense_documents")
    collection_name = os.environ.get("MONGODB_COLLECTION", "expenses")

    client = MongoClient(connection_string)
    db = client[database_name]
    collection = db[collection_name]

    query_filter = {}
    if vendor:
        query_filter["vendor"] = {"$regex": vendor, "$options": "i"}

    cursor = collection.find(query_filter).limit(limit)
    records = list(cursor)

    for record in records:
        record["_id"] = str(record["_id"])

    return records
