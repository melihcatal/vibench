"""
metrics_export_archive.py - Archive exported metric snapshots in managed object storage.
Uses Amazon S3 (boto3) for object storage.
Provider: Amazon S3
SDK: boto3
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

from __future__ import annotations

import datetime
import gzip
import json
import os
import sys
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError

from observability_client import (
    DatadogConfig,
    DatadogMetricsClient,
    build_windowed_request,
)
from observability_models import compute_series_stats


def archive_metric_snapshot(
    metric_name: str,
    bucket_name: str,
    window_minutes: int = 60,
    tags: Optional[List[str]] = None,
    archive_key: Optional[str] = None,
    s3_region: Optional[str] = None,
    storage_class: str = "STANDARD_IA",
) -> Dict[str, Any]:
    """
    Export metric data from Datadog and archive the snapshot in Amazon S3.

    Retrieves the full metric series data, computes summary statistics,
    serializes everything to JSON, compresses it with gzip, and uploads
    to the specified S3 bucket.

    Args:
        metric_name: The Datadog metric identifier.
        bucket_name: Target S3 bucket name.
        window_minutes: Time window in minutes.
        tags: Optional tag filters.
        archive_key: Optional S3 object key. Auto-generated if None.
        s3_region: Optional AWS region. Falls back to AWS_DEFAULT_REGION.
        storage_class: S3 storage class (default: STANDARD_IA).

    Returns:
        Dict with archive metadata and S3 upload details.
    """
    config = DatadogConfig()
    client = DatadogMetricsClient(config)

    request = build_windowed_request(
        metric_name=metric_name,
        window_minutes=window_minutes,
        aggregation="avg",
        rollup=60,
        tags=tags,
    )

    response = client.query(request)

    if archive_key is None:
        now_str = datetime.datetime.now(datetime.timezone.utc).strftime(
            "%Y/%m/%d/%H%M%S"
        )
        archive_key = f"metrics/snapshots/{now_str}/{metric_name}.json.gz"

    snapshot_data: Dict[str, Any] = {
        "export_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "metric": metric_name,
        "window_minutes": window_minutes,
        "tags": tags,
        "from_ts": response.from_ts,
        "to_ts": response.to_ts,
        "query": response.query,
        "status": response.status,
        "series": [],
        "summary": {},
    }

    all_values: List[float] = []
    for series in response.series:
        series_data = {
            "metric": series.metric_name,
            "display_name": series.display_name,
            "scope": series.scope,
            "unit": series.unit,
            "expression": series.expression,
            "points": [
                {"timestamp": p.timestamp, "value": p.value}
                for p in series.points
            ],
        }
        snapshot_data["series"].append(series_data)
        all_values.extend(series.values())

    if all_values:
        stats = compute_series_stats(
            type('Series', (), {
                'metric_name': metric_name,
                'points': [
                    type('P', (), {'timestamp': 0, 'value': v})()
                    for v in all_values
                ],
            })()
        )
        from observability_models import MetricSeries, MetricPoint
        temp_series = MetricSeries(
            metric_name=metric_name,
            display_name=metric_name,
            points=[MetricPoint(timestamp=0, value=v) for v in all_values],
        )
        stats = compute_series_stats(temp_series)
        snapshot_data["summary"] = {
            "total_points": stats.count,
            "avg": round(stats.avg, 6),
            "min": round(stats.min, 6),
            "max": round(stats.max, 6),
            "sum": round(stats.sum, 6),
            "stddev": round(stats.stddev, 6) if stats.stddev else None,
        }

    json_bytes = json.dumps(snapshot_data, indent=2).encode("utf-8")
    compressed = gzip.compress(json_bytes)

    region = s3_region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    s3_client = boto3.client("s3", region_name=region)

    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=archive_key,
            Body=compressed,
            StorageClass=storage_class,
            ContentType="application/gzip",
            Metadata={
                "metric-name": metric_name,
                "window-minutes": str(window_minutes),
                "export-timestamp": datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat(),
            },
        )

        result: Dict[str, Any] = {
            "status": "archived",
            "bucket": bucket_name,
            "key": archive_key,
            "region": region,
            "storage_class": storage_class,
            "original_size": len(json_bytes),
            "compressed_size": len(compressed),
            "compression_ratio": round(
                len(compressed) / max(len(json_bytes), 1), 4
            ),
            "snapshot_summary": snapshot_data["summary"],
        }
        return result

    except ClientError as exc:
        return {
            "status": "error",
            "error": str(exc),
            "bucket": bucket_name,
            "key": archive_key,
        }


def list_archived_snapshots(
    bucket_name: str,
    prefix: str = "metrics/snapshots/",
    s3_region: Optional[str] = None,
    max_keys: int = 50,
) -> List[Dict[str, Any]]:
    """List previously archived metric snapshots from S3."""
    region = s3_region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    s3_client = boto3.client("s3", region_name=region)

    try:
        response = s3_client.list_objects_v2(
            Bucket=bucket_name,
            Prefix=prefix,
            MaxKeys=max_keys,
        )

        objects = response.get("Contents", [])
        result = []
        for obj in objects:
            result.append({
                "key": obj["Key"],
                "size": obj["Size"],
                "last_modified": obj["LastModified"].isoformat(),
                "storage_class": obj.get("StorageClass", "STANDARD"),
            })

        return result

    except ClientError as exc:
        return [{"error": str(exc)}]


def main():
    if len(sys.argv) < 3:
        print(
            "Usage: metrics_export_archive.py <metric_name> <bucket_name> "
            "[--window MINUTES] [--region REGION] [--storage-class CLASS]"
        )
        sys.exit(1)

    metric_name = sys.argv[1]
    bucket_name = sys.argv[2]
    window = 60
    region = None
    storage_class = "STANDARD_IA"

    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == "--window" and i + 1 < len(sys.argv):
            window = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--region" and i + 1 < len(sys.argv):
            region = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--storage-class" and i + 1 < len(sys.argv):
            storage_class = sys.argv[i + 1]
            i += 2
        else:
            i += 1

    result = archive_metric_snapshot(
        metric_name=metric_name,
        bucket_name=bucket_name,
        window_minutes=window,
        s3_region=region,
        storage_class=storage_class,
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
