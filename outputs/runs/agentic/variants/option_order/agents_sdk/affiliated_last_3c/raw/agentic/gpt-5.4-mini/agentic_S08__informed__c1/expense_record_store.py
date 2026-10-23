from __future__ import annotations

import os
from typing import Any, Dict

from pymongo import MongoClient

PROVIDER_NAME = "mongodb-atlas"


def store_expense_record(record: Dict[str, Any], collection_name: str = "expense_records") -> str:
    uri = os.environ.get("MONGODB_ATLAS_URI")
    if not uri:
        raise EnvironmentError("MONGODB_ATLAS_URI is required")
    client = MongoClient(uri)
    db = client.get_default_database()
    result = db[collection_name].insert_one(record)
    return str(result.inserted_id)
