from __future__ import annotations

import os
from typing import Tuple

from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.database import DatabaseProxy
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


def get_database(client: CosmosClient) -> DatabaseProxy:
    return client.get_database_client(get_database_name())


def get_container(client: CosmosClient) -> ContainerProxy:
    database = get_database(client)
    return database.get_container_client(get_container_name())


def ensure_container() -> Tuple[DatabaseProxy, ContainerProxy]:
    client = get_cosmos_client()
    database = client.create_database_if_not_exists(id=get_database_name())
    container = database.create_container_if_not_exists(
        id=get_container_name(),
        partition_key=PartitionKey(path="/partition_key"),
        offer_throughput=400,
    )
    return database, container


def document_exists(container: ContainerProxy, document_id: str, partition_key: str) -> bool:
    try:
        container.read_item(item=document_id, partition_key=partition_key)
        return True
    except CosmosResourceNotFoundError:
        return False
