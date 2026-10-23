from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
import os

def get_blob_service_client(account_url=None):
    account_url = account_url or os.environ.get("AZURE_STORAGE_ACCOUNT_URL")
    if not account_url:
        raise ValueError("Azure Storage Account URL not provided and not found in environment variables.")
    credential = DefaultAzureCredential()
    return BlobServiceClient(account_url, credential=credential)

def get_container_client(container_name, account_url=None):
    client = get_blob_service_client(account_url)
    return client.get_container_client(container_name)

def get_blob_client(container_name, blob_name, account_url=None):
    client = get_blob_service_client(account_url)
    return client.get_blob_client(container=container_name, blob=blob_name)
