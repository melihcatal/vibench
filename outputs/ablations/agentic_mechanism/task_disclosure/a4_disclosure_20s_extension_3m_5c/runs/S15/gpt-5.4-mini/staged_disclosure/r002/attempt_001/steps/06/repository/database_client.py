import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional


try:
    from pymongo import MongoClient
    from pymongo.collection import Collection
    from pymongo.database import Database
except ImportError as exc:
    raise ImportError("pymongo is required for MongoDB Atlas integration") from exc


@dataclass(frozen=True)
class DatabaseConfig:
    uri: str
    database_name: str
    collection_name: str


def load_config() -> DatabaseConfig:
    uri = os.environ.get("MONGODB_URI") or os.environ.get("MONGODB_ATLAS_URI")
    if not uri:
        raise ValueError("Missing MONGODB_URI or MONGODB_ATLAS_URI")

    database_name = os.environ.get("MONGODB_DATABASE", "app")
    collection_name = os.environ.get("MONGODB_COLLECTION", "documents")
    return DatabaseConfig(uri=uri, database_name=database_name, collection_name=collection_name)


@lru_cache(maxsize=1)
def get_client() -> MongoClient:
    config = load_config()
    return MongoClient(config.uri)


def get_database() -> Database:
    config = load_config()
    return get_client()[config.database_name]


def get_collection() -> Collection:
    config = load_config()
    return get_database()[config.collection_name]


def ping() -> bool:
    client = get_client()
    client.admin.command("ping")
    return True


def insert_document(document: Dict[str, Any]) -> Any:
    return get_collection().insert_one(document)


def find_one(filter_query: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    return get_collection().find_one(filter_query or {})


def update_one(filter_query: Dict[str, Any], update: Dict[str, Any], upsert: bool = False) -> Any:
    return get_collection().update_one(filter_query, update, upsert=upsert)


def delete_one(filter_query: Dict[str, Any]) -> Any:
    return get_collection().delete_one(filter_query)
