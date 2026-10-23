from __future__ import annotations

import io
import json
import os
from datetime import datetime, timezone
from typing import Any

import boto3
from botocore.exceptions import ClientError


def archive_metric_snapshots(
    snapshots: list[dict[str, Any]],
    bucket_name: str | None = None,
    prefix: str = "metric-snapshots",
    region: str = "us-east-1",
) -> dict[str, Any]:
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID", "")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
    bucket = bucket_name or os.environ.get("S3_METRICS_BUCKET", "metrics-archive")
    s3_client = boto3.client(
        "s3",
        region_name=region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    archived_keys = []
    for i, snapshot in enumerate(snapshots):
        timestamp = datetime.now(timezone.utc).strftime("%Y/%m/%d/%H%M%S")
        object_key = f"{prefix}/{timestamp}/snapshot_{i}.json"
        payload = json.dumps(snapshot, default=str).encode("utf-8")
        try:
            s3_client.put_object(
                Bucket=bucket,
                Key=object_key,
                Body=io.BytesIO(payload),
                ContentType="application/json",
                StorageClass="STANDARD_IA",
            )
            archived_keys.append(object_key)
        except ClientError as e:
            archived_keys.append({"key": object_key, "error": str(e)})
    return {
        "service": "Amazon S3",
        "bucket": bucket,
        "archived_keys": archived_keys,
        "total_snapshots": len(snapshots),
        "successful_archives": len([k for k in archived_keys if isinstance(k, str)]),
    }
