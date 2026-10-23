import os
from azure.storage.blob import BlobServiceClient

def get_blob_service_client():
    connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    return BlobServiceClient.from_connection_string(connection_string)