import json
from datetime import datetime, timezone
from typing import Any, Dict

from azure.storage.blob import ContentSettings

from database_client import get_blob_container_client


def record_export_archive(
    snapshot: Dict[str, Any], archive_name: str | None = None
) -> Dict[str, Any]:
    container = get_blob_container_client()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    blob_name = archive_name or f"document-export-{timestamp}.json"
    payload = json.dumps(snapshot, ensure_ascii=False).encode("utf-8")
    blob_client = container.get_blob_client(blob_name)
    blob_client.upload_blob(
        payload,
        overwrite=True,
        content_settings=ContentSettings(content_type="application/json"),
    )
    return {
        "provider": "azure-blob-storage",
        "blobName": blob_name,
        "container": container.container_name,
        "size": len(payload),
    }
