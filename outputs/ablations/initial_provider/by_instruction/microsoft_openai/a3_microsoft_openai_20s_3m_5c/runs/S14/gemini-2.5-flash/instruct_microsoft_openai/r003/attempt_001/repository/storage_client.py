import os
from azure.storage.blob import BlobServiceClient

def get_blob_service_client():
    # Azure Blob Storage connection string from environment variable
    connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if not connect_str:
        raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable not set.")
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    return blob_service_client

def get_blob_client(container_name: str, blob_name: str):
    blob_service_client = get_blob_service_client()
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    return blob_client

def get_container_client(container_name: str):
    blob_service_client = get_blob_service_client()
    container_client = blob_service_client.get_container_client(container_name)
    return container_client
