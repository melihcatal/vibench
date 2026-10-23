from __future__ import annotations

import os
from typing import Any

from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.container import ContainerProxy
from azure.cosmos.exceptions import CosmosResourceNotFoundError


def get_cosmos_container() -> ContainerProxy:
    endpoint = os.environ["AZURE_COSMOS_ENDPOINT"]
    key = os.environ["AZURE_COSMOS_KEY"]
    database_name = os.environ["AZURE_COSMOS_DATABASE"]
    container_name = os.environ["AZURE_COSMOS_CONTAINER"]
    partition_key_path = os.getenv("AZURE_COSMOS_PARTITION_KEY", "/id")

    client = CosmosClient(url=endpoint, credential=key)
    database = client.create_database_if_not_exists(id=database_name)
    return database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path=partition_key_path),
    )


def get_partition_key_value(
    document_id: str, document: dict[str, Any] | None = None
) -> Any:
    partition_key_path = os.getenv("AZURE_COSMOS_PARTITION_KEY", "/id")
    key_name = partition_key_path.lstrip("/")
    if key_name == "id":
        return document_id
    if document and key_name in document:
        return document[key_name]
    raise KeyError(f"Missing partition key field: {key_name}")


def read_document(
    container: ContainerProxy, document_id: str, partition_key: Any | None = None
) -> dict[str, Any] | None:
    pk = (
        partition_key
        if partition_key is not None
        else get_partition_key_value(document_id)
    )
    try:
        return container.read_item(item=document_id, partition_key=pk)
    except CosmosResourceNotFoundError:
        return None
