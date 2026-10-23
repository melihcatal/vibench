from typing import Any, Dict, Optional
import os
from azure.cosmos import CosmosClient, PartitionKey, exceptions


class DatabaseClient:
    """Azure Cosmos DB client helper with configuration loading."""

    def __init__(self):
        self.endpoint = os.getenv("AZURE_COSMOS_ENDPOINT")
        self.key = os.getenv("AZURE_COSMOS_KEY")
        self.database_name = os.getenv("AZURE_COSMOS_DATABASE", "document_db")
        self.container_name = os.getenv("AZURE_COSMOS_CONTAINER", "documents")
        self.client = CosmosClient(self.endpoint, self.key)
        self.database = self.client.get_database_client(self.database_name)
        self.container = self.database.get_container_client(self.container_name)

    def get_container(self):
        return self.container
