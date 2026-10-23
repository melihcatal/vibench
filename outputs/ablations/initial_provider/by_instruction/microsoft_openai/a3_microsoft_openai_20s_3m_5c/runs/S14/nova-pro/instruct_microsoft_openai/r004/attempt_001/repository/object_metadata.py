import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

def object_metadata(container_name, blob_name):
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_properties = blob_client.get_blob_properties()
    return blob_properties