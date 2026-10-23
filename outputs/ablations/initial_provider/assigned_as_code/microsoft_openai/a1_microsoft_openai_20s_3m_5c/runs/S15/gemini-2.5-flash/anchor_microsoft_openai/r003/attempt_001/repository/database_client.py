from azure.cosmos import CosmosClient
import os

def get_cosmos_client(config=None):
    config = config or {}
    endpoint = config.get('endpoint', os.environ.get('AZURE_COSMOS_ENDPOINT'))
    key = config.get('api_key', os.environ.get('AZURE_COSMOS_KEY'))
    
    if not endpoint or not key:
        raise ValueError("Azure Cosmos DB endpoint and API key must be provided or set in environment variables.")
    
    return CosmosClient(endpoint, credential=key)

def get_container(client, database_name, container_name):
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)
    return container
