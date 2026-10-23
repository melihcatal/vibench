import os
from azure.storage.blob import BlobServiceClient


def get_blob_service_client():
    connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if not connect_str:
        raise ValueError(
            "AZURE_STORAGE_CONNECTION_STRING environment variable not set."
        )
    return BlobServiceClient.from_connection_string(connect_str)
