from __future__ import annotations

import gzip
import json
import os
import time
from typing import Any

import boto3
from botocore.exceptions import ClientError


S3_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
DEFAULT_BUCKET = os.environ.get("METRICS_ARCHIVE_BUCKET", "metrics-archive")
DEFAULT_PREFIX = "metric-snapshots"


def archive_metric_snapshot(
    snapshot_data: dict[str, Any],
    metric_name: str,
    bucket: str | None = None,
    prefix: str | None = None,
    compress: bool = True,
    client: boto3.client | None = None,
) -> dict[str, Any]:
    if client is None:
        aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID", "")
        aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
        if not aws_access_key or not aws_secret_key:
            raise ValueError(
                "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables must be set"
            )
        client = boto3.client(
            "s3",
            region_name=S3_REGION,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
        )

    target_bucket = bucket or DEFAULT_BUCKET
    target_prefix = prefix or DEFAULT_PREFIX

    ts = int(time.time())
    filename = f"{metric_name}-{ts}.json"
    if compress:
        filename += ".gz"

    object_key = f"{target_prefix}/{filename}"

    if compress:
        payload = json.dumps(snapshot_data, default=str).encode("utf-8")
        body = gzip.compress(payload)
        content_type = "application/gzip"
    else:
        body = json.dumps(snapshot_data, default=str).encode("utf-8")
        content_type = "application/json"

    upload_kwargs: dict[str, Any] = {
        "Bucket": target_bucket,
        "Key": object_key,
        "Body": body,
        "ContentType": content_type,
        "Metadata": {
            "metric-name": metric_name,
            "archived-at": str(ts),
            "compressed": str(compress).lower(),
        },
    }

    client.put_object(**upload_kwargs)

    return {
        "bucket": target_bucket,
        "key": object_key,
        "size_bytes": len(body),
        "compressed": compress,
        "archived_at": ts,
        "metric_name": metric_name,
    }


def list_archived_snapshots(
    metric_name: str | None = None,
    bucket: str | None = None,
    prefix: str | None = None,
    client: boto3.client | None = None,
) -> list[dict[str, Any]]:
    if client is None:
        aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID", "")
        aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
        if not aws_access_key or not aws_secret_key:
            raise ValueError(
                "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables must be set"
            )
        client = boto3.client(
            "s3",
            region_name=S3_REGION,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
        )

    target_bucket = bucket or DEFAULT_BUCKET
    target_prefix = prefix or DEFAULT_PREFIX
    if metric_name:
        target_prefix = f"{target_prefix}/{metric_name}"

    paginator = client.get_paginator("list_objects_v2")
    results = []
    for page in paginator.paginate(Bucket=target_bucket, Prefix=target_prefix):
        for obj in page.get("Contents", []):
            results.append(
                {
                    "key": obj["Key"],
                    "size": obj["Size"],
                    "last_modified": obj["LastModified"].isoformat(),
                }
            )

    return results


if __name__ == "__main__":
    import json

    sample_snapshot = {
        "metric": "system.cpu.user",
        "timestamp": int(time.time()),
        "values": [45.2, 47.8, 50.1, 52.3],
        "tags": {"env": "production", "host": "web-01"},
    }
    result = archive_metric_snapshot(sample_snapshot, metric_name="system.cpu.user")
    print(json.dumps(result, indent=2))
