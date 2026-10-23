import os
from azure.cosmos import CosmosClient

def get_cosmos_client():
    return CosmosClient(os.environ['AZURE_COSMOS_ENDPOINT'], credential=os.environ['AZURE_COSMOS_KEY'])

def get_database_container(client, database_name, container_name):
    database = client.get_database_client(database_name)
    return database.get_container_client(container_name)