import os
from functools import lru_cache
from typing import Any, Dict

from pymongo import MongoClient


def get_mongodb_uri() -> str:
    uri = os.getenv("MONGODB_ATLAS_URI")
    if not uri:
        raise RuntimeError("MONGODB_ATLAS_URI is required")
    return uri


def get_mongodb_database_name() -> str:
    return os.getenv("MONGODB_DATABASE", "appdb")


def get_mongodb_collection_name() -> str:
    return os.getenv("MONGODB_COLLECTION", "documents")


@lru_cache(maxsize=1)
def get_client() -> MongoClient:
    return MongoClient(get_mongodb_uri())


def get_collection():
    client = get_client()
    return client[get_mongodb_database_name()][get_mongodb_collection_name()]


def to_bson_safe(document: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in document.items() if not str(k).startswith("$")}
