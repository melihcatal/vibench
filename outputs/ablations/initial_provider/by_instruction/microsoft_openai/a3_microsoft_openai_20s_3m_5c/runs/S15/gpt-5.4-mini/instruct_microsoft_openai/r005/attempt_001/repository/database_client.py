import os

from azure.cosmos import CosmosClient


def get_cosmos_client():
    endpoint = os.environ["AZURE_COSMOS_ENDPOINT"]
    key = os.environ["AZURE_COSMOS_KEY"]
    return CosmosClient(endpoint, credential=key)


def get_database_name():
    return os.getenv("AZURE_COSMOS_DATABASE", "documents")


def get_container_name():
    return os.getenv("AZURE_COSMOS_CONTAINER", "records")


def get_container():
    client = get_cosmos_client()
    database = client.get_database_client(get_database_name())
    return database.get_container_client(get_container_name())
