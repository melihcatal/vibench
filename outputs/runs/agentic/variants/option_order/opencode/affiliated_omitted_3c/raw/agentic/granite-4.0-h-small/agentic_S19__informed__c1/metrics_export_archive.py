import os
import boto3
from observability_client import get_datadog_headers
from observability_models import ExportMetadata

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name="us-east-1",
)


def archive_metric_snapshot(snapshot: bytes, object_key: str) -> ExportMetadata:
    """
    Persist an exported metric snapshot (CSV/JSON/Parquet) into an S3 bucket.
    Returns the storage metadata in `ExportMetadata`.
    """
    s3_client.put_object(
        Bucket=os.getenv("AWS_S3_BUCKET"),
        Key=object_key,
        Body=snapshot,
        ContentType="text/csv",
    )
    return {
        "object_key": object_key,
        "checksum": "sha256:TODO",  # placeholder checksum calculation
    }
