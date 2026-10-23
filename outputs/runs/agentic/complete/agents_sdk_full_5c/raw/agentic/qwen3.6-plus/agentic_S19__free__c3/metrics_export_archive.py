"""
metrics_export_archive.py
Archive exported metric snapshots in managed object storage using the AWS S3 API.
Provider: Amazon Web Services S3 (s3.amazonaws.com)
"""

import os
import io
import json
import gzip
import csv
import time
from typing import List, Optional, Dict, Any, BinaryIO
from datetime import datetime

import boto3
from botocore.exceptions import ClientError

from observability_models import (
    MetricSeries,
    MetricStats,
    MetricSummary,
    Datapoint,
)

S3_ENDPOINT = "s3.amazonaws.com"


def archive_metric_snapshot(
    series_list: List[MetricSeries],
    bucket_name: str,
    snapshot_key: str,
    region: Optional[str] = None,
    compression: str = "gzip",
    storage_class: str = "STANDARD_IA",
    access_key_id: Optional[str] = None,
    secret_access_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Archive a list of MetricSeries snapshots to AWS S3 managed object storage.

    Serializes metric series data to JSON and uploads to the specified S3 bucket.
    Supports gzip compression and configurable storage class.

    Args:
        series_list: List of MetricSeries objects to archive.
        bucket_name: Target S3 bucket name.
        snapshot_key: S3 object key (path) for the snapshot.
        region: AWS region (e.g. "us-east-1").
        compression: Compression type ("gzip" or "none").
        storage_class: S3 storage class (e.g. "STANDARD_IA", "GLACIER").
        access_key_id: Optional AWS access key ID.
        secret_access_key: Optional AWS secret access key.

    Returns:
        Dict with archive metadata including S3 URI, size, and ETag.
    """
    access_key_id = access_key_id or os.environ.get("AWS_ACCESS_KEY_ID", "")
    secret_access_key = secret_access_key or os.environ.get("AWS_SECRET_ACCESS_KEY", "")
    region = region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    s3_client = boto3.client(
        "s3",
        region_name=region,
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
    )

    snapshot_data = {
        "metadata": {
            "exported_at": datetime.utcnow().isoformat() + "Z",
            "metric_count": len(series_list),
            "format_version": "1.0",
        },
        "series": [_serialize_metric_series(s) for s in series_list],
    }

    json_payload = json.dumps(snapshot_data, indent=2)

    if compression == "gzip":
        buf = io.BytesIO()
        with gzip.GzipFile(fileobj=buf, mode="wb", compresslevel=6) as gz:
            gz.write(json_payload.encode("utf-8"))
        upload_body = buf.getvalue()
        content_type = "application/gzip"
        content_encoding = "gzip"
        if not snapshot_key.endswith(".json.gz"):
            snapshot_key = snapshot_key + ".json.gz"
    else:
        upload_body = json_payload.encode("utf-8")
        content_type = "application/json"
        content_encoding = None

    upload_kwargs = {
        "Bucket": bucket_name,
        "Key": snapshot_key,
        "Body": upload_body,
        "ContentType": content_type,
        "StorageClass": storage_class,
    }

    if content_encoding:
        upload_kwargs["ContentEncoding"] = content_encoding

    try:
        response = s3_client.put_object(**upload_kwargs)

        s3_uri = f"s3://{bucket_name}/{snapshot_key}"

        return {
            "s3_uri": s3_uri,
            "bucket": bucket_name,
            "key": snapshot_key,
            "etag": response.get("ETag", "").strip('"'),
            "size_bytes": len(upload_body),
            "compressed": compression == "gzip",
            "storage_class": storage_class,
            "series_count": len(series_list),
            "exported_at": snapshot_data["metadata"]["exported_at"],
        }

    except ClientError as exc:
        raise RuntimeError(
            f"AWS S3 archive failed to {s3_uri}: {exc}"
        ) from exc


def archive_metric_stats(
    stats_list: List[MetricStats],
    bucket_name: str,
    snapshot_key: str,
    region: Optional[str] = None,
    storage_class: str = "STANDARD_IA",
    access_key_id: Optional[str] = None,
    secret_access_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Archive aggregated metric statistics to AWS S3.

    Args:
        stats_list: List of MetricStats objects.
        bucket_name: Target S3 bucket name.
        snapshot_key: S3 object key.
        region: AWS region.
        storage_class: S3 storage class.
        access_key_id: Optional AWS access key ID.
        secret_access_key: Optional AWS secret access key.

    Returns:
        Archive metadata dict.
    """
    access_key_id = access_key_id or os.environ.get("AWS_ACCESS_KEY_ID", "")
    secret_access_key = secret_access_key or os.environ.get("AWS_SECRET_ACCESS_KEY", "")
    region = region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    s3_client = boto3.client(
        "s3",
        region_name=region,
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
    )

    stats_data = {
        "metadata": {
            "exported_at": datetime.utcnow().isoformat() + "Z",
            "stats_count": len(stats_list),
            "format_version": "1.0",
        },
        "statistics": [_serialize_metric_stats(s) for s in stats_list],
    }

    json_payload = json.dumps(stats_data, indent=2)
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", compresslevel=6) as gz:
        gz.write(json_payload.encode("utf-8"))
    upload_body = buf.getvalue()

    if not snapshot_key.endswith(".json.gz"):
        snapshot_key = snapshot_key + ".json.gz"

    try:
        response = s3_client.put_object(
            Bucket=bucket_name,
            Key=snapshot_key,
            Body=upload_body,
            ContentType="application/gzip",
            ContentEncoding="gzip",
            StorageClass=storage_class,
        )

        s3_uri = f"s3://{bucket_name}/{snapshot_key}"

        return {
            "s3_uri": s3_uri,
            "bucket": bucket_name,
            "key": snapshot_key,
            "etag": response.get("ETag", "").strip('"'),
            "size_bytes": len(upload_body),
            "compressed": True,
            "storage_class": storage_class,
            "stats_count": len(stats_list),
            "exported_at": stats_data["metadata"]["exported_at"],
        }

    except ClientError as exc:
        raise RuntimeError(
            f"AWS S3 stats archive failed to {s3_uri}: {exc}"
        ) from exc


def archive_metric_csv(
    series: MetricSeries,
    bucket_name: str,
    snapshot_key: str,
    region: Optional[str] = None,
    storage_class: str = "STANDARD",
    access_key_id: Optional[str] = None,
    secret_access_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Archive a metric series as CSV to AWS S3 managed object storage.

    Args:
        series: A single MetricSeries to export.
        bucket_name: Target S3 bucket name.
        snapshot_key: S3 object key.
        region: AWS region.
        storage_class: S3 storage class.
        access_key_id: Optional AWS access key ID.
        secret_access_key: Optional AWS secret access key.

    Returns:
        Archive metadata dict.
    """
    access_key_id = access_key_id or os.environ.get("AWS_ACCESS_KEY_ID", "")
    secret_access_key = secret_access_key or os.environ.get("AWS_SECRET_ACCESS_KEY", "")
    region = region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    s3_client = boto3.client(
        "s3",
        region_name=region,
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
    )

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["timestamp", "value", "metric_name"])

    for dp in series.datapoints:
        writer.writerow([dp.timestamp, dp.value if dp.value is not None else "", dp.metric_name])

    csv_content = output.getvalue()

    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", compresslevel=6) as gz:
        gz.write(csv_content.encode("utf-8"))
    upload_body = buf.getvalue()

    if not snapshot_key.endswith(".csv.gz"):
        snapshot_key = snapshot_key + ".csv.gz"

    try:
        response = s3_client.put_object(
            Bucket=bucket_name,
            Key=snapshot_key,
            Body=upload_body,
            ContentType="application/gzip",
            ContentEncoding="gzip",
            StorageClass=storage_class,
        )

        s3_uri = f"s3://{bucket_name}/{snapshot_key}"

        return {
            "s3_uri": s3_uri,
            "bucket": bucket_name,
            "key": snapshot_key,
            "etag": response.get("ETag", "").strip('"'),
            "size_bytes": len(upload_body),
            "compressed": True,
            "format": "csv",
            "storage_class": storage_class,
            "datapoint_count": len(series.datapoints),
        }

    except ClientError as exc:
        raise RuntimeError(
            f"AWS S3 CSV archive failed to {s3_uri}: {exc}"
        ) from exc


def list_archived_snapshots(
    bucket_name: str,
    prefix: str = "",
    region: Optional[str] = None,
    access_key_id: Optional[str] = None,
    secret_access_key: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    List archived metric snapshots from AWS S3.

    Args:
        bucket_name: S3 bucket name.
        prefix: Optional key prefix to filter results.
        region: AWS region.
        access_key_id: Optional AWS access key ID.
        secret_access_key: Optional AWS secret access key.

    Returns:
        List of snapshot metadata dicts.
    """
    access_key_id = access_key_id or os.environ.get("AWS_ACCESS_KEY_ID", "")
    secret_access_key = secret_access_key or os.environ.get("AWS_SECRET_ACCESS_KEY", "")
    region = region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    s3_client = boto3.client(
        "s3",
        region_name=region,
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
    )

    try:
        response = s3_client.list_objects_v2(
            Bucket=bucket_name,
            Prefix=prefix,
        )

        snapshots = []
        for obj in response.get("Contents", []):
            snapshots.append({
                "s3_uri": f"s3://{bucket_name}/{obj['Key']}",
                "key": obj["Key"],
                "size_bytes": obj["Size"],
                "last_modified": obj["LastModified"].isoformat(),
                "storage_class": obj.get("StorageClass", "STANDARD"),
                "etag": obj.get("ETag", "").strip('"'),
            })

        return snapshots

    except ClientError as exc:
        raise RuntimeError(
            f"AWS S3 list failed for bucket '{bucket_name}': {exc}"
        ) from exc


def _serialize_metric_series(series: MetricSeries) -> Dict[str, Any]:
    """Serialize a MetricSeries to a JSON-compatible dict."""
    return {
        "metric_name": series.metric_name,
        "display_name": series.display_name,
        "tags": series.tags,
        "start_time": series.start_time,
        "end_time": series.end_time,
        "aggregation": series.aggregation,
        "datapoints": [
            {
                "timestamp": dp.timestamp,
                "value": dp.value,
            }
            for dp in series.datapoints
        ],
    }


def _serialize_metric_stats(stats: MetricStats) -> Dict[str, Any]:
    """Serialize a MetricStats to a JSON-compatible dict."""
    return {
        "metric_name": stats.metric_name,
        "start_time": stats.start_time,
        "end_time": stats.end_time,
        "aggregation": stats.aggregation,
        "count": stats.count,
        "avg": stats.avg,
        "min": stats.min,
        "max": stats.max,
        "sum": stats.sum,
        "std_dev": stats.std_dev,
        "p50": stats.p50,
        "p95": stats.p95,
        "p99": stats.p99,
    }
