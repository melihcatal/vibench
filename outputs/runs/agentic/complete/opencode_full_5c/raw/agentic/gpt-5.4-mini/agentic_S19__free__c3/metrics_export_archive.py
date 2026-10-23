import json
import boto3
from observability_models import MetricsExportRequest


def metrics_export_archive(request: MetricsExportRequest):
    client = boto3.client("s3", region_name="us-east-1")
    body = json.dumps(request.payload).encode("utf-8")
    client.put_object(Bucket=request.bucket, Key=request.object_name, Body=body)
    return {
        "bucket": request.bucket,
        "object_name": request.object_name,
        "archived": True,
    }
