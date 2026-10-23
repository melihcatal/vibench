import os
from azure.storage.blob import BlobServiceClient

class AzureStorageClient:
    def __init__(self):
        self.connection_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
        if not self.connection_string:
            raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable not set.")
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)

    def get_blob_client(self, container_name: str, blob_name: str):
        container_client = self.blob_service_client.get_container_client(container_name)
        return container_client.get_blob_client(blob_name)

    def get_container_client(self, container_name: str):
        return self.blob_service_client.get_container_client(container_name)
