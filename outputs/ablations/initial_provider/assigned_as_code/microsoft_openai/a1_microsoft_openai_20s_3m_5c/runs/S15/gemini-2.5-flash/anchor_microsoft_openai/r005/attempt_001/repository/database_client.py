from azure.cosmos import CosmosClient
import os

def get_cosmos_client():
    endpoint = os.environ.get("AZURE_COSMOS_ENDPOINT")
    key = os.environ.get("AZURE_COSMOS_KEY")
    if not endpoint or not key:
        raise ValueError("AZURE_COSMOS_ENDPOINT and AZURE_COSMOS_KEY environment variables must be set.")
    return CosmosClient(endpoint, credential=key)

def get_container_client(database_name, container_name):
    client = get_cosmos_client()
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)
    return container
