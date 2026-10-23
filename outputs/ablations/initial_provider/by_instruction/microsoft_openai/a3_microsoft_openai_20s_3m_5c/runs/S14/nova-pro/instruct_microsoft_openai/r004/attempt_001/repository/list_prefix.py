import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

def list_prefix(container_name, prefix=''):
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_client = blob_service_client.get_container_client(container_name)
    blob_list = container_client.list_blobs(name_starts_with=prefix)
    return [blob.name for blob in blob_list]