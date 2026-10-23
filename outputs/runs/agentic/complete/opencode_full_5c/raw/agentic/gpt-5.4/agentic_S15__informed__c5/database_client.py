from __future__ import annotations

import os
from typing import Any

from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.container import ContainerProxy
from azure.cosmos.exceptions import CosmosResourceNotFoundError


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"missing environment variable: {name}")
    return value


def get_cosmos_client() -> CosmosClient:
    endpoint = _require_env("AZURE_COSMOS_ENDPOINT")
    key = _require_env("AZURE_COSMOS_KEY")
    return CosmosClient(url=endpoint, credential=key)


def get_container() -> ContainerProxy:
    database_name = _require_env("AZURE_COSMOS_DATABASE")
    container_name = _require_env("AZURE_COSMOS_CONTAINER")
    client = get_cosmos_client()
    database = client.create_database_if_not_exists(id=database_name)
    return database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path="/partitionKey"),
    )


def read_item_or_none(document_id: str, partition_key: str) -> dict[str, Any] | None:
    container = get_container()
    try:
        return container.read_item(item=document_id, partition_key=partition_key)
    except CosmosResourceNotFoundError:
        return None
