from __future__ import annotations

import os
from typing import Optional

from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.container import ContainerProxy
from azure.cosmos.database import DatabaseProxy


DEFAULT_DATABASE_ENV = "AZURE_COSMOS_DATABASE"
DEFAULT_CONTAINER_ENV = "AZURE_COSMOS_CONTAINER"


def get_cosmos_client() -> CosmosClient:
    endpoint = os.environ["AZURE_COSMOS_ENDPOINT"]
    key = os.environ["AZURE_COSMOS_KEY"]
    return CosmosClient(url=endpoint, credential=key)


def get_database_name() -> str:
    return os.environ.get(DEFAULT_DATABASE_ENV, "app-documents")


def get_container_name() -> str:
    return os.environ.get(DEFAULT_CONTAINER_ENV, "records")


def get_database(client: Optional[CosmosClient] = None) -> DatabaseProxy:
    cosmos_client = client or get_cosmos_client()
    return cosmos_client.get_database_client(get_database_name())


def get_container(client: Optional[CosmosClient] = None) -> ContainerProxy:
    database = get_database(client)
    return database.get_container_client(get_container_name())


def ensure_container(client: Optional[CosmosClient] = None) -> ContainerProxy:
    cosmos_client = client or get_cosmos_client()
    database = cosmos_client.create_database_if_not_exists(id=get_database_name())
    database.create_container_if_not_exists(
        id=get_container_name(),
        partition_key=PartitionKey(path="/partitionKey"),
    )
    return database.get_container_client(get_container_name())
