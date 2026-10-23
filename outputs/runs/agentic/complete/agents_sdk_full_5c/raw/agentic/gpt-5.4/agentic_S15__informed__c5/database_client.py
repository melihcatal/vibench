from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.container import ContainerProxy
from azure.cosmos.database import DatabaseProxy


COSMOS_ENDPOINT_ENV = "AZURE_COSMOS_ENDPOINT"
COSMOS_KEY_ENV = "AZURE_COSMOS_KEY"
COSMOS_DATABASE_ENV = "AZURE_COSMOS_DATABASE"
COSMOS_CONTAINER_ENV = "AZURE_COSMOS_CONTAINER"
COSMOS_PARTITION_KEY_ENV = "AZURE_COSMOS_PARTITION_KEY"


class CosmosConfigurationError(RuntimeError):
    pass



def _required_env(name: str, default: Optional[str] = None) -> str:
    value = os.getenv(name, default)
    if not value:
        raise CosmosConfigurationError(f"Missing required environment variable: {name}")
    return value


@lru_cache(maxsize=1)
def get_cosmos_client() -> CosmosClient:
    endpoint = _required_env(COSMOS_ENDPOINT_ENV)
    key = _required_env(COSMOS_KEY_ENV)
    return CosmosClient(url=endpoint, credential=key)


@lru_cache(maxsize=1)
def get_database() -> DatabaseProxy:
    client = get_cosmos_client()
    database_name = _required_env(COSMOS_DATABASE_ENV, "appdb")
    return client.create_database_if_not_exists(id=database_name)


@lru_cache(maxsize=1)
def get_container() -> ContainerProxy:
    database = get_database()
    container_name = _required_env(COSMOS_CONTAINER_ENV, "documents")
    partition_path = _required_env(COSMOS_PARTITION_KEY_ENV, "/partitionKey")
    return database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path=partition_path),
        offer_throughput=400,
    )



def resolve_partition_key(document_id: str, provided: Optional[str] = None) -> str:
    return provided or document_id
