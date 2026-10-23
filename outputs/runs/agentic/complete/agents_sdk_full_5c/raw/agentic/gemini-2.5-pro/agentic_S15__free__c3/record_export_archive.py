import os
from azure.storage.blob import BlobServiceClient
from typing import Dict, Any
import json

def record_export_archive(record: Dict[str, Any], record_id: str) -> str:
    """
    Archives a document snapshot as a JSON file in Azure Blob Storage.

    Args:
        record: The document data to archive.
        record_id: A unique ID for the record, used as the blob name.

    Returns:
        The URL of the archived blob.
    """
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")

    if not connection_string or not container_name:
        raise ValueError("Azure Storage credentials not set in environment variables.")

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    
    blob_name = f"{record_id}.json"
    blob_client = blob_service_client.get_blob_client(
        container=container_name, 
        blob=blob_name
    )

    # Serialize the record to a JSON string
    record_bytes = json.dumps(record, indent=2).encode('utf-8')

    blob_client.upload_blob(record_bytes, overwrite=True)

    return blob_client.url
