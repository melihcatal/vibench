from __future__ import annotations

import os
from typing import Any, Dict

from pymongo import MongoClient



def expense_record_store(record: Dict[str, Any], database_name: str = "expenses", collection_name: str = "records") -> Dict[str, Any]:
    atlas_uri = os.getenv("MONGODB_ATLAS_URI")
    if not atlas_uri:
        raise ValueError("MONGODB_ATLAS_URI is required")
    client = MongoClient(atlas_uri)
    collection = client[database_name][collection_name]
    document = dict(record)
    document.setdefault("_id", document.get("record_id"))
    result = collection.replace_one({"_id": document["_id"]}, document, upsert=True)
    return {
        "provider": "MongoDB Atlas",
        "database": database_name,
        "collection": collection_name,
        "record_id": document["_id"],
        "matched_count": result.matched_count,
        "modified_count": result.modified_count,
        "upserted_id": str(result.upserted_id) if result.upserted_id is not None else None,
    }
