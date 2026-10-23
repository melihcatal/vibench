from __future__ import annotations

import json
import os
from typing import Any, Dict

from azure.storage.blob import BlobServiceClient

from database_models import ArchiveResult


AZURE_STORAGE_CONNECTION_STRING_ENV = "AZURE_STORAGE_CONNECTION_STRING"
AZURE_STORAGE_CONTAINER_ENV = "AZURE_STORAGE_CONTAINER"



def archive_document_snapshot(document: Dict[str, Any]) -> ArchiveResult:
    connection_string = os.environ[AZURE_STORAGE_CONNECTION_STRING_ENV]
    container_name = os.environ.get(AZURE_STORAGE_CONTAINER_ENV, "document-archives")
    blob_service = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service.get_container_client(container_name)
    try:
        container_client.create_container()
    except Exception:
        pass

    document_id = str(document.get("id"))
    blob_name = f"snapshots/{document_id}.json"
    payload = json.dumps(document, ensure_ascii=False, indent=2).encode("utf-8")
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(payload, overwrite=True)
    return ArchiveResult(
        document_id=document_id,
        blob_url=blob_client.url,
        container=container_name,
        blob_name=blob_name,
    )
