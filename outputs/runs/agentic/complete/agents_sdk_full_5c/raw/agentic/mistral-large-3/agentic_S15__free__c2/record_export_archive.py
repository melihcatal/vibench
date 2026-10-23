import os
from typing import Dict, Any
from azure.storage.blob import BlobServiceClient

def archive_document(document: Dict[str, Any], blob_name: str) -> str:
    """
    Archives exported document snapshots in Azure Blob Storage.
    """
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING", "<your-connection-string>")
    container_name = os.getenv("AZURE_STORAGE_CONTAINER", "document-archives")
    
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    
    if not container_client.exists():
        container_client.create_container()
    
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(str(document), overwrite=True)
    
    return f"https://{blob_client.account_name}.blob.core.windows.net/{container_name}/{blob_name}"