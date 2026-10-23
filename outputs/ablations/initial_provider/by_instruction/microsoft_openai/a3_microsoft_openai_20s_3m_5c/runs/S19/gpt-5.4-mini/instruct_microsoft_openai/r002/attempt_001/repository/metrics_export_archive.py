from typing import Any, Dict

from azure.storage.blob import BlobServiceClient


def metrics_export_archive(connection_string: str, container_name: str, blob_name: str, content: bytes) -> Dict[str, Any]:
    client = BlobServiceClient.from_connection_string(connection_string)
    container = client.get_container_client(container_name)
    blob = container.get_blob_client(blob_name)
    blob.upload_blob(content, overwrite=True)
    return {"provider": "Azure Blob Storage", "container": container_name, "blob": blob_name}
