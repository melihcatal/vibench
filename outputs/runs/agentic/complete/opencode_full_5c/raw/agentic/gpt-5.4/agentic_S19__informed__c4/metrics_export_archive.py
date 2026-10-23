from __future__ import annotations

import json
from typing import Any, Dict

import boto3


def metrics_export_archive(
    snapshot: Dict[str, Any], bucket: str, key: str, region_name: str | None = None
) -> Dict[str, Any]:
    s3 = boto3.client("s3", region_name=region_name)
    body = json.dumps(snapshot, default=str).encode("utf-8")
    response = s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=body,
        ContentType="application/json",
    )
    return {
        "provider": "Amazon S3",
        "bucket": bucket,
        "key": key,
        "etag": response.get("ETag"),
        "version_id": response.get("VersionId"),
    }
