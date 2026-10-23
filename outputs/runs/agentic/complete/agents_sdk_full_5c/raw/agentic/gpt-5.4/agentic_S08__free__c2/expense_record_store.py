from __future__ import annotations

import os
from typing import Any, Dict

from pymongo import MongoClient


MONGODB_URI_ENV = "MONGODB_ATLAS_URI"
DEFAULT_DB = "expenses"
DEFAULT_COLLECTION = "records"
ATLAS_HOST_HINT = "mongodb.net"


def expense_record_store(normalized_expense: Dict[str, Any], db_name: str = DEFAULT_DB, collection_name: str = DEFAULT_COLLECTION) -> Dict[str, Any]:
    client = MongoClient(os.environ.get(MONGODB_URI_ENV), appname="structured-document-extraction")
    collection = client[db_name][collection_name]
    result = collection.insert_one(normalized_expense)
    return {
        "provider": "MongoDB Atlas",
        "uri_env": MONGODB_URI_ENV,
        "host_hint": ATLAS_HOST_HINT,
        "database": db_name,
        "collection": collection_name,
        "inserted_id": str(result.inserted_id),
    }
