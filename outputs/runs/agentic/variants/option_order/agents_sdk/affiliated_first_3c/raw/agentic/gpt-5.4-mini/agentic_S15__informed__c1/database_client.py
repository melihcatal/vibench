import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

DEFAULT_URI_ENV = "MONGODB_ATLAS_URI"
DEFAULT_DB_ENV = "MONGODB_ATLAS_DB"
DEFAULT_COLLECTION_ENV = "MONGODB_ATLAS_COLLECTION"


@dataclass(frozen=True)
class NoSQLConfig:
    uri: str
    database: str
    collection: str


def load_config() -> NoSQLConfig:
    uri = os.environ.get(DEFAULT_URI_ENV)
    if not uri:
        raise RuntimeError(f"Missing required environment variable: {DEFAULT_URI_ENV}")
    database = os.environ.get(DEFAULT_DB_ENV, "documents")
    collection = os.environ.get(DEFAULT_COLLECTION_ENV, "records")
    return NoSQLConfig(uri=uri, database=database, collection=collection)


def get_client(uri: Optional[str] = None) -> MongoClient:
    return MongoClient(uri or load_config().uri)


def get_collection(config: Optional[NoSQLConfig] = None) -> Collection:
    cfg = config or load_config()
    client = MongoClient(cfg.uri)
    db: Database = client[cfg.database]
    return db[cfg.collection]


def ensure_primary_key(document: Dict[str, Any], key: str = "id") -> Dict[str, Any]:
    if key not in document or document[key] in (None, ""):
        raise ValueError(f"Document must contain non-empty primary key field '{key}'")
    return document
