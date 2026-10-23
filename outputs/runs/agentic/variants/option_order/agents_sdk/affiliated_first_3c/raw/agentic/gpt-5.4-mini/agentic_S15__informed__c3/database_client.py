"""Managed NoSQL Document Store client utilities for Azure Cosmos DB."""
from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional

from azure.cosmos import CosmosClient, PartitionKey

DEFAULT_DATABASE_NAME = os.getenv("AZURE_COSMOS_DATABASE", "documents_db")
DEFAULT_CONTAINER_NAME = os.getenv("AZURE_COSMOS_CONTAINER", "documents")
DEFAULT_ENDPOINT = os.getenv("AZURE_COSMOS_ENDPOINT", "")
DEFAULT_KEY = os.getenv("AZURE_COSMOS_KEY", "")
DEFAULT_PARTITION_KEY = os.getenv("AZURE_COSMOS_PARTITION_KEY", "/tenant_id")


@dataclass(frozen=True)
class CosmosConfig:
    endpoint: str
    key: str
    database_name: str = DEFAULT_DATABASE_NAME
    container_name: str = DEFAULT_CONTAINER_NAME
    partition_key_path: str = DEFAULT_PARTITION_KEY


def load_cosmos_config(overrides: Optional[Dict[str, str]] = None) -> CosmosConfig:
    overrides = overrides or {}
    return CosmosConfig(
        endpoint=overrides.get("endpoint", os.getenv("AZURE_COSMOS_ENDPOINT", DEFAULT_ENDPOINT)),
        key=overrides.get("key", os.getenv("AZURE_COSMOS_KEY", DEFAULT_KEY)),
        database_name=overrides.get("database_name", os.getenv("AZURE_COSMOS_DATABASE", DEFAULT_DATABASE_NAME)),
        container_name=overrides.get("container_name", os.getenv("AZURE_COSMOS_CONTAINER", DEFAULT_CONTAINER_NAME)),
        partition_key_path=overrides.get("partition_key_path", os.getenv("AZURE_COSMOS_PARTITION_KEY", DEFAULT_PARTITION_KEY)),
    )


@lru_cache(maxsize=1)
def get_cosmos_client(endpoint: Optional[str] = None, key: Optional[str] = None) -> CosmosClient:
    cfg = load_cosmos_config({"endpoint": endpoint or "", "key": key or ""})
    if not cfg.endpoint or not cfg.key:
        raise ValueError("AZURE_COSMOS_ENDPOINT and AZURE_COSMOS_KEY are required")
    return CosmosClient(cfg.endpoint, credential=cfg.key)


def get_container(config: Optional[CosmosConfig] = None):
    cfg = config or load_cosmos_config()
    client = get_cosmos_client(cfg.endpoint, cfg.key)
    database = client.get_database_client(cfg.database_name)
    try:
        container = database.get_container_client(cfg.container_name)
        container.read()  # ensure exists
    except Exception:
        database.create_container_if_not_exists(
            id=cfg.container_name,
            partition_key=PartitionKey(path=cfg.partition_key_path),
        )
        container = database.get_container_client(cfg.container_name)
    return container
