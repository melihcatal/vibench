import os
from azure.cosmos import CosmosClient

COSMOS_DB_ENDPOINT = os.environ.get("COSMOS_DB_ENDPOINT")
COSMOS_DB_KEY = os.environ.get("COSMOS_DB_KEY")
DATABASE_NAME = os.environ.get("COSMOS_DB_DATABASE_NAME", "documentdb")
CONTAINER_NAME = os.environ.get("COSMOS_DB_CONTAINER_NAME", "documents")

def get_cosmos_client():
    if not COSMOS_DB_ENDPOINT or not COSMOS_DB_KEY:
        raise ValueError("COSMOS_DB_ENDPOINT and COSMOS_DB_KEY must be set in environment variables")
    client = CosmosClient(COSMOS_DB_ENDPOINT, credential=COSMOS_DB_KEY)
    database = client.get_database_client(DATABASE_NAME)
    container = database.get_container_client(CONTAINER_NAME)
    return container
