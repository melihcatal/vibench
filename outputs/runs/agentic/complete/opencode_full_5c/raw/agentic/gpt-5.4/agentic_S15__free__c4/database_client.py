from __future__ import annotations

import os
from typing import Optional

from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient


def get_cosmos_client() -> CosmosClient:
    endpoint = os.environ["AZURE_COSMOS_ENDPOINT"]
    key = os.environ["AZURE_COSMOS_KEY"]
    return CosmosClient(url=endpoint, credential=key)


def get_container_client():
    database_name = os.environ["AZURE_COSMOS_DATABASE"]
    container_name = os.environ["AZURE_COSMOS_CONTAINER"]
    client = get_cosmos_client()
    database = client.get_database_client(database_name)
    return database.get_container_client(container_name)


def get_blob_service_client() -> BlobServiceClient:
    connection_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
    return BlobServiceClient.from_connection_string(connection_string)


def get_blob_container_client(container_name: Optional[str] = None):
    target_container = container_name or os.environ["AZURE_STORAGE_CONTAINER"]
    return get_blob_service_client().get_container_client(target_container)
