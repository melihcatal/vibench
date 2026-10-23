from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Dict

import boto3


def archive_metric_snapshot(snapshot: Dict[str, Any], bucket: str, prefix: str = "metric-archives/") -> str:
    s3 = boto3.client("s3")
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    key = f"{prefix.rstrip('/')}/snapshot-{timestamp}.json"
    s3.put_object(Bucket=bucket, Key=key, Body=json.dumps(snapshot, default=str).encode("utf-8"), ContentType="application/json")
    return key
