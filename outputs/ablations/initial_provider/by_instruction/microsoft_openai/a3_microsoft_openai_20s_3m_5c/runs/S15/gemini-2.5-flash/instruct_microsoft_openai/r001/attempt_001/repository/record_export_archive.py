import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

AZURE_STORAGE_CONNECTION_STRING = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
AZURE_STORAGE_CONTAINER_NAME = os.environ.get("AZURE_STORAGE_CONTAINER_NAME", "document-archives")

def archive_document_snapshot(document_id: str, document_content: str, file_name: str | None = None) -> dict:
    if not AZURE_STORAGE_CONNECTION_STRING:
        raise ValueError("AZURE_STORAGE_CONNECTION_STRING must be set in environment variables")
    
    if file_name is None:
        file_name = f"{document_id}_snapshot.json"

    blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(AZURE_STORAGE_CONTAINER_NAME)
    
    try:
        container_client.create_container()
    except Exception as e:
        # Container already exists or other error
        pass

    blob_client = container_client.get_blob_client(file_name)
    blob_client.upload_blob(document_content.encode('utf-8'), overwrite=True)
    
    return {"status": "success", "blob_name": file_name, "blob_url": blob_client.url}
