from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from observability_client import load_config, s3_client
from observability_models import ArchiveResult


S3_ENDPOINT = "s3.amazonaws.com"


def metrics_export_archive(snapshot: Dict[str, Any], key_prefix: str = "metric-archives", bucket: Optional[str] = None) -> ArchiveResult:
    cfg = load_config()
    archive_bucket = bucket or cfg.s3_archive_bucket
    if not archive_bucket:
        raise ValueError("S3 archive bucket must be provided via argument or S3_ARCHIVE_BUCKET")
    key = f"{key_prefix}/{datetime.now(timezone.utc).strftime('%Y/%m/%d/%H%M%S')}.json"
    client = s3_client()
    response = client.put_object(
        Bucket=archive_bucket,
        Key=key,
        Body=json.dumps(snapshot).encode("utf-8"),
        ContentType="application/json",
    )
    return ArchiveResult(
        bucket=archive_bucket,
        key=key,
        version_id=response.get("VersionId"),
        etag=response.get("ETag"),
        provider=S3_ENDPOINT,
    )
