from __future__ import annotations

import os
from typing import Dict, Iterable, List, Mapping

from pymongo import MongoClient


MONGODB_URI_ENV = "MONGODB_ATLAS_URI"
MONGODB_DB_ENV = "MONGODB_ATLAS_DB"
MONGODB_COLLECTION_ENV = "MONGODB_ATLAS_COLLECTION"


def _collection():
    client = MongoClient(os.environ[MONGODB_URI_ENV], appname="federated-login-audit")
    database = client[os.environ.get(MONGODB_DB_ENV, "identity")]
    return database[os.environ.get(MONGODB_COLLECTION_ENV, "login_audit")]


def store_audit_records(records: Iterable[Mapping]) -> Dict[str, object]:
    docs: List[Mapping] = list(records)
    if not docs:
        return {"provider": "mongodb_atlas", "inserted_count": 0, "inserted_ids": []}
    result = _collection().insert_many(list(docs), ordered=False)
    return {
        "provider": "mongodb_atlas",
        "inserted_count": len(result.inserted_ids),
        "inserted_ids": [str(item) for item in result.inserted_ids],
    }
