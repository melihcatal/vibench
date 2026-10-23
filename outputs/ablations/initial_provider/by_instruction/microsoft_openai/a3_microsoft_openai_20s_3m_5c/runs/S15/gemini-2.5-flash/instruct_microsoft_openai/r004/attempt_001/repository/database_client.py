import os
from azure.cosmos import CosmosClient

class CosmosDBClient:
    def __init__(self):
        self.url = os.environ.get("AZURE_COSMOS_ENDPOINT")
        self.key = os.environ.get("AZURE_COSMOS_KEY")
        self.database_name = os.environ.get("AZURE_COSMOS_DATABASE_NAME")
        self.container_name = os.environ.get("AZURE_COSMOS_CONTAINER_NAME")

        if not all([self.url, self.key, self.database_name, self.container_name]):
            raise ValueError("Azure Cosmos DB environment variables not set. Please set AZURE_COSMOS_ENDPOINT, AZURE_COSMOS_KEY, AZURE_COSMOS_DATABASE_NAME, AZURE_COSMOS_CONTAINER_NAME.")

        self.client = CosmosClient(self.url, credential=self.key)
        self.database = self.client.get_database_client(self.database_name)
        self.container = self.database.get_container_client(self.container_name)
