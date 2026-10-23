import os
from azure.cosmos import CosmosClient

# Load configuration from environment variables
COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT", "https://<your-account>.documents.azure.com:443/")
COSMOS_KEY = os.getenv("COSMOS_KEY", "<your-key>")

# Initialize Cosmos DB client
client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)

def get_cosmos_container(database_name: str, container_name: str):
    """
    Helper function to get a Cosmos DB container.
    
    Args:
        database_name: Name of the Cosmos DB database.
        container_name: Name of the Cosmos DB container.
        
    Returns:
        The Cosmos DB container object.
    """
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)
    return container