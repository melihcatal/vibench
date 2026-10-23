"""
Archive exported metric snapshots in managed object storage using Amazon S3.

Serializes metric data to JSON and uploads to Amazon S3 for archival.
Provider: Amazon S3 (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY).
"""

import json
import os
from datetime import datetime, timezone
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from observability_models import MetricSeries, MetricAggregation

S3_DEFAULT_BUCKET = os.environ.get("METRICS_S3_BUCKET", "metrics-archives")
S3_DEFAULT_REGION = os.environ.get("METRICS_S3_REGION", "us-east-1")


def _get_s3_client(region: Optional[str] = None) -> boto3.client:
    """Create an authenticated S3 client using boto3."""
    aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    if not aws_access_key or not aws_secret_key:
        raise EnvironmentError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables are required"
        )
    region_name = region or S3_DEFAULT_REGION
    return boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=region_name,
    )


def archive_metric_snapshot(
    series: MetricSeries,
    bucket: Optional[str] = None,
    key_prefix: str = "metrics/snapshots",
    region: Optional[str] = None,
) -> str:
    """
    Archive a single metric series snapshot to Amazon S3.

    Args:
        series: MetricSeries to archive.
        bucket: S3 bucket name (default: METRICS_S3_BUCKET env var).
        key_prefix: S3 key prefix for the object.
        region: AWS region for the S3 client.

    Returns:
        S3 object key of the archived snapshot.
    """
    client = _get_s3_client(region)
    bucket_name = bucket or S3_DEFAULT_BUCKET

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    safe_metric = series.metric.replace(".", "_").replace("/", "_")
    object_key = f"{key_prefix}/{safe_metric}/{timestamp}.json"

    snapshot_data = {
        "metric": series.metric,
        "exported_at": timestamp,
        "point_count": series.count,
        "display_name": series.display_name,
        "unit": series.unit,
        "tag_set": series.tag_set,
        "points": [
            {"timestamp": p.timestamp.isoformat(), "value": p.value}
            for p in series.points
        ],
    }

    payload = json.dumps(snapshot_data, indent=2).encode("utf-8")

    client.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=payload,
        ContentType="application/json",
        Metadata={
            "metric-name": series.metric,
            "export-timestamp": timestamp,
        },
    )

    return object_key


def archive_metric_aggregation(
    aggregation: MetricAggregation,
    bucket: Optional[str] = None,
    key_prefix: str = "metrics/aggregations",
    region: Optional[str] = None,
) -> str:
    """
    Archive a metric aggregation to Amazon S3.

    Args:
        aggregation: MetricAggregation to archive.
        bucket: S3 bucket name.
        key_prefix: S3 key prefix.
        region: AWS region.

    Returns:
        S3 object key.
    """
    client = _get_s3_client(region)
    bucket_name = bucket or S3_DEFAULT_BUCKET

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    safe_metric = aggregation.metric.replace(".", "_").replace("/", "_")
    object_key = f"{key_prefix}/{safe_metric}/{timestamp}.json"

    snapshot_data = {
        "metric": aggregation.metric,
        "exported_at": timestamp,
        "aggregation": {
            "avg": aggregation.avg,
            "min": aggregation.min_val,
            "max": aggregation.max_val,
            "sum": aggregation.sum_val,
            "count": aggregation.count,
            "percentiles": aggregation.percentiles,
        },
        "tag_set": aggregation.tag_set,
    }

    payload = json.dumps(snapshot_data, indent=2).encode("utf-8")

    client.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=payload,
        ContentType="application/json",
    )

    return object_key


def archive_metric_batch(
    series_list: list[MetricSeries],
    bucket: Optional[str] = None,
    key_prefix: str = "metrics/snapshots",
    region: Optional[str] = None,
) -> list[str]:
    """
    Archive multiple metric series to Amazon S3.

    Args:
        series_list: List of MetricSeries to archive.
        bucket: S3 bucket name.
        key_prefix: S3 key prefix.
        region: AWS region.

    Returns:
        List of S3 object keys.
    """
    keys = []
    for series in series_list:
        key = archive_metric_snapshot(series, bucket=bucket, key_prefix=key_prefix, region=region)
        keys.append(key)
    return keys


def list_archived_metrics(
    bucket: Optional[str] = None,
    key_prefix: str = "metrics/snapshots",
    region: Optional[str] = None,
) -> list[dict]:
    """
    List archived metric snapshots in Amazon S3.

    Args:
        bucket: S3 bucket name.
        key_prefix: S3 key prefix to filter by.
        region: AWS region.

    Returns:
        List of dicts with key, size, and last_modified.
    """
    client = _get_s3_client(region)
    bucket_name = bucket or S3_DEFAULT_BUCKET

    response = client.list_objects_v2(
        Bucket=bucket_name,
        Prefix=key_prefix,
    )

    objects = response.get("Contents", [])
    return [
        {
            "key": obj["Key"],
            "size": obj["Size"],
            "last_modified": obj["LastModified"].isoformat(),
        }
        for obj in objects
    ]


def retrieve_archived_snapshot(
    object_key: str,
    bucket: Optional[str] = None,
    region: Optional[str] = None,
) -> dict:
    """
    Retrieve an archived metric snapshot from Amazon S3.

    Args:
        object_key: S3 object key.
        bucket: S3 bucket name.
        region: AWS region.

    Returns:
        Deserialized snapshot data.
    """
    client = _get_s3_client(region)
    bucket_name = bucket or S3_DEFAULT_BUCKET

    response = client.get_object(Bucket=bucket_name, Key=object_key)
    data = json.loads(response["Body"].read().decode("utf-8"))
    return data
