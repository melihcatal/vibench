"""
Archive exported metric snapshots in managed object storage.

Provider: AWS S3 via boto3 (boto3)
Uses boto3 S3 client connecting to s3.amazonaws.com for archiving
metric snapshot JSON payloads to an S3 bucket.
"""

from __future__ import annotations

import json
import os
import gzip
import io
from datetime import datetime
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError, BotoCoreError

from observability_models import (
    MetricAggregateStats,
    MetricComparisonResult,
    MetricDataPoint,
    MetricSeries,
    MetricTimeWindow,
)


def _serialize_metric_data(data: Any) -> str:
    """Serialize metric data to JSON string with datetime handling."""
    def json_serializer(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, MetricTimeWindow):
            return {
                "start": obj.start.isoformat(),
                "end": obj.end.isoformat(),
                "interval_seconds": obj.interval_seconds,
            }
        if isinstance(obj, MetricDataPoint):
            return {
                "timestamp": obj.timestamp.isoformat(),
                "value": obj.value,
                "tags": obj.tags,
            }
        if isinstance(obj, MetricSeries):
            return {
                "expression": obj.expression,
                "scope": obj.scope,
                "data_points": [json_serializer(dp) for dp in obj.data_points],
            }
        if isinstance(obj, MetricAggregateStats):
            return {
                "metric_name": obj.metric_name,
                "aggregation": obj.aggregation,
                "window": json_serializer(obj.window),
                "min_value": obj.min_value,
                "max_value": obj.max_value,
                "avg_value": obj.avg_value,
                "sum_value": obj.sum_value,
                "count": obj.count,
                "p50": obj.p50,
                "p95": obj.p95,
                "p99": obj.p99,
            }
        if isinstance(obj, MetricComparisonResult):
            return {
                "series_a": json_serializer(obj.series_a),
                "series_b": json_serializer(obj.series_b),
                "correlation": obj.correlation,
                "mean_difference": obj.mean_difference,
                "relative_change_pct": obj.relative_change_pct,
            }
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

    return json.dumps(data, default=json_serializer, indent=2)


