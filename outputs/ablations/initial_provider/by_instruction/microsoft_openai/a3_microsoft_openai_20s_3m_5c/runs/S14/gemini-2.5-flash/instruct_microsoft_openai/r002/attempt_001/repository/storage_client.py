import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

class StorageClient:
    _blob_service_client: BlobServiceClient = None

    def __init__(self):
        load_dotenv()
        if not StorageClient._blob_service_client:
            connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
            if not connection_string:
                raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable not set.")
            StorageClient._blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    def get_blob_service_client(self) -> BlobServiceClient:
        return StorageClient._blob_service_client
