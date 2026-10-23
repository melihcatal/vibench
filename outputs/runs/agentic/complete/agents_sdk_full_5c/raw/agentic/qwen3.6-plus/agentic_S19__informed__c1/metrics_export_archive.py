"""Archive exported metric snapshots in managed object storage.

Uses Amazon S3 (boto3 SDK) to upload metric snapshot data as archived
objects in an S3 bucket with configurable prefixes, metadata, and
storage class settings.
Provider signals:
  - boto3.client("s3") / boto3.resource("s3")
  - s3.put_object, s3.upload_fileobj API calls
  - AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY environment variables
"""

from __future__ import annotations

import gzip
import io
import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import boto3

from observability_models import MetricSeries, compute_series_stats


def archive_metric_snapshot(
    series_list: List[MetricSeries],
    bucket: str,
    metric_name: str,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    aws_region: str = "us-east-1",
    storage_class: str = "STANDARD_IA",
    prefix: Optional[str] = None,
    metadata: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """Archive a metric snapshot to Amazon S3 as a gzip-compressed JSON file.

    Parameters
    ----------
    series_list : list[MetricSeries]
        Metric series data to archive.
    bucket : str
        S3 bucket name.
    metric_name : str
        Metric name used for object key prefix.
    aws_access_key_id : str, optional
        AWS access key; falls back to AWS_ACCESS_KEY_ID env var.
    aws_secret_access_key : str, optional
        AWS secret key; falls back to AWS_SECRET_ACCESS_KEY env var.
    aws_region : str
        AWS region for the S3 endpoint.
    storage_class : str
        S3 storage class (e.g. "STANDARD_IA", "GLACIER", "STANDARD").
    prefix : str, optional
        S3 key prefix; defaults to "metrics-archives/<metric_name>/".
    metadata : dict, optional
        Additional S3 object metadata.

    Returns
    -------
    dict
        Upload result with bucket, key, size, and etag.
    """
    access_key = aws_access_key_id or os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = aws_secret_access_key or os.environ.get("AWS_SECRET_ACCESS_KEY")

    if not access_key or not secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are required for "
            "Amazon S3 access."
        )

    s3_client = boto3.client(
        "s3",
        region_name=aws_region,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )

    payload = _build_snapshot_payload(series_list, metric_name)
    compressed = _gzip_compress(payload)

    now = datetime.utcnow()
    key_prefix = prefix or f"metrics-archives/{metric_name}"
    object_key = f"{key_prefix}/{now.strftime('%Y/%m/%d/%H%M%S')}_snapshot.json.gz"

    s3_metadata = metadata or {}
    s3_metadata["metric-name"] = metric_name
    s3_metadata["snapshot-timestamp"] = now.isoformat()
    s3_metadata["series-count"] = str(len(series_list))

    response = s3_client.put_object(
        Bucket=bucket,
        Key=object_key,
        Body=compressed,
        StorageClass=storage_class,
        ContentType="application/gzip",
        Metadata=s3_metadata,
    )

    return {
        "bucket": bucket,
        "key": object_key,
        "size_bytes": len(compressed),
        "etag": response.get("ETag", "").strip('"'),
        "storage_class": storage_class,
    }


def archive_batch_metric_snapshots(
    snapshots: List[Dict[str, Any]],
    bucket: str,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    aws_region: str = "us-east-1",
    storage_class: str = "STANDARD_IA",
) -> List[Dict[str, Any]]:
    """Archive multiple metric snapshots to Amazon S3.

    Parameters
    ----------
    snapshots : list[dict]
        Each dict must have keys: "series_list", "metric_name", optionally "prefix".
    bucket : str
        S3 bucket name.
    aws_access_key_id : str, optional
        AWS access key.
    aws_secret_access_key : str, optional
        AWS secret key.
    aws_region : str
        AWS region.
    storage_class : str
        S3 storage class.

    Returns
    -------
    list[dict]
        Upload results for each snapshot.
    """
    results = []
    for snap in snapshots:
        result = archive_metric_snapshot(
            series_list=snap["series_list"],
            bucket=bucket,
            metric_name=snap["metric_name"],
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_region=aws_region,
            storage_class=storage_class,
            prefix=snap.get("prefix"),
        )
        results.append(result)

    return results


def _build_snapshot_payload(
    series_list: List[MetricSeries],
    metric_name: str,
) -> bytes:
    """Serialize metric series data into a JSON payload for archiving."""
    snapshot = {
        "metric_name": metric_name,
        "captured_at": datetime.utcnow().isoformat(),
        "series_count": len(series_list),
        "series": [],
    }

    for series in series_list:
        stats = compute_series_stats(series)
        series_data = {
            "metric_type": series.metric_type,
            "resource_labels": series.resource_labels,
            "stats": stats,
            "points": [
                {
                    "timestamp": p.timestamp.isoformat(),
                    "value": p.value,
                    "labels": p.labels,
                }
                for p in series.points
            ],
        }
        snapshot["series"].append(series_data)

    return json.dumps(snapshot, default=str).encode("utf-8")


def _gzip_compress(data: bytes) -> bytes:
    """Gzip-compress a byte payload."""
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb") as gz:
        gz.write(data)
    return buf.getvalue()


if __name__ == "__main__":
    sample_series = MetricSeries(
        metric_type="cpu/utilization",
        resource_labels={"instance_id": "vm-001"},
        points=[],
    )
    result = archive_metric_snapshot(
        series_list=[sample_series],
        bucket="my-metrics-archive",
        metric_name="cpu-utilization",
    )
    print(f"Archived to s3://{result['bucket']}/{result['key']}")
