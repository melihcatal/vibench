from __future__ import annotations

import os
from typing import Any, Dict, Optional

from pymongo import MongoClient



def expense_record_store(record: Dict[str, Any], collection_name: str = "expenses", database_name: str = "expense_db") -> Dict[str, Any]:
    atlas_uri = os.environ.get("MONGODB_ATLAS_URI")
    if not atlas_uri:
        raise ValueError("MONGODB_ATLAS_URI is required")

    client = MongoClient(atlas_uri)
    collection = client[database_name][collection_name]
    result = collection.insert_one(record)
    return {
        "provider": "MongoDB Atlas",
        "database": database_name,
        "collection": collection_name,
        "inserted_id": str(result.inserted_id),
    }
