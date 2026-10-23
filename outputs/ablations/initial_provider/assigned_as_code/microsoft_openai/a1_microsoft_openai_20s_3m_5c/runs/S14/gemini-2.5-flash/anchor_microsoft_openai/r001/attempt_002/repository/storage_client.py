from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
import os

def get_blob_service_client(account_url=None):
    account_url = account_url or os.environ.get("AZURE_STORAGE_ACCOUNT_URL")
    if not account_url:
        raise ValueError("Azure Storage Account URL not provided and not found in environment variables.")
    
    # DefaultAzureCredential will attempt to authenticate using a chain of methods,
    # including environment variables, managed identity, Azure CLI, etc.
    credential = DefaultAzureCredential()
    return BlobServiceClient(account_url, credential=credential)
