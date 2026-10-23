from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.container import ContainerProxy
from azure.cosmos.database import DatabaseProxy
from azure.cosmos.exceptions import CosmosResourceNotFoundError


COSMOS_ENDPOINT_ENV = "AZURE_COSMOSDB_ENDPOINT"
COSMOS_KEY_ENV = "AZURE_COSMOSDB_KEY"
COSMOS_DATABASE_ENV = "AZURE_COSMOSDB_DATABASE"
COSMOS_CONTAINER_ENV = "AZURE_COSMOSDB_CONTAINER"


@lru_cache(maxsize=1)
def get_cosmos_client() -> CosmosClient:
    endpoint = os.environ[COSMOS_ENDPOINT_ENV]
    key = os.environ[COSMOS_KEY_ENV]
    return CosmosClient(url=endpoint, credential=key)


@lru_cache(maxsize=1)
def get_database() -> DatabaseProxy:
    client = get_cosmos_client()
    database_name = os.environ.get(COSMOS_DATABASE_ENV, "app-documents")
    return client.create_database_if_not_exists(id=database_name)


@lru_cache(maxsize=1)
def get_container() -> ContainerProxy:
    database = get_database()
    container_name = os.environ.get(COSMOS_CONTAINER_ENV, "documents")
    return database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path="/partitionKey"),
        offer_throughput=400,
    )


def ensure_document_exists(document_id: str, partition_key: str):
    container = get_container()
    try:
        return container.read_item(item=document_id, partition_key=partition_key)
    except CosmosResourceNotFoundError:
        return None


def optional_partition_key(value: Optional[str]) -> Optional[str]:
    return value if value not in (None, "") else None
