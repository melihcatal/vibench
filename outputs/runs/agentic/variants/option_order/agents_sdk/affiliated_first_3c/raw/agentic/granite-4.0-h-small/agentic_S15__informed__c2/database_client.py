import os
from azure.cosmos import CosmosClient, exceptions

def get_cosmos_client():
    """Initialize and return an Azure Cosmos DB client using environment variables."""
    endpoint = os.getenv("AZURE_COSMOS_ENDPOINT")
    key = os.getenv("AZURE_COSMOS_KEY")
    if not endpoint or not key:
        raise RuntimeError("AZURE_COSMOS_ENDPOINT and AZURE_COSMOS_KEY must be set")
    client = CosmosClient(endpoint, key, connection_policy=None)
    return client

# Example of using the client (can be called from other modules)
# client = get_cosmos_client()
# database = client.get_database_client('mydb')
# container = database.get_container_client('mycontainer')
