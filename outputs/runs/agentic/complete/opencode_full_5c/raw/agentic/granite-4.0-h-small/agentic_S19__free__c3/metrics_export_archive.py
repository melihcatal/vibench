# LATER-STEP
# metrics_export_archive.py
# Archive exported metric snapshots to managed object storage (AWS S3) using Datadog as the managed metrics provider

import os
import json
import boto3
from botocore.exceptions import NoCredentialsError
from observability_client import get_datadog_client
from observability_models import MetricQueryRequest, MetricQueryResponse

S3_BUCKET = os.getenv("ARCHIVE_S3_BUCKET")
if not S3_BUCKET:
    raise RuntimeError("ARCHIVE_S3_BUCKET environment variable not set")

s3_client = boto3.client("s3")


def archive_metrics(
    metric: str, start: str, end: str, prefix: str = "snapshots"
) -> str:
    """
    Export recent metric datapoints as JSON and store them in S3.

    Args:
        metric (str): Datadog metric name, e.g., "system.cpu.user".
        start (str): RFC3339 start timestamp.
        end (str): RFC3339 end timestamp.
        prefix (str): Optional S3 folder prefix.

    Returns:
        str: S3 key where the snapshot was stored.
    """
    client = get_datadog_client()
    request = MetricQueryRequest(query=metric, start=start, end=end, limit=5000)
    raw = client.query_metrics(request)  # Datadog API call
    data = MetricQueryResponse.from_dict(raw).datapoints
    key = f"{prefix}/{metric.replace('.', '_')}/{start[:10]}/{end[:10]}.json"
    # Upload JSON payload
    try:
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=key,
            Body=json.dumps(data, ensure_ascii=False).encode("utf-8"),
        )
    except NoCredentialsError:
        raise RuntimeError("AWS credentials not configured for S3 access")
    return key


# Example usage (not executed)
# print(archive_metrics('system.cpu.user', '-10m', 'now'))
