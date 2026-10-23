import os
from azure.cosmos import CosmosClient, exceptions, PartitionKey

def get_client():
    """Initialize and return a Cosmos DB client using environment variables.
    
    Expected environment variables:
        AZURE_COSMOS_ENDPOINT
        AZURE_COSMOS_KEY
    """
    endpoint = os.getenv("AZURE_COSMOS_ENDPOINT")
    key = os.getenv("AZURE_COSMOS_KEY")
    if not endpoint or not key:
        raise RuntimeError("Cosmos endpoint and key must be set in environment variables")
    client = CosmosClient(endpoint, credential=key)
    # Assuming a database named 'my_database' and container 'my_container'
    database = client.get_database_client("my_database")
    container = database.get_container_client("my_container")
    return container
