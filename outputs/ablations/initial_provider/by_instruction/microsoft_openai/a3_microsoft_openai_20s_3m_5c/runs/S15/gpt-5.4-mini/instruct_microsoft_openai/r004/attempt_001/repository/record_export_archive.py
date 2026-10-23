import os

from azure.storage.blob import BlobServiceClient


def record_export_archive(payload: bytes, blob_name: str) -> str:
    client = BlobServiceClient.from_connection_string(os.getenv("AZURE_STORAGE_CONNECTION_STRING", ""))
    container = client.get_container_client(os.getenv("AZURE_STORAGE_CONTAINER", "archives"))
    container.upload_blob(name=blob_name, data=payload, overwrite=True)
    return blob_name
