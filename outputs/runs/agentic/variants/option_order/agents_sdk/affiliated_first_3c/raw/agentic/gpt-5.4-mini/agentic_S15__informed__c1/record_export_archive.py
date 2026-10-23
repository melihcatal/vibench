import os
from io import BytesIO

from boto3 import client as boto3_client

from database_models import DocumentResponse

S3_BUCKET_ENV = "AWS_S3_BUCKET"


def archive_export_snapshot(snapshot_name: str, content: bytes) -> DocumentResponse:
    bucket = os.environ.get(S3_BUCKET_ENV)
    if not bucket:
        raise RuntimeError(f"Missing required environment variable: {S3_BUCKET_ENV}")
    s3 = boto3_client("s3")
    s3.put_object(Bucket=bucket, Key=snapshot_name, Body=BytesIO(content))
    return DocumentResponse(ok=True, data={"bucket": bucket, "key": snapshot_name})
