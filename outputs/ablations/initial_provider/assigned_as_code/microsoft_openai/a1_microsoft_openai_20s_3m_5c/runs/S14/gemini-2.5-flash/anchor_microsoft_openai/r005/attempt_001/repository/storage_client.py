from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
import os

def get_blob_service_client(account_url: str):
    """
    Returns a BlobServiceClient using DefaultAzureCredential.
    """
    credential = DefaultAzureCredential()
    return BlobServiceClient(account_url, credential=credential)

def get_container_client(account_url: str, container_name: str):
    """
    Returns a ContainerClient for a specific container.
    """
    blob_service_client = get_blob_service_client(account_url)
    return blob_service_client.get_container_client(container_name)
