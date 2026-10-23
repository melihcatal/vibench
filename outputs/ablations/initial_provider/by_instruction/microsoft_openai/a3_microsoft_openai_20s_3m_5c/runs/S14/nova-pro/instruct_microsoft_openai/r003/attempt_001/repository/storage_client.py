import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

class StorageClient:
    def __init__(self):
        self.connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)

    def get_container_client(self, container_name):
        return self.blob_service_client.get_container_client(container_name)

    def get_blob_client(self, container_name, blob_name):
        return self.blob_service_client.get_blob_client(container_name, blob_name)