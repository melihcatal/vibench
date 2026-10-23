from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
import os

def get_blob_service_client():
    # In a real application, account_url and container_name would likely come from environment variables or a configuration file.
    # For this example, we'll use environment variables.
    account_url = os.environ.get("AZURE_STORAGE_ACCOUNT_URL")
    if not account_url:
        raise ValueError("AZURE_STORAGE_ACCOUNT_URL environment variable not set.")

    credential = DefaultAzureCredential()
    return BlobServiceClient(account_url, credential=credential)

def get_account_key():
    account_key = os.environ.get("AZURE_STORAGE_ACCOUNT_KEY")
    if not account_key:
        raise ValueError("AZURE_STORAGE_ACCOUNT_KEY environment variable not set.")
    return account_key

def get_container_name():
    container_name = os.environ.get("AZURE_STORAGE_CONTAINER_NAME")
    if not container_name:
        raise ValueError("AZURE_STORAGE_CONTAINER_NAME environment variable not set.")
    return container_name
