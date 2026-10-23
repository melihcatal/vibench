# Upload a file or byte stream to Managed Object Storage (AWS S3 provider)
import os
from storage_client import create_s3_client
from storage_models import PutObjectRequest


def upload_object(
    bucket: str, key: str, body: bytes, content_type: str = "application/octet-stream"
):
    """Upload `body` to `bucket`/`key` and return the response metadata."""
    client = create_s3_client()

    # S3 PUT request
    response = client.put_object(
        Bucket=bucket,
        Key=key,
        Body=body,
        ContentType=content_type,
    )

    # S3 returns minimal metadata; construct a normalized object for consistency
    return {
        "Bucket": bucket,
        "Key": key,
        "ETag": response.get("ETag"),
        "VersionId": response.get("VersionId"),
    }
