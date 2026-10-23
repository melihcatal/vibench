from __future__ import annotations

import os
from typing import Any, Dict, Optional

from pymongo import MongoClient


def store_expense_record(
    record: Dict[str, Any],
    collection_name: str = "expenses",
    database_name: Optional[str] = None,
) -> Dict[str, Any]:
    client = MongoClient(os.environ["MONGODB_ATLAS_URI"])
    db = client[database_name or os.getenv("MONGODB_ATLAS_DATABASE", "finance")]
    collection = db[collection_name]
    result = collection.insert_one(record)
    return {
        "provider": "mongodb-atlas",
        "database": db.name,
        "collection": collection.name,
        "inserted_id": str(result.inserted_id),
    }
