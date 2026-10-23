import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

AZURE_STORAGE_CONNECTION_STRING = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
AZURE_STORAGE_CONTAINER_NAME = os.environ.get("AZURE_STORAGE_CONTAINER_NAME", "document-archives")

def archive_document_snapshot(document_id: str, content: bytes, file_extension: str = "json") -> str:
    if not AZURE_STORAGE_CONNECTION_STRING:
        raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable must be set.")
    
    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

    # Get a blob client for the container and blob name
    container_client: ContainerClient = blob_service_client.get_container_client(AZURE_STORAGE_CONTAINER_NAME)
    
    # Create container if it does not exist
    try:
        container_client.create_container()
    except Exception as e:
        # Ignore error if container already exists
        if "ContainerAlreadyExists" not in str(e):
            raise

    blob_name = f"{document_id}_archive.{file_extension}"
    blob_client: BlobClient = container_client.get_blob_client(blob_name)

    # Upload the document content
    blob_client.upload_blob(content, overwrite=True)

    return blob_client.url
