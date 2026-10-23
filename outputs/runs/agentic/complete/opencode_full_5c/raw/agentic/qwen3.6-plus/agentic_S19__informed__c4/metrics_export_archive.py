import os
import json
import time
import gzip
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from observability_models import (
    MetricsExportRequest,
    MetricsExportResponse,
    Datapoint,
)


def get_s3_client() -> boto3.client:
    aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    if not aws_access_key or not aws_secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables are required for Amazon S3"
        )
    return boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
    )


def archive_metric_snapshot(request: MetricsExportRequest) -> MetricsExportResponse:
    s3_client = get_s3_client()
    snapshot_payload = {
        "metric_name": request.metric_name,
        "export_timestamp": request.export_timestamp,
        "datapoints": [
            {"timestamp": dp.timestamp, "value": dp.value, "dimensions": dp.dimensions}
            for dp in request.snapshot_data
        ],
        "total_points": len(request.snapshot_data),
    }
    json_bytes = json.dumps(snapshot_payload, indent=2).encode("utf-8")
    compressed = gzip.compress(json_bytes)
    timestamp_str = time.strftime(
        "%Y%m%dT%H%M%SZ", time.gmtime(request.export_timestamp)
    )
    object_key = (
        f"{request.object_key_prefix}/{request.metric_name}/{timestamp_str}.json.gz"
    )
    try:
        s3_client.put_object(
            Bucket=request.bucket_name,
            Key=object_key,
            Body=compressed,
            ContentType="application/gzip",
            Metadata={
                "metric-name": request.metric_name,
                "export-timestamp": str(request.export_timestamp),
                "datapoint-count": str(len(request.snapshot_data)),
            },
        )
    except ClientError as e:
        return MetricsExportResponse(
            bucket_name=request.bucket_name,
            object_key=object_key,
            export_timestamp=request.export_timestamp,
            size_bytes=len(compressed),
            status="error",
        )
    return MetricsExportResponse(
        bucket_name=request.bucket_name,
        object_key=object_key,
        export_timestamp=request.export_timestamp,
        size_bytes=len(compressed),
        status="ok",
    )


if __name__ == "__main__":
    sample_data = [
        Datapoint(timestamp=int(time.time()) - i * 60, value=50.0 + i * 0.5)
        for i in range(100)
    ]
    req = MetricsExportRequest(
        metric_name="system.cpu.user",
        snapshot_data=sample_data,
        export_timestamp=int(time.time()),
        bucket_name=os.environ.get("S3_BUCKET_NAME", "metrics-archive"),
        object_key_prefix="metrics/snapshots",
    )
    result = archive_metric_snapshot(req)
    print(f"Status: {result.status}")
    print(f"Object key: {result.object_key}")
    print(f"Size: {result.size_bytes} bytes")
