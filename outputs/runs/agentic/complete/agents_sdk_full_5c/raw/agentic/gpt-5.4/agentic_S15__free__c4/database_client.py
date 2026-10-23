from __future__ import annotations

import os
from typing import Optional

from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.container import ContainerProxy


COSMOS_URL_ENV = "AZURE_COSMOSDB_URL"
COSMOS_KEY_ENV = "AZURE_COSMOSDB_KEY"
COSMOS_DATABASE_ENV = "AZURE_COSMOSDB_DATABASE"
COSMOS_CONTAINER_ENV = "AZURE_COSMOSDB_CONTAINER"
COSMOS_PARTITION_KEY_ENV = "AZURE_COSMOSDB_PARTITION_KEY"


class CosmosDocumentStore:
    def __init__(
        self,
        url: Optional[str] = None,
        key: Optional[str] = None,
        database_name: Optional[str] = None,
        container_name: Optional[str] = None,
        partition_key_path: Optional[str] = None,
    ) -> None:
        self.url = url or os.environ[COSMOS_URL_ENV]
        self.key = key or os.environ[COSMOS_KEY_ENV]
        self.database_name = database_name or os.environ.get(COSMOS_DATABASE_ENV, "documents-db")
        self.container_name = container_name or os.environ.get(COSMOS_CONTAINER_ENV, "documents")
        self.partition_key_path = partition_key_path or os.environ.get(COSMOS_PARTITION_KEY_ENV, "/partitionKey")
        self.client = CosmosClient(self.url, credential=self.key)
        self.database = self.client.create_database_if_not_exists(id=self.database_name)
        self.container = self.database.create_container_if_not_exists(
            id=self.container_name,
            partition_key=PartitionKey(path=self.partition_key_path),
            offer_throughput=400,
        )

    def get_container(self) -> ContainerProxy:
        return self.container



def default_partition_key(document_id: str) -> str:
    return document_id



def resolve_partition_key(value: Optional[str], document_id: str) -> str:
    return value if value is not None else default_partition_key(document_id)
