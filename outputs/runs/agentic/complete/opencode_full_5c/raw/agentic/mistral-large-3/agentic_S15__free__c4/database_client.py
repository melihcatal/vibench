from typing import Any, Dict, Optional
import os
from azure.cosmos import CosmosClient, PartitionKey, exceptions


class DatabaseClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseClient, cls).__new__(cls)
            cls._instance._initialize_client()
        return cls._instance

    def _initialize_client(self):
        self.endpoint = os.getenv("AZURE_COSMOS_ENDPOINT")
        self.key = os.getenv("AZURE_COSMOS_KEY")
        self.database_name = os.getenv("AZURE_COSMOS_DATABASE", "document_db")
        self.container_name = os.getenv("AZURE_COSMOS_CONTAINER", "documents")

        self.client = CosmosClient(self.endpoint, self.key)
        self.database = self.client.create_database_if_not_exists(id=self.database_name)
        self.container = self.database.create_container_if_not_exists(
            id=self.container_name, partition_key=PartitionKey(path="/partitionKey")
        )

    def get_container(self):
        return self.container
