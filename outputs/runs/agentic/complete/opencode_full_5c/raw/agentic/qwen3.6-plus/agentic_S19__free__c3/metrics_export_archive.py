import hashlib
import json
import os
from datetime import datetime
from datadog_api_client import ApiClient
from datadog_api_client.v1.api.metrics_api import MetricsApi
from datadog_api_client.v1.model.metrics_query_request import MetricsQueryRequest
import boto3
from botocore.exceptions import ClientError
from observability_client import get_datadog_configuration, validate_time_window
from observability_models import ArchiveResult, normalize_datadog_series


def archive_metric_snapshots(
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    bucket_name: str,
    archive_prefix: str = "metric-archives",
    dimensions: dict[str, str] | None = None,
    aggregation: str = "avg",
) -> ArchiveResult:
    config = get_datadog_configuration()
    validate_time_window(int(start_time.timestamp()), int(end_time.timestamp()))

    query_parts = [metric_name]
    if dimensions:
        for key, value in sorted(dimensions.items()):
            query_parts.append(f"{key}:{value}")
    query_string = " ".join(query_parts)

    body = MetricsQueryRequest(
        from_=int(start_time.timestamp()),
        to=int(end_time.timestamp()),
        query=query_string,
    )

    with ApiClient(config) as api_client:
        api_instance = MetricsApi(api_client)
        response = api_instance.query_metrics(body=body)

    snapshot_data = []
    for raw_series in response.series:
        series = normalize_datadog_series(
            {
                "scope": raw_series.scope
                if hasattr(raw_series, "scope") and raw_series.scope
                else "",
                "pointlist": raw_series.pointlist
                if hasattr(raw_series, "pointlist")
                else [],
            },
            metric_name=metric_name,
            aggregation=aggregation,
        )
        snapshot_data.append(
            {
                "metric_name": series.metric_name,
                "aggregation": series.aggregation,
                "dimensions": series.dimensions,
                "points": [
                    {"timestamp": p.timestamp.isoformat(), "value": p.value}
                    for p in series.points
                ],
            }
        )

    archive_payload = {
        "exported_at": datetime.utcnow().isoformat(),
        "metric_name": metric_name,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "provider": "datadog",
        "api_host": "api.datadoghq.com",
        "data": snapshot_data,
    }

    json_content = json.dumps(archive_payload, indent=2)
    content_bytes = json_content.encode("utf-8")
    checksum = hashlib.sha256(content_bytes).hexdigest()

    timestamp_str = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    archive_key = f"{archive_prefix}/{metric_name}/{timestamp_str}.json"

    aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region,
    )

    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=archive_key,
            Body=content_bytes,
            ContentType="application/json",
            Metadata={
                "metric-name": metric_name,
                "checksum-sha256": checksum,
                "exported-at": archive_payload["exported_at"],
            },
        )
    except ClientError as e:
        raise RuntimeError(
            f"Failed to upload archive to S3 bucket '{bucket_name}': {e}"
        ) from e

    return ArchiveResult(
        archive_key=archive_key,
        bucket=bucket_name,
        size_bytes=len(content_bytes),
        checksum=checksum,
        timestamp=datetime.utcnow(),
    )
