# [LATER-STEP] metrics_export_archive.py

# Archive exported metric snapshots in managed object storage (Amazon S3 example).
# This script pulls a recent time window of a metric using New Relic, writes the JSON payload
# to a local temporary file, and then uploads it to an S3 bucket.

import os
import json
import boto3
from datetime import datetime, timedelta
from pathlib import Path

from observability_client import NewRelicClient
from observability_models import MetricQueryRequest, MetricQueryResponse

S3_BUCKET = os.getenv("ARCHIVE_S3_BUCKET")
if not S3_BUCKET:
    raise RuntimeError("Environment variable ARCHIVE_S3_BUCKET not set")


def archive_metric_snapshot(
    metric_name: str, window_hours: int = 24, prefix: str = "metrics_export"
) -> Path:
    """
    Export a metric snapshot and store it in S3.

    Args:
        metric_name: Name of the metric (e.g., "cpu.usage.percent").
        window_hours: How far back to fetch data (default last 24h).
        prefix: S3 folder prefix for the object key.

    Returns:
        Path object pointing to the local temporary JSON file (for debugging).
    """
    now = datetime.utcnow()
    start = now - timedelta(hours=window_hours)
    query = MetricQueryRequest(metric=metric_name, start=start, end=now, limit=1000)
    client = NewRelicClient()
    raw: MetricQueryResponse = client.query_metrics(query.__dict__)
    # Normalize to dict suitable for JSON serialization.
    payload = raw.to_dict() if hasattr(raw, "to_dict") else raw
    # Write to a temporary local file.
    tmp_dir = Path("/tmp/metrics_export")
    tmp_dir.mkdir(parents=True, exist_ok=True)
    timestamp = now.strftime("%Y%m%dT%H%M%S")
    local_path = tmp_dir / f"{metric_name}_{timestamp}.json"
    with open(local_path, "w") as fp:
        json.dump(payload, fp, indent=2)
    # Upload to S3.
    s3 = boto3.client("s3")
    s3_key = f"{prefix}/{metric_name}/{timestamp}.json"
    s3.upload_file(str(local_path), S3_BUCKET, s3_key)
    print(f"Archived {metric_name} to s3://{S3_BUCKET}/{s3_key}")
    return local_path


if __name__ == "__main__":
    # Example: archive "request.duration.ms" for the past 48 hours into bucket "my-metrics-archive"
    archive_path = archive_metric_snapshot(
        "request.duration.ms", window_hours=48, prefix="daily_snapshots"
    )
    print("Local copy written to:", archive_path)
