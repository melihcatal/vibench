from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Mapping

from observability_client import get_s3_client, load_config
from observability_models import ExportArchiveResponse


def metrics_export_archive(snapshot: Mapping[str, Any], bucket: str, key_prefix: str = "metric-archives/") -> ExportArchiveResponse:
    cfg = load_config()
    s3 = get_s3_client(cfg.region_name)
    payload = json.dumps(dict(snapshot), default=str, sort_keys=True).encode("utf-8")
    key = f"{key_prefix}{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    resp = s3.put_object(Bucket=bucket, Key=key, Body=payload, ContentType="application/json")
    return ExportArchiveResponse(bucket=bucket, key=key, etag=resp.get("ETag"))
