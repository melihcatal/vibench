from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from document_models import ExpenseRecord, expense_record_to_dict
from document_client import (
    MONGODB_CONNECTION_STRING,
    MONGODB_DATABASE,
    MONGODB_COLLECTION,
    validate_mongodb_credentials,
    get_mongodb_client_config,
)


def store_expense_record(
    record: ExpenseRecord,
    connection_string: str = "",
    database_name: str = "",
    collection_name: str = "",
) -> str:
    conn_str = connection_string or MONGODB_CONNECTION_STRING
    db_name = database_name or MONGODB_DATABASE
    col_name = collection_name or MONGODB_COLLECTION

    if not conn_str:
        raise ValueError(
            "MongoDB connection string not configured. Set MONGODB_CONNECTION_STRING."
        )

    client = MongoClient(conn_str)
    db = client[db_name]
    collection = db[col_name]

    record_dict = expense_record_to_dict(record)

    if not record_dict.get("record_id"):
        record_dict["record_id"] = str(ObjectId())

    if not record_dict.get("normalized_at"):
        record_dict["normalized_at"] = datetime.utcnow().isoformat()

    record_dict["stored_at"] = datetime.utcnow().isoformat()
    record_dict["provider"] = "mongodb_atlas"

    result = collection.insert_one(record_dict)
    client.close()

    return str(result.inserted_id)


def store_expense_records_batch(
    records: list[ExpenseRecord],
    connection_string: str = "",
    database_name: str = "",
    collection_name: str = "",
) -> list[str]:
    conn_str = connection_string or MONGODB_CONNECTION_STRING
    db_name = database_name or MONGODB_DATABASE
    col_name = collection_name or MONGODB_COLLECTION

    if not conn_str:
        raise ValueError(
            "MongoDB connection string not configured. Set MONGODB_CONNECTION_STRING."
        )

    client = MongoClient(conn_str)
    db = client[db_name]
    collection = db[col_name]

    documents = []
    for record in records:
        record_dict = expense_record_to_dict(record)
        if not record_dict.get("record_id"):
            record_dict["record_id"] = str(ObjectId())
        if not record_dict.get("normalized_at"):
            record_dict["normalized_at"] = datetime.utcnow().isoformat()
        record_dict["stored_at"] = datetime.utcnow().isoformat()
        record_dict["provider"] = "mongodb_atlas"
        documents.append(record_dict)

    result = collection.insert_many(documents)
    client.close()

    return [str(oid) for oid in result.inserted_ids]


def retrieve_expense_record(
    record_id: str,
    connection_string: str = "",
    database_name: str = "",
    collection_name: str = "",
) -> ExpenseRecord | None:
    conn_str = connection_string or MONGODB_CONNECTION_STRING
    db_name = database_name or MONGODB_DATABASE
    col_name = collection_name or MONGODB_COLLECTION

    if not conn_str:
        raise ValueError(
            "MongoDB connection string not configured. Set MONGODB_CONNECTION_STRING."
        )

    client = MongoClient(conn_str)
    db = client[db_name]
    collection = db[col_name]

    doc = collection.find_one({"record_id": record_id})
    client.close()

    if doc is None:
        return None

    doc.pop("_id", None)
    doc.pop("stored_at", None)
    doc.pop("provider", None)

    return ExpenseRecord(**doc)


def query_expense_records(
    vendor_or_merchant: str = "",
    document_type: str = "",
    date_from: str = "",
    date_to: str = "",
    min_total: float = 0.0,
    connection_string: str = "",
    database_name: str = "",
    collection_name: str = "",
) -> list[ExpenseRecord]:
    conn_str = connection_string or MONGODB_CONNECTION_STRING
    db_name = database_name or MONGODB_DATABASE
    col_name = collection_name or MONGODB_COLLECTION

    if not conn_str:
        raise ValueError(
            "MongoDB connection string not configured. Set MONGODB_CONNECTION_STRING."
        )

    client = MongoClient(conn_str)
    db = client[db_name]
    collection = db[col_name]

    query: dict = {}
    if vendor_or_merchant:
        query["vendor_or_merchant"] = {"$regex": vendor_or_merchant, "$options": "i"}
    if document_type:
        query["document_type"] = document_type
    if date_from or date_to:
        date_range: dict = {}
        if date_from:
            date_range["$gte"] = date_from
        if date_to:
            date_range["$lte"] = date_to
        query["date"] = date_range
    if min_total > 0:
        query["total_amount"] = {"$gte": min_total}

    cursor = collection.find(query)
    records = []
    for doc in cursor:
        doc.pop("_id", None)
        doc.pop("stored_at", None)
        doc.pop("provider", None)
        records.append(ExpenseRecord(**doc))

    client.close()
    return records


def delete_expense_record(
    record_id: str,
    connection_string: str = "",
    database_name: str = "",
    collection_name: str = "",
) -> bool:
    conn_str = connection_string or MONGODB_CONNECTION_STRING
    db_name = database_name or MONGODB_DATABASE
    col_name = collection_name or MONGODB_COLLECTION

    if not conn_str:
        raise ValueError(
            "MongoDB connection string not configured. Set MONGODB_CONNECTION_STRING."
        )

    client = MongoClient(conn_str)
    db = client[db_name]
    collection = db[col_name]

    result = collection.delete_one({"record_id": record_id})
    client.close()

    return result.deleted_count > 0
