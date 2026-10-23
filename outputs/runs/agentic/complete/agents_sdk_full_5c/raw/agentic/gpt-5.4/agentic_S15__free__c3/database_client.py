from __future__ import annotations

import os
from typing import Optional

from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.exceptions import CosmosResourceExistsError


COSMOS_ENDPOINT_ENV = "AZURE_COSMOSDB_ENDPOINT"
COSMOS_KEY_ENV = "AZURE_COSMOSDB_KEY"
COSMOS_DATABASE_ENV = "AZURE_COSMOSDB_DATABASE"
COSMOS_CONTAINER_ENV = "AZURE_COSMOSDB_CONTAINER"


_default_client: Optional[CosmosClient] = None


def get_cosmos_client() -> CosmosClient:
    global _default_client
    if _default_client is None:
        endpoint = os.environ[COSMOS_ENDPOINT_ENV]
        key = os.environ[COSMOS_KEY_ENV]
        _default_client = CosmosClient(url=endpoint, credential=key)
    return _default_client


def get_database_name() -> str:
    return os.getenv(COSMOS_DATABASE_ENV, "app-documents")


def get_container_name() -> str:
    return os.getenv(COSMOS_CONTAINER_ENV, "records")


def get_container_client():
    client = get_cosmos_client()
    return client.get_database_client(get_database_name()).get_container_client(get_container_name())


def ensure_container(partition_key_path: str = "/partitionKey"):
    client = get_cosmos_client()
    db = client.create_database_if_not_exists(id=get_database_name())
    try:
        return db.create_container(
            id=get_container_name(),
            partition_key=PartitionKey(path=partition_key_path),
            offer_throughput=400,
        )
    except CosmosResourceExistsError:
        return db.get_container_client(get_container_name())
