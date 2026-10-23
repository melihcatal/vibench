from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

class StorageClient:
    def __init__(self, connection_string):
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    def get_container_client(self, container_name):
        return self.blob_service_client.get_container_client(container_name)

    def get_blob_client(self, container_name, blob_name):
        return self.blob_service_client.get_blob_client(container_name, blob_name)