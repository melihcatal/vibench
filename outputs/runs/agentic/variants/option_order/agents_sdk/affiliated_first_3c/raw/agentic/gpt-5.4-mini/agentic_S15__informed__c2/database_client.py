import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from pymongo import MongoClient


@dataclass(frozen=True)
class DatabaseSettings:
    uri: str
    database_name: str
    collection_name: str


def load_settings() -> DatabaseSettings:
    return DatabaseSettings(
        uri=os.getenv("MONGODB_ATLAS_URI", "mongodb://localhost:27017"),
        database_name=os.getenv("MONGODB_ATLAS_DATABASE", "document_store"),
        collection_name=os.getenv("MONGODB_ATLAS_COLLECTION", "documents"),
    )


def get_client() -> MongoClient:
    settings = load_settings()
    return MongoClient(settings.uri)


def get_collection():
    settings = load_settings()
    client = get_client()
    return client[settings.database_name][settings.collection_name]


def normalize_document(document: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if document is None:
        return None
    normalized = dict(document)
    normalized.pop("_id", None)
    return normalized
