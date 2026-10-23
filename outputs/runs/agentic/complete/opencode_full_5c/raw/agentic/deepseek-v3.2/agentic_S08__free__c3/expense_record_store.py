import os
from pymongo import MongoClient
from datetime import datetime
from document_client import load_config


def store_expense_record(expense_record):
    config = load_config()

    client = MongoClient(config["mongodb_uri"])
    db = client[config["mongodb_database"]]
    collection = db[config["mongodb_collection"]]

    record_with_metadata = {
        **expense_record,
        "stored_at": datetime.now().isoformat(),
        "database": config["mongodb_database"],
        "collection": config["mongodb_collection"],
    }

    result = collection.insert_one(record_with_metadata)

    return {
        "success": True,
        "record_id": str(result.inserted_id),
        "database": config["mongodb_database"],
        "collection": config["mongodb_collection"],
        "stored_at": record_with_metadata["stored_at"],
    }


def get_expense_record(record_id):
    config = load_config()

    client = MongoClient(config["mongodb_uri"])
    db = client[config["mongodb_database"]]
    collection = db[config["mongodb_collection"]]

    from bson.objectid import ObjectId

    record = collection.find_one({"_id": ObjectId(record_id)})

    if record:
        record["_id"] = str(record["_id"])
        return record
    else:
        return None


def search_expense_records(query):
    config = load_config()

    client = MongoClient(config["mongodb_uri"])
    db = client[config["mongodb_database"]]
    collection = db[config["mongodb_collection"]]

    results = list(collection.find(query).limit(100))

    for record in results:
        record["_id"] = str(record["_id"])

    return {
        "count": len(results),
        "results": results,
        "database": config["mongodb_database"],
        "collection": config["mongodb_collection"],
    }


def update_expense_record(record_id, updates):
    config = load_config()

    client = MongoClient(config["mongodb_uri"])
    db = client[config["mongodb_database"]]
    collection = db[config["mongodb_collection"]]

    from bson.objectid import ObjectId

    updates["updated_at"] = datetime.now().isoformat()

    result = collection.update_one({"_id": ObjectId(record_id)}, {"$set": updates})

    return {
        "success": result.modified_count > 0,
        "modified_count": result.modified_count,
        "record_id": record_id,
    }
