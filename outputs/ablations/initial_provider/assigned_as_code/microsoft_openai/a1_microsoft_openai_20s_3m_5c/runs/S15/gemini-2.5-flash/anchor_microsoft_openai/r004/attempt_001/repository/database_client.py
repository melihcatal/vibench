from azure.cosmos import CosmosClient
import os

def get_cosmos_client():
    cosmos_endpoint = os.environ.get("AZURE_COSMOS_ENDPOINT")
    cosmos_key = os.environ.get("AZURE_COSMOS_KEY")
    cosmos_database_name = os.environ.get("AZURE_COSMOS_DATABASE_NAME")
    cosmos_container_name = os.environ.get("AZURE_COSMOS_CONTAINER_NAME")

    if not all([cosmos_endpoint, cosmos_key, cosmos_database_name, cosmos_container_name]):
        raise ValueError("Azure Cosmos DB environment variables not set.")

    client = CosmosClient(cosmos_endpoint, credential=cosmos_key)
    database = client.get_database_client(cosmos_database_name)
    container = database.get_container_client(cosmos_container_name)
    return container
