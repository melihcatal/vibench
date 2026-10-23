import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from typing import Union

def archive_record_snapshot(record_id: str, content: Union[str, bytes], file_name: str, content_type: str = "application/json") -> str:
    azure_storage_connection_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
    azure_storage_container_name = os.environ.get("AZURE_STORAGE_CONTAINER_NAME")

    if not all([azure_storage_connection_string, azure_storage_container_name]):
        raise ValueError("Azure Storage environment variables not set. Please set AZURE_STORAGE_CONNECTION_STRING, AZURE_STORAGE_CONTAINER_NAME.")

    blob_service_client = BlobServiceClient.from_connection_string(azure_storage_connection_string)
    container_client = blob_service_client.get_container_client(azure_storage_container_name)

    # Create the container if it doesn't exist
    try:
        container_client.create_container()
    except Exception as e:
        # Ignore error if container already exists
        if "ContainerAlreadyExists" not in str(e):
            raise e

    blob_name = f"archives/{record_id}/{file_name}"
    blob_client = container_client.get_blob_client(blob_name)

    if isinstance(content, str):
        content_data = content.encode('utf-8')
    else:
        content_data = content

    blob_client.upload_blob(content_data, overwrite=True, content_settings={'content_type': content_type})
    return blob_client.url
