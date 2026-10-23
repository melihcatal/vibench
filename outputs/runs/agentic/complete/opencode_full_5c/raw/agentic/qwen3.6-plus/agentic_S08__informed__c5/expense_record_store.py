import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from document_models import NormalizedExpenseRecord

MONGODB_ATLAS_URI = os.environ.get("MONGODB_ATLAS_URI", "")
MONGODB_DATABASE = os.environ.get("MONGODB_DATABASE", "expense_documents")
MONGODB_COLLECTION = os.environ.get("MONGODB_COLLECTION", "expenses")


def get_mongo_client():
    if not MONGODB_ATLAS_URI:
        raise ValueError("MONGODB_ATLAS_URI must be set for MongoDB Atlas connection")
    client = MongoClient(MONGODB_ATLAS_URI)
    return client


def store_expense_record(
    expense_record: NormalizedExpenseRecord, db_name=None, collection_name=None
) -> str:
    client = get_mongo_client()
    db = client[db_name or MONGODB_DATABASE]
    collection = db[collection_name or MONGODB_COLLECTION]

    document = expense_record.to_dict()
    result = collection.insert_one(document)
    return str(result.inserted_id)


def store_multiple_expense_records(
    records: list, db_name=None, collection_name=None
) -> list:
    client = get_mongo_client()
    db = client[db_name or MONGODB_DATABASE]
    collection = db[collection_name or MONGODB_COLLECTION]

    documents = [record.to_dict() for record in records]
    result = collection.insert_many(documents)
    return [str(oid) for oid in result.inserted_ids]


def query_expense_records(
    vendor=None,
    source_type=None,
    date_from=None,
    date_to=None,
    db_name=None,
    collection_name=None,
) -> list:
    client = get_mongo_client()
    db = client[db_name or MONGODB_DATABASE]
    collection = db[collection_name or MONGODB_COLLECTION]

    query = {}
    if vendor:
        query["vendor_or_merchant"] = {"$regex": vendor, "$options": "i"}
    if source_type:
        query["source_type"] = source_type
    if date_from or date_to:
        date_filter = {}
        if date_from:
            date_filter["$gte"] = date_from
        if date_to:
            date_filter["$lte"] = date_to
        query["document_date"] = date_filter

    cursor = collection.find(query)
    return list(cursor)


def get_expense_record_by_id(
    record_id: str, db_name=None, collection_name=None
) -> dict:
    from bson import ObjectId

    client = get_mongo_client()
    db = client[db_name or MONGODB_DATABASE]
    collection = db[collection_name or MONGODB_COLLECTION]

    try:
        record = collection.find_one({"_id": ObjectId(record_id)})
    except Exception:
        record = collection.find_one({"_id": record_id})

    return record


def delete_expense_record(record_id: str, db_name=None, collection_name=None) -> bool:
    from bson import ObjectId

    client = get_mongo_client()
    db = client[db_name or MONGODB_DATABASE]
    collection = db[collection_name or MONGODB_COLLECTION]

    try:
        result = collection.delete_one({"_id": ObjectId(record_id)})
    except Exception:
        result = collection.delete_one({"_id": record_id})

    return result.deleted_count > 0


def update_expense_record(
    record_id: str, updates: dict, db_name=None, collection_name=None
) -> bool:
    from bson import ObjectId

    client = get_mongo_client()
    db = client[db_name or MONGODB_DATABASE]
    collection = db[collection_name or MONGODB_COLLECTION]

    try:
        result = collection.update_one({"_id": ObjectId(record_id)}, {"$set": updates})
    except Exception:
        result = collection.update_one({"_id": record_id}, {"$set": updates})

    return result.modified_count > 0
