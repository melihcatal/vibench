from __future__ import annotations

import os
from typing import Any, Dict

from pymongo import MongoClient


def store_expense_record(
    expense_record: Dict[str, Any],
    database_name: str = "expenses",
    collection_name: str = "records",
) -> Dict[str, Any]:
    client = MongoClient(os.getenv("MONGODB_ATLAS_URI"))
    collection = client[database_name][collection_name]
    document = dict(expense_record)
    document.setdefault("_id", document.get("id"))
    result = collection.replace_one({"_id": document["_id"]}, document, upsert=True)
    return {
        "provider": "mongodb-atlas",
        "id": document["_id"],
        "matched_count": result.matched_count,
        "modified_count": result.modified_count,
        "upserted_id": str(result.upserted_id)
        if result.upserted_id is not None
        else None,
    }
