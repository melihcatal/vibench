import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


COSMOS_ENDPOINT_ENV = "AZURE_COSMOS_ENDPOINT"
COSMOS_KEY_ENV = "AZURE_COSMOS_KEY"
COSMOS_DATABASE_ENV = "AZURE_COSMOS_DATABASE"
COSMOS_CONTAINER_ENV = "AZURE_COSMOS_CONTAINER"
COSMOS_API_VERSION = "2018-12-31"


@dataclass(frozen=True)
class DatabaseConfig:
    endpoint: str
    key: str
    database: str
    container: str


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise ValueError(f"{name} is required")
    return value


def load_config() -> DatabaseConfig:
    return DatabaseConfig(
        endpoint=_require_env(COSMOS_ENDPOINT_ENV).rstrip("/"),
        key=_require_env(COSMOS_KEY_ENV),
        database=_require_env(COSMOS_DATABASE_ENV),
        container=_require_env(COSMOS_CONTAINER_ENV),
    )


def get_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"x-ms-version": COSMOS_API_VERSION})
    return session


def build_document_url(config: Optional[DatabaseConfig] = None, document_id: Optional[str] = None) -> str:
    config = config or load_config()
    base = f"{config.endpoint}/dbs/{config.database}/colls/{config.container}/docs"
    if document_id is None:
        return base
    return f"{base}/{document_id}"


def build_headers(config: Optional[DatabaseConfig] = None) -> Dict[str, str]:
    config = config or load_config()
    return {
        "Authorization": config.key,
        "x-ms-date": requests.utils.formatdate(usegmt=True),
        "x-ms-version": COSMOS_API_VERSION,
        "Content-Type": "application/json",
    }


def get_client(config: Optional[DatabaseConfig] = None) -> Dict[str, Any]:
    config = config or load_config()
    return {
        "config": config,
        "session": get_session(),
        "base_url": build_document_url(config),
        "headers": build_headers(config),
    }
