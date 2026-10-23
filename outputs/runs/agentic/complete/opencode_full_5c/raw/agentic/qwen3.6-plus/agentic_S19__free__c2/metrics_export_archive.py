from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError

from observability_client import ObservabilityClient, create_client
from observability_models import (
    MetricExportSnapshot,
    MetricTimeSeries,
    normalize_datadog_series,
)

AWS_S3_REGION = "us-east-1"
ENV_AWS_ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID"
ENV_AWS_SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY"
ENV_AWS_DEFAULT_REGION = "AWS_DEFAULT_REGION"


def metrics_export_archive(
    metric_name: str,
    start: int,
    end: int,
    bucket_name: str,
    s3_prefix: str = "metric-snapshots",
    tags: Optional[List[str]] = None,
    interval: Optional[int] = None,
    client: Optional[ObservabilityClient] = None,
    s3_client: Optional[boto3.client] = None,
    region: Optional[str] = None,
) -> MetricExportSnapshot:
    if client is None:
        client = create_client()

    tag_filter = ""
    if tags:
        tag_filter = "{" + ",".join(tags) + "}"
    query_str = f"{metric_name}{tag_filter}"

    params = {
        "from": start,
        "to": end,
        "query": query_str,
    }
    if interval is not None:
        params["interval"] = interval

    response = client.query_metrics_v1(
        query=query_str,
        start=start,
        end=end,
        interval=interval,
    )

    series_list = []
    for raw_series in response.get("series", []):
        series_list.append(normalize_datadog_series(raw_series, metric_name))

    export_timestamp = int(datetime.now(timezone.utc).timestamp())
    snapshot_id = str(uuid.uuid4())

    snapshot_data = {
        "snapshot_id": snapshot_id,
        "metric_name": metric_name,
        "start": start,
        "end": end,
        "export_timestamp": export_timestamp,
        "query": query_str,
        "series": [],
    }

    for series in series_list:
        series_data = {
            "metric_name": series.metric_name,
            "scope": series.scope,
            "tag_set": series.tag_set,
            "expression": series.expression,
            "unit": series.unit,
            "point_count": len(series.points),
            "points": [
                {"timestamp": p.timestamp, "value": p.value, "tags": p.tags}
                for p in series.points
            ],
        }
        snapshot_data["series"].append(series_data)

    if s3_client is None:
        region = region or os.environ.get(ENV_AWS_DEFAULT_REGION, AWS_S3_REGION)
        s3_client = boto3.client("s3", region_name=region)

    object_key = _build_s3_key(s3_prefix, metric_name, snapshot_id, export_timestamp)

    s3_client.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=json.dumps(snapshot_data, indent=2).encode("utf-8"),
        ContentType="application/json",
        Metadata={
            "metric-name": metric_name,
            "snapshot-id": snapshot_id,
            "export-timestamp": str(export_timestamp),
            "time-window-start": str(start),
            "time-window-end": str(end),
        },
    )

    storage_uri = f"s3://{bucket_name}/{object_key}"

    return MetricExportSnapshot(
        snapshot_id=snapshot_id,
        metric_name=metric_name,
        start=start,
        end=end,
        data=snapshot_data,
        series_list=series_list,
        export_timestamp=export_timestamp,
        storage_key=object_key,
        storage_uri=storage_uri,
        storage_provider="aws-s3",
    )


def archive_metric_snapshots_batch(
    snapshots: List[Dict[str, Any]],
    bucket_name: str,
    s3_prefix: str = "metric-snapshots",
    s3_client: Optional[boto3.client] = None,
    region: Optional[str] = None,
) -> List[MetricExportSnapshot]:
    if s3_client is None:
        region = region or os.environ.get(ENV_AWS_DEFAULT_REGION, AWS_S3_REGION)
        s3_client = boto3.client("s3", region_name=region)

    results = []
    for snapshot_data in snapshots:
        export_timestamp = int(datetime.now(timezone.utc).timestamp())
        snapshot_id = str(uuid.uuid4())
        metric_name = snapshot_data.get("metric_name", "unknown")

        snapshot_data["snapshot_id"] = snapshot_id
        snapshot_data["export_timestamp"] = export_timestamp

        object_key = _build_s3_key(
            s3_prefix, metric_name, snapshot_id, export_timestamp
        )

        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=json.dumps(snapshot_data, indent=2).encode("utf-8"),
            ContentType="application/json",
        )

        storage_uri = f"s3://{bucket_name}/{object_key}"

        results.append(
            MetricExportSnapshot(
                snapshot_id=snapshot_id,
                metric_name=metric_name,
                start=snapshot_data.get("start", 0),
                end=snapshot_data.get("end", 0),
                data=snapshot_data,
                export_timestamp=export_timestamp,
                storage_key=object_key,
                storage_uri=storage_uri,
                storage_provider="aws-s3",
            )
        )

    return results


def _build_s3_key(
    s3_prefix: str, metric_name: str, snapshot_id: str, timestamp: int
) -> str:
    date_str = datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y/%m/%d")
    sanitized_metric = metric_name.replace(".", "_").replace(":", "_")
    return f"{s3_prefix}/{date_str}/{sanitized_metric}/{snapshot_id}.json"
