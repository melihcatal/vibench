from __future__ import annotations

import os
from typing import Any, Dict

from pymongo import MongoClient


mongo_client = MongoClient(os.environ["MONGODB_URI"])
collection = mongo_client[os.environ.get("MONGODB_DB", "identity_audit")][os.environ.get("MONGODB_COLLECTION", "login_audit")]


def store_login_audit(record: Dict[str, Any]) -> str:
    inserted = collection.insert_one(record)
    return str(inserted.inserted_id)
