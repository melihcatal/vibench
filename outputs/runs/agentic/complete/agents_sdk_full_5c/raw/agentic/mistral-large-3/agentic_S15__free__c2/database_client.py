import os
from azure.cosmos import CosmosClient, Container

def get_cosmos_client() -> CosmosClient:
    """
    Initializes and returns an Azure Cosmos DB client.
    """
    endpoint = os.getenv("COSMOS_ENDPOINT", "https://<your-account>.documents.azure.com:443/")
    key = os.getenv("COSMOS_KEY", "<your-key>")
    return CosmosClient(endpoint, key)

def get_cosmos_container() -> Container:
    """
    Returns the Azure Cosmos DB container for document operations.
    """
    client = get_cosmos_client()
    database_name = os.getenv("COSMOS_DATABASE", "documentDB")
    container_name = os.getenv("COSMOS_CONTAINER", "documents")
    database = client.get_database_client(database_name)
    return database.get_container_client(container_name)