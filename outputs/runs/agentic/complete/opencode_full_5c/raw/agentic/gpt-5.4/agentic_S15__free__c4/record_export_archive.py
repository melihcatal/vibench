from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Mapping

from database_client import get_blob_container_client


def archive_record_snapshot(
    record: Mapping[str, object],
    blob_name: str | None = None,
    container_name: str | None = None,
):
    container = get_blob_container_client(container_name)
    target_name = (
        blob_name
        or f"document-snapshots/{record['id']}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    )
    payload = json.dumps(dict(record), ensure_ascii=False).encode("utf-8")
    blob_client = container.get_blob_client(target_name)
    blob_client.upload_blob(payload, overwrite=True)
    return {
        "container": container.container_name,
        "blob_name": target_name,
        "size": len(payload),
    }
