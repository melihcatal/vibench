from __future__ import annotations

import os
from typing import Any, Dict

from pymongo import MongoClient


DEFAULT_DB = "expenses"
DEFAULT_COLLECTION = "records"


def store_expense_record(record: Dict[str, Any], database: str = DEFAULT_DB, collection: str = DEFAULT_COLLECTION) -> str:
    client = MongoClient(os.environ["MONGODB_ATLAS_URI"])
    coll = client[database][collection]
    payload = dict(record)
    payload.setdefault("provider", "mongodb-atlas")
    result = coll.insert_one(payload)
    return str(result.inserted_id)