def archive_metric_snapshot(
    snapshot_data: Any,
    bucket: str,
    metric_name: str,
    archive_key_prefix: str = "metrics/snapshots",
    compress: bool = True,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    aws_region: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Archive a metric snapshot to AWS S3 managed object storage.

    Uses boto3 S3 client to upload metric data (series, aggregates, comparisons)
    as JSON (optionally gzip-compressed) to an S3 bucket at s3.amazonaws.com.

    Args:
        snapshot_data: Metric data to archive (MetricDataPoint list, MetricSeries, etc.)
        bucket: Target S3 bucket name.
        metric_name: Metric name for organizing the archive path.
        archive_key_prefix: S3 key prefix, default 'metrics/snapshots'.
        compress: Whether to gzip-compress the payload.
        aws_access_key_id: AWS access key (or set AWS_ACCESS_KEY_ID env var).
        aws_secret_access_key: AWS secret key (or set AWS_SECRET_ACCESS_KEY env var).
        aws_region: AWS region (or set AWS_DEFAULT_REGION env var).

    Returns:
        Dict with archive metadata including S3 key, size, and timestamp.
    """
    region = aws_region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    session_kwargs = {"region_name": region}
    if aws_access_key_id:
        session_kwargs["aws_access_key_id"] = aws_access_key_id
    if aws_secret_access_key:
        session_kwargs["aws_secret_access_key"] = aws_secret_access_key

    s3_client = boto3.client("s3", **session_kwargs)

    # Serialize data
    json_payload = _serialize_metric_data(snapshot_data)

    # Optionally compress
    if compress:
        buf = io.BytesIO()
        with gzip.GzipFile(fileobj=buf, mode="wb") as gz:
            gz.write(json_payload.encode("utf-8"))
        payload_bytes = buf.getvalue()
        content_type = "application/gzip"
        content_encoding = "gzip"
    else:
        payload_bytes = json_payload.encode("utf-8")
        content_type = "application/json"
        content_encoding = None

    # Build S3 key with timestamp and metric name
    now = datetime.utcnow()
    date_prefix = now.strftime("%Y/%m/%d")
    file_ext = ".json.gz" if compress else ".json"
    s3_key = f"{archive_key_prefix}/{metric_name}/{date_prefix}/{now.strftime('%H%M%S')}{file_ext}"

    try:
        # Upload to S3 via boto3
        extra_args = {
            "ContentType": content_type,
            "Metadata": {
                "metric-name": metric_name,
                "archived-at": now.isoformat(),
                "snapshot-type": type(snapshot_data).__name__,
            },
        }
        if content_encoding:
            extra_args["ContentEncoding"] = content_encoding

        s3_client.put_object(
            Bucket=bucket,
            Key=s3_key,
            Body=payload_bytes,
            **extra_args,
        )

        return {
            "success": True,
            "bucket": bucket,
            "key": s3_key,
            "size_bytes": len(payload_bytes),
            "compressed": compress,
            "archived_at": now.isoformat(),
            "metric_name": metric_name,
        }
    except ClientError as exc:
        return {
            "success": False,
            "error": str(exc),
            "bucket": bucket,
            "key": s3_key,
            "metric_name": metric_name,
        }
    except BotoCoreError as exc:
        return {
            "success": False,
            "error": str(exc),
            "bucket": bucket,
            "key": s3_key,
            "metric_name": metric_name,
        }


def archive_metric_series_list(
    series_list: List[MetricSeries],
    bucket: str,
    archive_key_prefix: str = "metrics/series",
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    aws_region: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Archive a list of MetricSeries to AWS S3.
    """
    metric_name = series_list[0].expression.split(":")[0] if series_list else "unknown"
    return archive_metric_snapshot(
        snapshot_data=series_list,
        bucket=bucket,
        metric_name=metric_name,
        archive_key_prefix=archive_key_prefix,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_region=aws_region,
    )


def archive_comparison_result(
    comparison: MetricComparisonResult,
    bucket: str,
    archive_key_prefix: str = "metrics/comparisons",
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    aws_region: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Archive a MetricComparisonResult to AWS S3.
    """
    metric_name = comparison.series_a.expression.split(":")[0] if comparison.series_a else "unknown"
    return archive_metric_snapshot(
        snapshot_data=comparison,
        bucket=bucket,
        metric_name=metric_name,
        archive_key_prefix=archive_key_prefix,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_region=aws_region,
    )


def list_archived_snapshots(
    bucket: str,
    metric_name: Optional[str] = None,
    prefix: str = "metrics/snapshots",
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    aws_region: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    List archived metric snapshots from AWS S3.

    Uses boto3 S3 client to list objects under the snapshots prefix.

    Args:
        bucket: S3 bucket name.
        metric_name: Optional metric name to filter by.
        prefix: S3 key prefix to search.
        aws_access_key_id: AWS access key.
        aws_secret_access_key: AWS secret key.
        aws_region: AWS region.

    Returns:
        List of archive metadata dicts.
    """
    region = aws_region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    session_kwargs = {"region_name": region}
    if aws_access_key_id:
        session_kwargs["aws_access_key_id"] = aws_access_key_id
    if aws_secret_access_key:
        session_kwargs["aws_secret_access_key"] = aws_secret_access_key

    s3_client = boto3.client("s3", **session_kwargs)

    if metric_name:
        full_prefix = f"{prefix}/{metric_name}/"
    else:
        full_prefix = prefix

    snapshots = []
    paginator = s3_client.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket, Prefix=full_prefix):
        for obj in page.get("Contents", []):
            snapshots.append({
                "key": obj["Key"],
                "size_bytes": obj["Size"],
                "last_modified": obj["LastModified"].isoformat() if obj.get("LastModified") else None,
                "storage_class": obj.get("StorageClass", "STANDARD"),
            })

    return snapshots
