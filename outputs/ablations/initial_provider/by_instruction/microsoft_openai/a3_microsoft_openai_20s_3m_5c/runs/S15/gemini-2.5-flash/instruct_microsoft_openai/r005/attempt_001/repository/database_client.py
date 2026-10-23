import os
from azure.cosmos import CosmosClient

def get_cosmos_client():
    cosmos_db_endpoint = os.environ.get("COSMOS_DB_ENDPOINT")
    cosmos_db_key = os.environ.get("COSMOS_DB_KEY")
    if not cosmos_db_endpoint or not cosmos_db_key:
        raise ValueError("COSMOS_DB_ENDPOINT and COSMOS_DB_KEY environment variables must be set.")
    return CosmosClient(cosmos_db_endpoint, cosmos_db_key)

def get_database_and_container(database_name, container_name):
    client = get_cosmos_client()
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)
    return container
