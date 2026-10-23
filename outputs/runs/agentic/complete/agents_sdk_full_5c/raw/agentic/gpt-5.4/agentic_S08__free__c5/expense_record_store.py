from __future__ import annotations

import os
from typing import Any, Dict, Optional

from pymongo import MongoClient



def store_expense_record(record: Dict[str, Any], collection_name: str = "expenses") -> Dict[str, Any]:
    mongo_uri = os.environ["MONGODB_ATLAS_URI"]
    database_name = os.getenv("MONGODB_ATLAS_DATABASE", "finance")
    client = MongoClient(mongo_uri, appname="structured-document-extraction")
    collection = client[database_name][collection_name]
    result = collection.insert_one(record)
    return {
        "provider": "mongodb-atlas",
        "database": database_name,
        "collection": collection_name,
        "inserted_id": str(result.inserted_id),
    }
