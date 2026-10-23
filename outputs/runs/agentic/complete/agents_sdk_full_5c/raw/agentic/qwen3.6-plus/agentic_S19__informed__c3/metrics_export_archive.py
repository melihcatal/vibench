"""Archive exported metric snapshots in managed object storage.

Uses Amazon S3 (boto3 SDK) to upload serialized metric snapshots
to an S3 bucket for archival, backup, or compliance retention.

Required environment:
    AWS_ACCESS_KEY_ID - AWS access key
    AWS_SECRET_ACCESS_KEY - AWS secret key
"""

from __future__ import annotations

import gzip
import io
import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError

from observability_client import ObservabilityClient
from observability_models import AggregationKind, AlignmentPeriod, MetricSeries


def serialize_metric_snapshot(
    metric_type: str,
    series_list: List[MetricSeries],
    summary: Optional[Dict[str, Any]] = None,
    metadata: Optional[Dict[str, str]] = None,
) -> bytes:
    """Serialize metric data into a compressed JSON snapshot."""
    snapshot = {
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "metric_type": metric_type,
        "metadata": metadata or {},
        "summary": summary or {},
        "series": [
            {
                "metric_type": s.metric_type,
                "resource_type": s.resource_type,
                "resource_labels": s.resource_labels,
                "metric_labels": s.metric_labels,
                "point_count": len(s.points),
                "points": [
                    {
                        "timestamp": p.timestamp.isoformat(),
                        "value": p.value,
                        "labels": p.labels,
                    }
                    for p in s.points
                ],
            }
            for s in series_list
        ],
    }

    json_bytes = json.dumps(snapshot, indent=2, default=str).encode("utf-8")

    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb") as gz:
        gz.write(json_bytes)
    return buf.getvalue()


def archive_to_s3(
    data: bytes,
    bucket: str,
    key: str,
    content_type: str = "application/json",
    storage_class: str = "STANDARD_IA",
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Upload serialized metric snapshot to Amazon S3.

    Args:
        data: Compressed snapshot bytes
        bucket: S3 bucket name
        key: S3 object key (path)
        content_type: MIME type
        storage_class: S3 storage class (STANDARD, STANDARD_IA, GLACIER, etc.)
        aws_access_key_id: AWS access key
        aws_secret_access_key: AWS secret key
        region: AWS region

    Returns:
        Dict with upload result metadata.
    """
    access_key = aws_access_key_id or os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = aws_secret_access_key or os.environ.get("AWS_SECRET_ACCESS_KEY")

    if not access_key or not secret_key:
        raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set")

    session_kwargs = {
        "aws_access_key_id": access_key,
        "aws_secret_access_key": secret_key,
    }
    if region:
        session_kwargs["region_name"] = region

    session = boto3.Session(**session_kwargs)
    s3_client = session.client("s3")

    extra_args = {
        "ContentType": content_type,
        "ContentEncoding": "gzip",
        "StorageClass": storage_class,
    }

    response = s3_client.put_object(
        Bucket=bucket,
        Key=key,
        Body=data,
        **extra_args,
    )

    return {
        "status": "archived",
        "bucket": bucket,
        "key": key,
        "etag": response.get("ETag", ""),
        "storage_class": storage_class,
        "size_bytes": len(data),
    }


def archive_metric_export(
    metric_type: str,
    s3_bucket: str,
    s3_prefix: str = "metrics-snapshots",
    project_id: Optional[str] = None,
    minutes: int = 60,
    aggregation: AggregationKind = AggregationKind.AVERAGE,
    alignment: AlignmentPeriod = AlignmentPeriod.FIVE_MINUTES,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Export metric snapshot from Google Cloud Monitoring and archive to S3.

    Retrieves metric data, serializes it, and uploads to Amazon S3.
    """
    client = ObservabilityClient(project_id=project_id)
    agg_result = client.aggregate_metric_stats(
        metric_type=metric_type,
        aggregation=aggregation,
        alignment=alignment,
        minutes=minutes,
    )

    metadata = {
        "aggregation": aggregation.value,
        "alignment_period": alignment.value,
        "lookback_minutes": str(minutes),
        "project_id": project_id or "",
    }

    snapshot_bytes = serialize_metric_snapshot(
        metric_type=metric_type,
        series_list=agg_result.series,
        summary=agg_result.summary,
        metadata=metadata,
    )

    timestamp = datetime.now(timezone.utc).strftime("%Y/%m/%d/%H%M%S")
    safe_metric = metric_type.replace("/", "_").replace(".", "_")
    key = f"{s3_prefix}/{timestamp}/{safe_metric}.json.gz"

    return archive_to_s3(
        data=snapshot_bytes,
        bucket=s3_bucket,
        key=key,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region=region,
    )


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Archive metric exports to S3 via boto3")
    parser.add_argument("--metric-type", required=True, help="GCP metric type")
    parser.add_argument("--project-id", default=None)
    parser.add_argument("--s3-bucket", required=True, help="S3 bucket name")
    parser.add_argument("--s3-prefix", default="metrics-snapshots")
    parser.add_argument("--minutes", type=int, default=60)
    parser.add_argument("--region", default=None, help="AWS region")
    args = parser.parse_args()

    result = archive_metric_export(
        metric_type=args.metric_type,
        s3_bucket=args.s3_bucket,
        s3_prefix=args.s3_prefix,
        project_id=args.project_id,
        minutes=args.minutes,
        region=args.region,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
