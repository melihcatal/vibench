import os
from azure.cosmos import CosmosClient, exceptions

class NoSQLClient:
    """Thin wrapper over Azure Cosmos DB NoSQL SDK."""
    def __init__(self):
        endpoint = os.getenv('COSMOS_ENDPOINT')
        key = os.getenv('COSMOS_KEY')
        self.client = CosmosClient(endpoint, key)
    
    def get_container(self, database_name, container_name):
        try:
            db = self.client.get_database_client(database_name)
            container = db.get_container_client(container_name)
            return container
        except exceptions.CosmosResourceNotFoundError:
            raise ValueError(f"Database or container not found: {database_name}/{container_name}")
