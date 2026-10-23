import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


class DatabaseClientError(RuntimeError):
    pass


@dataclass(frozen=True)
class DatabaseConfig:
    base_url: str
    api_key: str
    app_id: str
    database: str
    collection: str
    cluster: str = "Cluster0"


def _get_env(*names: str) -> Optional[str]:
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return None


def load_config() -> DatabaseConfig:
    base_url = _get_env("MONGODB_DATA_API_BASE_URL", "MONGODB_ATLAS_DATA_API_URL")
    api_key = _get_env("MONGODB_DATA_API_KEY", "MONGODB_ATLAS_DATA_API_KEY")
    app_id = _get_env("MONGODB_ATLAS_APP_ID", "MONGODB_DATA_API_APP_ID")
    database = _get_env("MONGODB_DATA_API_DATABASE", "MONGODB_ATLAS_DATABASE")
    collection = _get_env("MONGODB_DATA_API_COLLECTION", "MONGODB_ATLAS_COLLECTION")
    cluster = _get_env("MONGODB_DATA_API_CLUSTER", "MONGODB_ATLAS_CLUSTER") or "Cluster0"
    if not base_url or not api_key or not app_id or not database or not collection:
        raise DatabaseClientError("Missing MongoDB Atlas Data API configuration")
    return DatabaseConfig(
        base_url=base_url.rstrip("/"),
        api_key=api_key,
        app_id=app_id,
        database=database,
        collection=collection,
        cluster=cluster,
    )


def create_headers(config: Optional[DatabaseConfig] = None) -> Dict[str, str]:
    cfg = config or load_config()
    return {"Content-Type": "application/json", "Accept": "application/json", "api-key": cfg.api_key}


def collection_endpoint(config: Optional[DatabaseConfig] = None) -> str:
    cfg = config or load_config()
    return f"{cfg.base_url}/app/{cfg.app_id}/endpoint/data/v1/action"


def build_document_body(document: Dict[str, Any], primary_key_field: str = "_id") -> Dict[str, Any]:
    if primary_key_field not in document:
        raise DatabaseClientError(f"Missing primary key field: {primary_key_field}")
    return {
        "dataSource": load_config().cluster,
        "database": load_config().database,
        "collection": load_config().collection,
        "filter": {primary_key_field: document[primary_key_field]},
        "update": {"$set": document},
        "upsert": True,
    }


def request_session(config: Optional[DatabaseConfig] = None) -> requests.Session:
    cfg = config or load_config()
    session = requests.Session()
    session.headers.update(create_headers(cfg))
    return session


__all__ = ["DatabaseClientError", "DatabaseConfig", "load_config", "create_headers", "collection_endpoint", "build_document_body", "request_session"]
