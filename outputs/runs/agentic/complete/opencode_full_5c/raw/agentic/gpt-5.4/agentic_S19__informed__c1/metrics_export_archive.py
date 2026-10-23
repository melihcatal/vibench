from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Dict

from observability_client import s3_client


def metrics_export_archive(
    bucket: str,
    export_name: str,
    snapshot: Dict[str, Any],
    prefix: str = "metrics-archive",
) -> Dict[str, Any]:
    client = s3_client()
    exported_at = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    key = f"{prefix.rstrip('/')}/{export_name}-{exported_at}.json"
    body = json.dumps(snapshot, separators=(",", ":")).encode("utf-8")
    response = client.put_object(
        Bucket=bucket,
        Key=key,
        Body=body,
        ContentType="application/json",
    )
    return {
        "provider": "amazon-s3",
        "bucket": bucket,
        "key": key,
        "etag": response.get("ETag"),
        "version_id": response.get("VersionId"),
    }
