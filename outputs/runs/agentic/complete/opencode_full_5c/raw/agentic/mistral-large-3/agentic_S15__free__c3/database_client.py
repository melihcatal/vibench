import os
from typing import Any, Dict, Optional
from azure.cosmos import CosmosClient, ContainerProxy, DatabaseProxy
from azure.cosmos.exceptions import CosmosHttpResponseError


class DatabaseClient:
    """Client helper for Azure Cosmos DB NoSQL document store."""

    def __init__(self) -> None:
        self.endpoint = os.getenv("AZURE_COSMOS_ENDPOINT", "")
        self.key = os.getenv("AZURE_COSMOS_KEY", "")
        self.database_name = os.getenv("AZURE_COSMOS_DATABASE", "")
        self.container_name = os.getenv("AZURE_COSMOS_CONTAINER", "")
        self.client: CosmosClient = CosmosClient(self.endpoint, self.key)
        self.database: DatabaseProxy = self.client.get_database_client(
            self.database_name
        )
        self.container: ContainerProxy = self.database.get_container_client(
            self.container_name
        )

    def get_container(self) -> ContainerProxy:
        """Returns the Cosmos DB container client."""
        return self.container
