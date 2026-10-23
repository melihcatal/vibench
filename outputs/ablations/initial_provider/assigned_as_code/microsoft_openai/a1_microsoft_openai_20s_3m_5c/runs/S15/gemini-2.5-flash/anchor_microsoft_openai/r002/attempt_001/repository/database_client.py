from azure.cosmos import CosmosClient
import os


def get_cosmos_client():
    cosmos_endpoint = os.environ.get("AZURE_COSMOS_ENDPOINT")
    cosmos_key = os.environ.get("AZURE_COSMOS_KEY")
    if not cosmos_endpoint or not cosmos_key:
        raise ValueError("AZURE_COSMOS_ENDPOINT and AZURE_COSMOS_KEY environment variables must be set.")
    return CosmosClient(cosmos_endpoint, credential=cosmos_key)


def get_container_client(database_name, container_name):
    client = get_cosmos_client()
    database_client = client.get_database_client(database_name)
    container_client = database_client.get_container_client(container_name)
    return container_client
