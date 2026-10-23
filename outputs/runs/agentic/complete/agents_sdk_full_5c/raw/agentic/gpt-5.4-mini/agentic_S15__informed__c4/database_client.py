import os
from functools import lru_cache
from typing import Any, Dict, Optional

from pymongo import MongoClient

DEFAULT_DB_NAME = os.getenv("MONGODB_ATLAS_DB_NAME", "document_store")
DEFAULT_COLLECTION_NAME = os.getenv("MONGODB_ATLAS_COLLECTION_NAME", "records")


@lru_cache(maxsize=1)
def get_mongo_client() -> MongoClient:
    uri = os.getenv("MONGODB_ATLAS_URI")
    if not uri:
        raise EnvironmentError("MONGODB_ATLAS_URI is required for MongoDB Atlas access")
    return MongoClient(uri)


@lru_cache(maxsize=128)
def get_collection(db_name: Optional[str] = None, collection_name: Optional[str] = None):
    client = get_mongo_client()
    db = client[db_name or DEFAULT_DB_NAME]
    return db[collection_name or DEFAULT_COLLECTION_NAME]


def build_document_id(payload: Dict[str, Any]) -> str:
    for key in ("id", "_id", "document_id", "record_id"):
        value = payload.get(key)
        if value is not None:
            return str(value)
    raise ValueError("payload must include one of: id, _id, document_id, record_id")


def load_context(db_name: Optional[str] = None, collection_name: Optional[str] = None) -> Dict[str, str]:
    return {
        "db_name": db_name or DEFAULT_DB_NAME,
        "collection_name": collection_name or DEFAULT_COLLECTION_NAME,
        "provider": "MongoDB Atlas",
    }
