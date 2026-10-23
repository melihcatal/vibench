from typing import Dict, Any, Optional
import os
from azure.cosmos import CosmosClient, PartitionKey, exceptions


class DatabaseClient:
    """Client helper for Azure Cosmos DB NoSQL document store."""

    def __init__(self):
        self.endpoint = os.getenv(
            "AZURE_COSMOS_ENDPOINT", "https://<your-account>.documents.azure.com:443/"
        )
        self.key = os.getenv("AZURE_COSMOS_KEY", "<your-key>")
        self.database_name = os.getenv("AZURE_COSMOS_DATABASE", "document_db")
        self.container_name = os.getenv("AZURE_COSMOS_CONTAINER", "documents")
        self.client = CosmosClient(self.endpoint, credential=self.key)
        self.database = self.client.get_database_client(self.database_name)
        self.container = self.database.get_container_client(self.container_name)

    def get_container(self):
        return self.container
