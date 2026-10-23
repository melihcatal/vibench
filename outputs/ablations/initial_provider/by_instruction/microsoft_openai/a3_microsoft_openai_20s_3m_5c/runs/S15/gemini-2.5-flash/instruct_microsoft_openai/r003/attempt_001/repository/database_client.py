import os
from azure.cosmos import CosmosClient

COSMOS_DB_ENDPOINT = os.environ.get("COSMOS_DB_ENDPOINT")
COSMOS_DB_KEY = os.environ.get("COSMOS_DB_KEY")
COSMOS_DB_DATABASE_NAME = os.environ.get("COSMOS_DB_DATABASE_NAME", "documentdb")
COSMOS_DB_CONTAINER_NAME = os.environ.get("COSMOS_DB_CONTAINER_NAME", "items")

class CosmosDBClient:
    def __init__(self):
        if not COSMOS_DB_ENDPOINT or not COSMOS_DB_KEY:
            raise ValueError("COSMOS_DB_ENDPOINT and COSMOS_DB_KEY environment variables must be set.")
        self.client = CosmosClient(COSMOS_DB_ENDPOINT, credential=COSMOS_DB_KEY)
        self.database = self.client.get_database_client(COSMOS_DB_DATABASE_NAME)
        self.container = self.database.get_container_client(COSMOS_DB_CONTAINER_NAME)

    def get_container(self):
        return self.container
