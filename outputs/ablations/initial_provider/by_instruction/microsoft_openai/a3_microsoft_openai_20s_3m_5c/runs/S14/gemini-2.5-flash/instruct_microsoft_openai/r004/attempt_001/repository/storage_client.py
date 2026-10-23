import os
from azure.storage.blob import BlobServiceClient

def get_blob_service_client():
    """
    Initializes and returns an Azure BlobServiceClient using a connection string
    from environment variables.
    """
    connection_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
    if not connection_string:
        raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable not set.")
    return BlobServiceClient.from_connection_string(connection_string)
