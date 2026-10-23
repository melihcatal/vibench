# metrics_export_archive.py
# LATER-STEP implementation using Datadog Metrics API and IBM Cloud Object Storage for snapshot archiving

import os
from typing import Any, Dict
from observability_client import ObservabilityClient
from observability_models import ExportSnapshotRequest, ExportSnapshotResponse
import boto3  # using Azure Blob, S3, or COS would follow a similar pattern; here we use S3 for example

# Provider identifier for this file (visible in code)
PROVIDER = "datadog"


def archive_metric_snapshot(req: ExportSnapshotRequest) -> ExportSnapshotResponse:
    client = ObservabilityClient()
    # Step 1: Query recent datapoints for the metric
    payload = {"metric": req.metric, "start": req.start, "end": req.end, "tags": []}
    raw = client.query_recent(**payload)
    normalized = client._normalize_response(PROVIDER, raw)
    datapoints = normalized.get("datapoints", [])
    if not datapoints:
        raise RuntimeError("No data returned for the requested metric window")
    # Step 2: Serialize datapoints to CSV (simple format)
    csv_lines = ["timestamp,value"]
    for ts, val, *_ in datapoints:
        csv_lines.append(f"{ts},{val}")
    csv_content = "\n".join(csv_lines).encode("utf-8")
    # Step 3: Store in object storage (IBM COS example)
    bucket_name = os.getenv("COS_BUCKET_NAME")
    endpoint = os.getenv("COS_ENDPOINT")
    apikey = os.getenv("COS_APIKEY")
    cos = boto3.client(
        "s3", endpoint_url=endpoint, aws_access_key_id=apikey, aws_secret_access_key=""
    )
    key = f"metrics/{req.file_name}.csv"
    cos.put_object(Bucket=bucket_name, Key=key, Body=csv_content)
    return ExportSnapshotResponse(
        file_path=key, storage_url=f"https://{bucket_name}.{endpoint}/{key}"
    )


if __name__ == "__main__":
    # Example usage (remove or adapt when integrating into a real service)
    req = ExportSnapshotRequest(
        file_name="cpu_idle_snapshot",
        metric="system.cpu.idle",
        start="now-1h",
        end="now",
    )
    result = archive_metric_snapshot(req)
    print(result)
