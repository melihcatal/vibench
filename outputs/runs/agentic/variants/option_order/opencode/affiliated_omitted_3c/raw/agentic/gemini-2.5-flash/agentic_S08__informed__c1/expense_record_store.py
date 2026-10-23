import os
from pymongo import MongoClient
from document_models import NormalizedExpense


def persist_expense_record(record: NormalizedExpense) -> dict:
    mongodb_atlas_uri = os.environ["MONGODB_ATLAS_URI"]
    client = MongoClient(mongodb_atlas_uri)

    db = client.expense_db
    collection = db.records

    # Convert dataclass to dictionary for MongoDB insertion
    record_dict = record.__dict__
    # Convert LineItem dataclasses to dictionaries if present
    if "line_items" in record_dict and record_dict["line_items"]:
        record_dict["line_items"] = [
            item.__dict__ for item in record_dict["line_items"]
        ]

    result = collection.insert_one(record_dict)

    return {"_id": str(result.inserted_id), "status": "success"}
