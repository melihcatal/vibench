# database_client.py
# [HELPER] Azure Cosmos DB configuration and client utilities

import os
from azure.cosmos import CosmosClient

COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT")
COSMOS_KEY = os.getenv("COSMOS_KEY")

if not COSMOS_ENDPOINT or not COSMOS_KEY:
    raise RuntimeError("Cosmos DB credentials not configured in environment variables")

def get_cosmos_db_client() -> CosmosClient:
    """Initialize and return an Azure Cosmos DB client."""
    return CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
