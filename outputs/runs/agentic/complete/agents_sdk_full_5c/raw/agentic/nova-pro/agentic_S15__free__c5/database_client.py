import os
from azure.cosmos import CosmosClient

class DatabaseClient:
    def __init__(self):
        self.client = CosmosClient(os.environ['COSMOS_URI'], os.environ['COSMOS_KEY'])
        self.database = self.client.get_database_client('myDatabase')
        self.container = self.database.get_container_client('myContainer')
