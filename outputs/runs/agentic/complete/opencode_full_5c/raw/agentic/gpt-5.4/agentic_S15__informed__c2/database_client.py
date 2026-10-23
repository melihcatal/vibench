from __future__ import annotations

import os
from typing import Any

from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.database import DatabaseProxy
from azure.cosmos.container import ContainerProxy


def get_cosmos_settings() -> dict[str, str]:
    endpoint = os.environ["AZURE_COSMOS_ENDPOINT"]
    key = os.environ["AZURE_COSMOS_KEY"]
    database_name = os.environ.get("AZURE_COSMOS_DATABASE", "app-documents")
    container_name = os.environ.get("AZURE_COSMOS_CONTAINER", "records")
    partition_key_path = os.environ.get("AZURE_COSMOS_PARTITION_KEY", "/pk")
    return {
        "endpoint": endpoint,
        "key": key,
        "database_name": database_name,
        "container_name": container_name,
        "partition_key_path": partition_key_path,
    }


def get_cosmos_client() -> CosmosClient:
    settings = get_cosmos_settings()
    return CosmosClient(url=settings["endpoint"], credential=settings["key"])


def get_database(client: CosmosClient | None = None) -> DatabaseProxy:
    active_client = client or get_cosmos_client()
    settings = get_cosmos_settings()
    return active_client.create_database_if_not_exists(id=settings["database_name"])


def get_container(client: CosmosClient | None = None) -> ContainerProxy:
    settings = get_cosmos_settings()
    database = get_database(client)
    return database.create_container_if_not_exists(
        id=settings["container_name"],
        partition_key=PartitionKey(path=settings["partition_key_path"]),
    )


def ensure_partition_key(
    document: dict[str, Any], partition_key: str | None
) -> dict[str, Any]:
    if partition_key is not None:
        document["pk"] = partition_key
    elif "pk" not in document:
        document["pk"] = document["id"]
    return document


def sanitize_query_value(value: Any) -> Any:
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise TypeError("query field value must be scalar")
