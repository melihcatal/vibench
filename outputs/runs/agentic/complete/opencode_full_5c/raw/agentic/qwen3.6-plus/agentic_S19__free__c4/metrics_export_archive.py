import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from observability_client import ObservabilityClient
from observability_models import (
    ArchiveResult,
    MetricDataPoint,
    MetricDimension,
    MetricQueryResponse,
    MetricStatistic,
    normalize_period_to_seconds,
    parse_dimension_string,
)

DEFAULT_S3_BUCKET = "metrics-archive-bucket"
DEFAULT_STORAGE_CLASS = "STANDARD_IA"
DEFAULT_ARCHIVE_PREFIX = "metrics-snapshots"


def metrics_export_archive(
    namespace: str,
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    bucket: str = DEFAULT_S3_BUCKET,
    period_minutes: int = 5,
    dimensions: Optional[List[MetricDimension]] = None,
    statistic: MetricStatistic = MetricStatistic.AVERAGE,
    storage_class: str = DEFAULT_STORAGE_CLASS,
    archive_prefix: str = DEFAULT_ARCHIVE_PREFIX,
    region: Optional[str] = None,
) -> ArchiveResult:
    period_seconds = normalize_period_to_seconds(period_minutes)

    client = ObservabilityClient(region=region)

    response = client.get_metric_data(
        namespace=namespace,
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        period=period_seconds,
        dimensions=dimensions,
        statistics=[statistic],
    )

    archive_data = _build_archive_payload(response)

    timestamp_str = start_time.strftime("%Y%m%dT%H%M%SZ")
    dim_suffix = ""
    if dimensions:
        dim_suffix = "_" + "_".join(f"{d.name}-{d.value}" for d in dimensions)

    s3_key = (
        f"{archive_prefix}/{namespace}/{metric_name}/{timestamp_str}{dim_suffix}.json"
    )

    upload_result = client.upload_to_s3(
        bucket=bucket,
        key=s3_key,
        data=archive_data,
        storage_class=storage_class,
        content_type="application/json",
    )

    return ArchiveResult(
        bucket=upload_result["bucket"],
        key=upload_result["key"],
        etag=upload_result["etag"],
        version_id=upload_result.get("version_id"),
        storage_class=storage_class,
    )


def metrics_export_archive_from_response(
    response: MetricQueryResponse,
    bucket: str = DEFAULT_S3_BUCKET,
    storage_class: str = DEFAULT_STORAGE_CLASS,
    archive_prefix: str = DEFAULT_ARCHIVE_PREFIX,
    region: Optional[str] = None,
) -> ArchiveResult:
    archive_data = _build_archive_payload(response)

    start_time = (
        response.datapoints[0].timestamp
        if response.datapoints
        else datetime.now(timezone.utc)
    )
    timestamp_str = start_time.strftime("%Y%m%dT%H%M%SZ")

    dim_suffix = ""
    if response.dimensions:
        dim_suffix = "_" + "_".join(f"{d.name}-{d.value}" for d in response.dimensions)

    s3_key = (
        f"{archive_prefix}/{response.namespace}/{response.metric_name}/"
        f"{timestamp_str}{dim_suffix}.json"
    )

    client = ObservabilityClient(region=region)

    upload_result = client.upload_to_s3(
        bucket=bucket,
        key=s3_key,
        data=archive_data,
        storage_class=storage_class,
        content_type="application/json",
    )

    return ArchiveResult(
        bucket=upload_result["bucket"],
        key=upload_result["key"],
        etag=upload_result["etag"],
        version_id=upload_result.get("version_id"),
        storage_class=storage_class,
    )


def _build_archive_payload(response: MetricQueryResponse) -> Dict[str, Any]:
    return {
        "export_timestamp": datetime.now(timezone.utc).isoformat(),
        "metric": {
            "namespace": response.namespace,
            "metric_name": response.metric_name,
            "label": response.label,
            "dimensions": [d.to_cloudwatch_dict() for d in response.dimensions],
        },
        "datapoints": [
            {
                "timestamp": dp.timestamp.isoformat(),
                "value": dp.value,
                "unit": dp.unit,
                "statistic": dp.statistic,
            }
            for dp in response.datapoints
        ],
        "datapoint_count": len(response.datapoints),
    }


def format_archive_result(result: ArchiveResult) -> str:
    lines = [
        f"Archive successful",
        f"Bucket: {result.bucket}",
        f"Key: {result.key}",
        f"ETag: {result.etag}",
        f"Storage Class: {result.storage_class}",
    ]
    if result.version_id:
        lines.append(f"Version ID: {result.version_id}")
    return "\n".join(lines)
