import os
from azure.cosmos import CosmosClient, Container

COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT", "https://your-cosmos-account.documents.azure.com:443/")
COSMOS_KEY = os.getenv("COSMOS_KEY", "your-cosmos-key")
DATABASE_NAME = os.getenv("COSMOS_DATABASE", "documentDB")
CONTAINER_NAME = os.getenv("COSMOS_CONTAINER", "documents")

_client = None

def get_cosmos_client() -> CosmosClient:
    """Initializes and returns a singleton CosmosClient."""
    global _client
    if _client is None:
        _client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
    return _client

def get_cosmos_container() -> Container:
    """Returns the configured Cosmos DB container."""
    client = get_cosmos_client()
    database = client.get_database_client(DATABASE_NAME)
    container = database.get_container_client(CONTAINER_NAME)
    return container