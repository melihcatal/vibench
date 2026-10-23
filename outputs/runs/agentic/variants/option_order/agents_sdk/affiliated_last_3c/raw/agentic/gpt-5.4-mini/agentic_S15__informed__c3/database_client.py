import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database


@dataclass(frozen=True)
class DatabaseSettings:
    uri: str
    database_name: str
    collection_name: str


@lru_cache(maxsize=1)
def get_settings() -> DatabaseSettings:
    uri = os.environ.get("MONGODB_ATLAS_URI", "mongodb://localhost:27017")
    database_name = os.environ.get("MONGODB_ATLAS_DATABASE", "document_store")
    collection_name = os.environ.get("MONGODB_ATLAS_COLLECTION", "records")
    return DatabaseSettings(uri=uri, database_name=database_name, collection_name=collection_name)


@lru_cache(maxsize=1)
def get_client() -> MongoClient:
    return MongoClient(get_settings().uri)


def get_database() -> Database:
    settings = get_settings()
    return get_client()[settings.database_name]


def get_collection() -> Collection:
    settings = get_settings()
    return get_database()[settings.collection_name]


def document_id_field() -> str:
    return os.environ.get("MONGODB_ATLAS_ID_FIELD", "_id")


def normalize_identifier(document: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(document)
    if "id" in normalized and document_id_field() != "id":
        normalized[document_id_field()] = normalized.pop("id")
    return normalized


def projection_for_fields(fields: Optional[list[str]] = None) -> Optional[Dict[str, int]]:
    if not fields:
        return None
    projection = {field: 1 for field in fields}
    projection[document_id_field()] = 1
    return projection
