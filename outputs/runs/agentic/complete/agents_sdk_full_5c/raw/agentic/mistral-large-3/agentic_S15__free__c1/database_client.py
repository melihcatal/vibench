import os
from azure.cosmos import CosmosClient

# Azure Cosmos DB configuration
COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT", "https://your-account.documents.azure.com:443/")
COSMOS_KEY = os.getenv("COSMOS_KEY", "your-primary-key")

# Initialize Cosmos DB client
client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)

def get_cosmos_container(database_name: str, container_name: str):
    """
    Helper to get a Cosmos DB container reference.
    """
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)
    return container