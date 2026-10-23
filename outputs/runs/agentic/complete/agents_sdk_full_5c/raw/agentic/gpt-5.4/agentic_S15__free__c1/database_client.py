from __future__ import annotations

import os
from typing import Optional
from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.container import ContainerProxy
from azure.cosmos.database import DatabaseProxy


COSMOS_ENDPOINT_ENV = "AZURE_COSMOS_ENDPOINT"
COSMOS_KEY_ENV = "AZURE_COSMOS_KEY"
COSMOS_DATABASE_ENV = "AZURE_COSMOS_DATABASE"
COSMOS_CONTAINER_ENV = "AZURE_COSMOS_CONTAINER"
COSMOS_PARTITION_KEY_FIELD_ENV = "AZURE_COSMOS_PARTITION_KEY_FIELD"


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def get_cosmos_client() -> CosmosClient:
    endpoint = get_required_env(COSMOS_ENDPOINT_ENV)
    key = get_required_env(COSMOS_KEY_ENV)
    return CosmosClient(url=endpoint, credential=key)


def get_database(client: Optional[CosmosClient] = None) -> DatabaseProxy:
    cosmos_client = client or get_cosmos_client()
    database_name = get_required_env(COSMOS_DATABASE_ENV)
    return cosmos_client.get_database_client(database_name)


def get_container(client: Optional[CosmosClient] = None) -> ContainerProxy:
    database = get_database(client)
    container_name = get_required_env(COSMOS_CONTAINER_ENV)
    return database.get_container_client(container_name)


def get_partition_key_field() -> str:
    return os.getenv(COSMOS_PARTITION_KEY_FIELD_ENV, "partition_key")


def ensure_database_and_container() -> ContainerProxy:
    client = get_cosmos_client()
    database_name = get_required_env(COSMOS_DATABASE_ENV)
    container_name = get_required_env(COSMOS_CONTAINER_ENV)
    partition_key_field = get_partition_key_field()
    database = client.create_database_if_not_exists(id=database_name)
    database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path=f"/{partition_key_field}"),
    )
    return database.get_container_client(container_name)
