import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

def presigned_download(container_name, blob_name):
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    sas_token = blob_client.get_blob_url(expiry=3600)
    return sas_token