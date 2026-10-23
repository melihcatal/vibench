from __future__ import annotations

import os
from typing import Any

from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.container import ContainerProxy
from azure.cosmos.database import DatabaseProxy


COSMOS_ENDPOINT_ENV = "AZURE_COSMOS_ENDPOINT"
COSMOS_KEY_ENV = "AZURE_COSMOS_KEY"
COSMOS_DATABASE_ENV = "AZURE_COSMOS_DATABASE"
COSMOS_CONTAINER_ENV = "AZURE_COSMOS_CONTAINER"
COSMOS_PARTITION_PATH_ENV = "AZURE_COSMOS_PARTITION_KEY_PATH"


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def get_cosmos_client() -> CosmosClient:
    endpoint = _required_env(COSMOS_ENDPOINT_ENV)
    key = _required_env(COSMOS_KEY_ENV)
    return CosmosClient(url=endpoint, credential=key)


def get_database(client: CosmosClient | None = None) -> DatabaseProxy:
    cosmos_client = client or get_cosmos_client()
    database_name = _required_env(COSMOS_DATABASE_ENV)
    return cosmos_client.get_database_client(database_name)


def get_container(client: CosmosClient | None = None) -> ContainerProxy:
    database = get_database(client)
    container_name = _required_env(COSMOS_CONTAINER_ENV)
    return database.get_container_client(container_name)


def ensure_container(client: CosmosClient | None = None) -> ContainerProxy:
    cosmos_client = client or get_cosmos_client()
    database_name = _required_env(COSMOS_DATABASE_ENV)
    container_name = _required_env(COSMOS_CONTAINER_ENV)
    partition_path = os.getenv(COSMOS_PARTITION_PATH_ENV, "/partition_key")
    database = cosmos_client.create_database_if_not_exists(id=database_name)
    return database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path=partition_path),
    )


def extract_cosmos_headers(response_headers: dict[str, Any] | None) -> dict[str, Any]:
    headers = response_headers or {}
    return {
        "etag": headers.get("etag") or headers.get("ETag"),
        "request_charge": float(headers.get("x-ms-request-charge", 0.0) or 0.0),
        "activity_id": headers.get("x-ms-activity-id"),
    }
