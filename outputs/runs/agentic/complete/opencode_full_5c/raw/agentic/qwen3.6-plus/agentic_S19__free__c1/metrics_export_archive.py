import gzip
import json
import os
from datetime import datetime
from typing import Any, Optional

import boto3
from botocore.exceptions import ClientError

from observability_models import (
    ArchiveResult,
    MetricQueryResponse,
)


S3_STORAGE_CLASS = "STANDARD_IA"


def metrics_export_archive(
    metric_data: MetricQueryResponse,
    bucket_name: str,
    key_prefix: str = "metric-snapshots",
    storage_class: str = S3_STORAGE_CLASS,
    compress: bool = True,
) -> ArchiveResult:
    aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    if not aws_access_key or not aws_secret_key:
        return ArchiveResult(
            key="",
            bucket=bucket_name,
            storage_class=storage_class,
        )

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region,
    )

    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    metric_name = metric_data.metric_name or "unknown"
    safe_metric_name = metric_name.replace(":", "_").replace(".", "_")
    file_name = f"{safe_metric_name}_{timestamp}.json"

    if compress:
        file_name += ".gz"

    key = f"{key_prefix}/{file_name}"

    payload = {
        "metric_name": metric_name,
        "status": metric_data.status,
        "exported_at": datetime.utcnow().isoformat(),
        "datapoints": [
            {"timestamp": ts.isoformat(), "value": val}
            for ts, val in metric_data.datapoints
        ],
        "dimensions": metric_data.dimensions,
        "series_count": len(metric_data.series),
    }

    json_bytes = json.dumps(payload, indent=2).encode("utf-8")

    if compress:
        json_bytes = gzip.compress(json_bytes)

    try:
        put_kwargs = {
            "Bucket": bucket_name,
            "Key": key,
            "Body": json_bytes,
            "ContentType": "application/json" if not compress else "application/gzip",
            "StorageClass": storage_class,
            "Metadata": {
                "metric-name": metric_name,
                "exported-at": datetime.utcnow().isoformat(),
                "datapoint-count": str(len(metric_data.datapoints)),
            },
        }

        response = s3_client.put_object(**put_kwargs)

        return ArchiveResult(
            key=key,
            bucket=bucket_name,
            size_bytes=len(json_bytes),
            etag=response.get("ETag", "").strip('"'),
            storage_class=storage_class,
            archived_at=datetime.utcnow(),
        )

    except ClientError as e:
        return ArchiveResult(
            key=key,
            bucket=bucket_name,
            storage_class=storage_class,
            error=str(e),
        )


def archive_metric_snapshot(
    metric_data: MetricQueryResponse,
    bucket_name: str,
    key_prefix: str = "metric-snapshots",
) -> ArchiveResult:
    return metrics_export_archive(
        metric_data=metric_data,
        bucket_name=bucket_name,
        key_prefix=key_prefix,
        storage_class=S3_STORAGE_CLASS,
        compress=True,
    )


def archive_multiple_snapshots(
    snapshots: list[tuple[MetricQueryResponse, str]],
    bucket_name: str,
    key_prefix: str = "metric-snapshots",
) -> list[ArchiveResult]:
    results = []
    for metric_data, prefix in snapshots:
        result = metrics_export_archive(
            metric_data=metric_data,
            bucket_name=bucket_name,
            key_prefix=f"{key_prefix}/{prefix}",
            storage_class=S3_STORAGE_CLASS,
            compress=True,
        )
        results.append(result)
    return results
