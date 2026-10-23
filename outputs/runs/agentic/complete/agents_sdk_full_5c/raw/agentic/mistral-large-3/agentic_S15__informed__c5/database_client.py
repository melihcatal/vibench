import os
from azure.cosmos import CosmosClient

# Azure Cosmos DB configuration
COSMOS_ENDPOINT = os.getenv("AZURE_COSMOS_ENDPOINT")
COSMOS_KEY = os.getenv("AZURE_COSMOS_KEY")
DATABASE_NAME = os.getenv("AZURE_COSMOS_DATABASE", "document_db")
CONTAINER_NAME = os.getenv("AZURE_COSMOS_CONTAINER", "documents")

_client = None


def get_cosmos_client():
    """Initializes and returns a singleton CosmosClient."""
    global _client
    if _client is None:
        _client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
    return _client


def get_cosmos_container():
    """Returns the Cosmos DB container for document operations."""
    client = get_cosmos_client()
    database = client.get_database_client(DATABASE_NAME)
    container = database.get_container_client(CONTAINER_NAME)
    return container