from azure.cosmos import CosmosClient
import os
from typing import Optional, Dict, Any


class DatabaseClient:
    """
    Client helper for Azure Cosmos DB for NoSQL.
    """

    def __init__(self, database_name: str, container_name: str):
        self.endpoint = os.getenv("AZURE_COSMOS_ENDPOINT")
        self.key = os.getenv("AZURE_COSMOS_KEY")
        self.database_name = database_name
        self.container_name = container_name
        self.client = None
        self.container = None

    def connect(self):
        """Establish connection to Cosmos DB."""
        if not self.endpoint or not self.key:
            raise ValueError("AZURE_COSMOS_ENDPOINT and AZURE_COSMOS_KEY must be set")

        self.client = CosmosClient(self.endpoint, self.key)
        database = self.client.get_database_client(self.database_name)
        self.container = database.get_container_client(self.container_name)

    def get_container(self):
        """Get the container client."""
        if not self.container:
            self.connect()
        return self.container


def load_config() -> Dict[str, Any]:
    """
    Loads configuration for Azure Cosmos DB.

    Returns:
        Dictionary containing configuration
    """
    return {
        "endpoint": os.getenv("AZURE_COSMOS_ENDPOINT"),
        "key": os.getenv("AZURE_COSMOS_KEY"),
        "database": os.getenv("AZURE_COSMOS_DATABASE", "default_db"),
        "container": os.getenv("AZURE_COSMOS_CONTAINER", "default_container"),
    }
