import os
from azure.cosmos import CosmosClient, PartitionKey

class DatabaseClient:
    def __init__(self):
        self.url = os.getenv('COSMOS_DB_URL')
        self.key = os.getenv('COSMOS_DB_KEY')
        self.client = CosmosClient(self.url, self.key)
        self.database_name = os.getenv('COSMOS_DB_NAME')
        self.container_name = os.getenv('COSMOS_DB_CONTAINER')
        self.database = self.client.get_database_client(self.database_name)
        self.container = self.database.get_container_client(self.container_name)

    def get_container(self):
        return self.container