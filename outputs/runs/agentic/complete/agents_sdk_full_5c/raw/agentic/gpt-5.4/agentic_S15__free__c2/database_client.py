from __future__ import annotations

import os
from typing import Optional

from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.container import ContainerProxy
from azure.cosmos.exceptions import CosmosResourceNotFoundError


COSMOS_ENDPOINT_ENV = "AZURE_COSMOS_ENDPOINT"
COSMOS_KEY_ENV = "AZURE_COSMOS_KEY"
COSMOS_DATABASE_ENV = "AZURE_COSMOS_DATABASE"
COSMOS_CONTAINER_ENV = "AZURE_COSMOS_CONTAINER"


def get_cosmos_client() -> CosmosClient:
    endpoint = os.environ[COSMOS_ENDPOINT_ENV]
    key = os.environ[COSMOS_KEY_ENV]
    return CosmosClient(url=endpoint, credential=key)


def get_database_name() -> str:
    return os.getenv(COSMOS_DATABASE_ENV, "app-documents")


def get_container_name() -> str:
    return os.getenv(COSMOS_CONTAINER_ENV, "records")


def get_container(create_if_missing: bool = False) -> ContainerProxy:
    client = get_cosmos_client()
    database_name = get_database_name()
    container_name = get_container_name()
    database = client.create_database_if_not_exists(id=database_name) if create_if_missing else client.get_database_client(database_name)
    if create_if_missing:
        return database.create_container_if_not_exists(
            id=container_name,
            partition_key=PartitionKey(path="/partitionKey"),
            offer_throughput=400,
        )
    return database.get_container_client(container_name)


def get_item_if_exists(document_id: str, partition_key: str) -> Optional[dict]:
    container = get_container(create_if_missing=False)
    try:
        return container.read_item(item=document_id, partition_key=partition_key)
    except CosmosResourceNotFoundError:
        return None
