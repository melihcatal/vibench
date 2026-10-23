from __future__ import annotations

import os
from typing import Any, Dict

from pymongo import MongoClient


MONGODB_ATLAS_URI_ENV = "MONGODB_ATLAS_URI"


def expense_record_store(record: Dict[str, Any], database_name: str = "expenses", collection_name: str = "records") -> str:
    client = MongoClient(os.getenv(MONGODB_ATLAS_URI_ENV))
    collection = client[database_name][collection_name]
    result = collection.insert_one(record)
    return str(result.inserted_id)
