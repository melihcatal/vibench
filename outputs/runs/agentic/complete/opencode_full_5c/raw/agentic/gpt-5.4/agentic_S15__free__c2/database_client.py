from __future__ import annotations

import os
from typing import Optional

from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.container import ContainerProxy
from azure.cosmos.database import DatabaseProxy


COSMOS_ENDPOINT_ENV = "AZURE_COSMOSDB_ENDPOINT"
COSMOS_KEY_ENV = "AZURE_COSMOSDB_KEY"
COSMOS_DATABASE_ENV = "AZURE_COSMOSDB_DATABASE"
COSMOS_CONTAINER_ENV = "AZURE_COSMOSDB_CONTAINER"
COSMOS_PARTITION_KEY_ENV = "AZURE_COSMOSDB_PARTITION_KEY"


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def get_cosmos_client() -> CosmosClient:
    endpoint = _require_env(COSMOS_ENDPOINT_ENV)
    key = _require_env(COSMOS_KEY_ENV)
    return CosmosClient(url=endpoint, credential=key)


def get_database(client: Optional[CosmosClient] = None) -> DatabaseProxy:
    active_client = client or get_cosmos_client()
    database_name = _require_env(COSMOS_DATABASE_ENV)
    return active_client.get_database_client(database_name)


def get_container(client: Optional[CosmosClient] = None) -> ContainerProxy:
    database = get_database(client=client)
    container_name = _require_env(COSMOS_CONTAINER_ENV)
    return database.get_container_client(container_name)


def create_container_if_missing(
    client: Optional[CosmosClient] = None,
) -> ContainerProxy:
    active_client = client or get_cosmos_client()
    database_name = _require_env(COSMOS_DATABASE_ENV)
    container_name = _require_env(COSMOS_CONTAINER_ENV)
    partition_path = os.getenv(COSMOS_PARTITION_KEY_ENV, "/id")
    database = active_client.create_database_if_not_exists(id=database_name)
    return database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path=partition_path),
    )


def resolve_partition_key(
    document: dict, explicit_partition_key: Optional[str] = None
) -> str:
    if explicit_partition_key is not None:
        return str(explicit_partition_key)
    partition_path = os.getenv(COSMOS_PARTITION_KEY_ENV, "/id")
    key_name = partition_path.lstrip("/")
    value = document.get(key_name) or document.get("id")
    if value is None:
        raise ValueError(f"Unable to resolve partition key from path {partition_path}")
    return str(value)
