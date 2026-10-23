from __future__ import annotations

from typing import Mapping

from pymongo import MongoClient


MONGODB_ATLAS_URI = "MONGODB_ATLAS_URI"


def persist_login_audit(record: Mapping[str, object], db_name: str = "identity", collection_name: str = "login_audit") -> str:
    client = MongoClient()
    coll = client[db_name][collection_name]
    result = coll.insert_one(dict(record))
    return str(result.inserted_id)
