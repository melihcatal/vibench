import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

def get_storage_client():
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    return blob_service_client