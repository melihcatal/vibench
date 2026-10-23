import os
from functools import lru_cache

from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


@lru_cache(maxsize=1)
def get_cosmos_client() -> CosmosClient:
    endpoint = get_required_env("AZURE_COSMOS_ENDPOINT")
    key = get_required_env("AZURE_COSMOS_KEY")
    return CosmosClient(url=endpoint, credential=key)


def get_cosmos_container():
    client = get_cosmos_client()
    database_name = get_required_env("AZURE_COSMOS_DATABASE")
    container_name = get_required_env("AZURE_COSMOS_CONTAINER")
    database = client.get_database_client(database_name)
    return database.get_container_client(container_name)


@lru_cache(maxsize=1)
def get_blob_service_client() -> BlobServiceClient:
    connection_string = get_required_env("AZURE_STORAGE_CONNECTION_STRING")
    return BlobServiceClient.from_connection_string(connection_string)


def get_blob_container_client():
    service = get_blob_service_client()
    container_name = get_required_env("AZURE_STORAGE_CONTAINER")
    return service.get_container_client(container_name)
