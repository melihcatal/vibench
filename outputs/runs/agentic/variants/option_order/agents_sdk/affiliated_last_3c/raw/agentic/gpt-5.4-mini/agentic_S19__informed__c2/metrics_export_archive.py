from __future__ import annotations

import json
from datetime import datetime, timezone

from observability_client import CloudWatchMetricsClient, ObservabilityConfig
from observability_models import ExportResult


def metrics_export_archive(payload: dict, object_key: str | None = None) -> ExportResult:
    cfg = ObservabilityConfig()
    client = CloudWatchMetricsClient(cfg)
    key = object_key or f"metrics/{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    body = json.dumps(payload, default=str).encode("utf-8")
    response = client.put_object(key=key, body=body)
    return ExportResult(bucket=cfg.bucket_name, object_key=key, etag=response.get("ETag"), uri=f"s3://{cfg.bucket_name}/{key}")
