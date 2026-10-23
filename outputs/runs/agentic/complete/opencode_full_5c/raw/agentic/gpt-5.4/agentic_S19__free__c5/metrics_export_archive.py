from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, Optional

from observability_client import upload_json_to_gcs


def metrics_export_archive(
    bucket: str, snapshot: Dict, object_name: Optional[str] = None
) -> dict:
    archive_name = (
        object_name
        or f"metric-snapshots/{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    )
    return upload_json_to_gcs(bucket=bucket, object_name=archive_name, payload=snapshot)
