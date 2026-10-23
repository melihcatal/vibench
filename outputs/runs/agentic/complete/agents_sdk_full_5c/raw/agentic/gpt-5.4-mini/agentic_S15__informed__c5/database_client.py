from __future__ import annotations

import os
from functools import lru_cache
from typing import Any, Dict, Optional

from azure.cosmos import CosmosClient, DatabaseProxy, ContainerProxy


DEFAULT_DATABASE_NAME = os.getenv("COSMOS_DATABASE_NAME", "documents")
DEFAULT_CONTAINER_NAME = os.getenv("COSMOS_CONTAINER_NAME", "records")


@lru_cache(maxsize=1)
def get_cosmos_client() -> CosmosClient:
    endpoint = os.environ["AZURE_COSMOS_ENDPOINT"]
    key = os.environ["AZURE_COSMOS_KEY"]
    return CosmosClient(endpoint, credential=key)


@lru_cache(maxsize=1)
def get_database_client(database_name: str = DEFAULT_DATABASE_NAME) -> DatabaseProxy:
    return get_cosmos_client().get_database_client(database_name)


@lru_cache(maxsize=1)
def get_container_client(
    database_name: str = DEFAULT_DATABASE_NAME,
    container_name: str = DEFAULT_CONTAINER_NAME,
) -> ContainerProxy:
    return get_database_client(database_name).get_container_client(container_name)


def build_document_id(payload: Dict[str, Any]) -> str:
    for key in ("id", "document_id", "record_id", "primary_id"):
        value = payload.get(key)
        if value not in (None, ""):
            return str(value)
    raise ValueError("payload must include an identifier field")


def partition_key_from_payload(payload: Dict[str, Any]) -> Optional[str]:
    value = payload.get("partition_key") or payload.get("tenant_id") or payload.get("category")
    return None if value in (None, "") else str(value)
