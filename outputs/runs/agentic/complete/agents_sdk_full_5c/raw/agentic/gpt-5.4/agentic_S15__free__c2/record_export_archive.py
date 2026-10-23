from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any, Mapping

from azure.storage.blob import BlobServiceClient


AZURE_STORAGE_CONNECTION_STRING_ENV = "AZURE_STORAGE_CONNECTION_STRING"
AZURE_BLOB_CONTAINER_ENV = "AZURE_BLOB_CONTAINER"


def archive_document_snapshot(document: Mapping[str, Any], prefix: str = "exports") -> str:
    service = BlobServiceClient.from_connection_string(os.environ[AZURE_STORAGE_CONNECTION_STRING_ENV])
    container_name = os.getenv(AZURE_BLOB_CONTAINER_ENV, "document-archive")
    container = service.get_container_client(container_name)
    try:
        container.create_container()
    except Exception:
        pass

    doc_id = str(document.get("id", "unknown"))
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    blob_name = f"{prefix}/{doc_id}-{timestamp}.json"
    blob = container.get_blob_client(blob_name)
    blob.upload_blob(json.dumps(dict(document), ensure_ascii=False).encode("utf-8"), overwrite=True)
    return f"https://{service.account_name}.blob.core.windows.net/{container_name}/{blob_name}"
