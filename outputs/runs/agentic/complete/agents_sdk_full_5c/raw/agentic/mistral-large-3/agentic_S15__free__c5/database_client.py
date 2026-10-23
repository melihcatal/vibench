import os
from azure.cosmos import CosmosClient

def get_cosmos_container():
    """
    Provides a configured Azure Cosmos DB container client.
    """
    endpoint = os.getenv("COSMOS_ENDPOINT", "https://<your-account>.documents.azure.com:443/")
    key = os.getenv("COSMOS_KEY", "<your-key>")
    database_name = os.getenv("COSMOS_DATABASE", "documents-db")
    container_name = os.getenv("COSMOS_CONTAINER", "documents")
    
    client = CosmosClient(endpoint, key)
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)
    return container