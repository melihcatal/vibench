import json
import os
from typing import Any, Dict

from azure.storage.blob import BlobServiceClient, ContentSettings

AZURE_BLOB_CONNECTION_STRING_ENV = "AZURE_STORAGE_CONNECTION_STRING"
AZURE_BLOB_CONTAINER_ENV = "AZURE_STORAGE_CONTAINER"


def archive_image_analysis_artifacts(artifact_name: str, payload: Dict[str, Any]) -> str:
    connection_string = os.environ.get(AZURE_BLOB_CONNECTION_STRING_ENV, "").strip()
    container_name = os.environ.get(AZURE_BLOB_CONTAINER_ENV, "").strip()
    if not connection_string or not container_name:
        raise ValueError("AZURE_STORAGE_CONNECTION_STRING and AZURE_STORAGE_CONTAINER are required")
    service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = service_client.get_container_client(container_name)
    try:
        container_client.create_container()
    except Exception:
        pass
    blob_client = container_client.get_blob_client(f"{artifact_name}.json")
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    blob_client.upload_blob(data, overwrite=True, content_settings=ContentSettings(content_type="application/json"))
    return blob_client.url
