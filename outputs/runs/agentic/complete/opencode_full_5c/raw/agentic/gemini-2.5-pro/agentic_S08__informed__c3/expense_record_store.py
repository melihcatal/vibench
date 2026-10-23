import os
from pymongo import MongoClient
from typing import Dict, Any


def store_expense_record(normalized_record: Dict[str, Any]):
    connection_string = os.getenv("MONGODB_ATLAS_URI")
    if not connection_string:
        raise ValueError("MONGODB_ATLAS_URI environment variable not set.")

    client = MongoClient(connection_string)

    db_name = os.getenv("MONGO_DB_NAME", "expenses")
    collection_name = os.getenv("MONGO_COLLECTION_NAME", "records")

    db = client[db_name]
    collection = db[collection_name]

    # Convert dataclass to dict if necessary
    from dataclasses import is_dataclass, asdict

    if is_dataclass(normalized_record):
        record_to_insert = asdict(normalized_record)
    else:
        record_to_insert = normalized_record

    result = collection.insert_one(record_to_insert)
    return result.inserted_id
