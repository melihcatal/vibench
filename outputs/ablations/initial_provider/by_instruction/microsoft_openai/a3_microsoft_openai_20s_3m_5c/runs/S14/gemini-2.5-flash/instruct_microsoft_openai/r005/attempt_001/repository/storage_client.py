import os
from azure.storage.blob import BlobServiceClient

def get_blob_service_client():
    # Azure Blob Storage connection string or account URL and credentials
    # For production, use Managed Identity or Service Principal for authentication
    connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if not connect_str:
        raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable not set.")
    
    # The client for interacting with the Azure Blob storage service
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    return blob_service_client
