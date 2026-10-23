from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Optional

from azure.storage.blob import BlobServiceClient


def record_export_archive(
    documents: Iterable[Dict[str, Any]], archive_name: Optional[str] = None
) -> Dict[str, Any]:
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container_name = os.getenv("AZURE_STORAGE_CONTAINER")
    if not connection_string:
        raise RuntimeError(
            "Missing required environment variable: AZURE_STORAGE_CONNECTION_STRING"
        )
    if not container_name:
        raise RuntimeError(
            "Missing required environment variable: AZURE_STORAGE_CONTAINER"
        )
    blob_service = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service.get_container_client(container_name)
    container_client.create_container()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    blob_name = archive_name or f"document-archive-{timestamp}.json"
    payload = json.dumps([dict(item) for item in documents], separators=(",", ":"))
    container_client.upload_blob(name=blob_name, data=payload, overwrite=True)
    return {
        "provider": "azure_blob_storage",
        "container": container_name,
        "blob_name": blob_name,
        "bytes": len(payload.encode("utf-8")),
    }
