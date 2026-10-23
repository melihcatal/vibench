import os
import json
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from local_helpers.observability_client import get_client
from local_helpers.observability_models import MetricQueryRequest, MetricDataResult
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("METRICS_PROVIDER", "AZURE_MONITOR")  # default provider
S3_BUCKET = os.getenv("ARCHIVE_S3_BUCKET")
if not S3_BUCKET:
    raise ValueError("ARCHIVE_S3_BUCKET environment variable must be set")

s3_client = boto3.client("s3")


def export_metric_snapshot(provider, resource_id, metric_name, snapshot_name):
    """
    Pull recent metric data for a given resource/metric, combine it with metadata, and store as a JSON
    object in managed object storage (S3 bucket).
    """
    client = get_client(provider)
    now = datetime.utcnow()
    start = now - timedelta(days=1)  # recent 24‑hour snapshot
    end = now
    # Use the provider client to fetch raw datapoints
    response = client.query_metric_window(
        resource_id, metric_name, start.isoformat(), end.isoformat()
    )
    # Wrap raw response into a reusable model; Azure Monitor returns CompareResult for CompareRequest,
    # but for a simple window we can unpack its internal datapoints.
    datapoints = []
    if provider == "AZURE_MONITOR":
        # Azure CompareResult shape: {'series': [{'datapoints': [...]}]}
        series = response.series if "series" in response else response.get("value", [])
        if isinstance(series, list) and series:
            datapoints = series[0].get("datapoints", [])
        else:
            datapoints = series.get("datapoints", [])
    elif provider == "CLOUDWATCH":
        # AWS CloudWatch shape
        datapoints = response.get("Datapoints", [])
    else:
        raise NotImplementedError(f"export_metrics not implemented for {provider}")

    snapshot = {
        "resource_id": resource_id,
        "metric_name": metric_name,
        "snapshot_name": snapshot_name,
        "retrieved_at_utc": now.isoformat() + "Z",
        "datapoints": datapoints,
    }
    # Store JSON in S3 (overwrites if exists)
    s3_key = f"metric_snapshots/{snapshot_name}.json"
    try:
        s3_client.put_object(
            Bucket=S3_BUCKET, Key=s3_key, Body=json.dumps(snapshot, indent=2)
        )
        return {"status": "ok", "snapshot": snapshot, "s3_key": s3_key}
    except (NoCredentialsError, ClientError) as e:
        raise RuntimeError(f"Failed to write to S3: {e}")


if __name__ == "__main__":
    # Demo usage (remove in production code)
    result = export_metric_snapshot(
        "AZURE_MONITOR", "my-resource-id", "cpuUsage", "cpu-snapshot-2024-01-01"
    )
    print(json.dumps(result, indent=2))
