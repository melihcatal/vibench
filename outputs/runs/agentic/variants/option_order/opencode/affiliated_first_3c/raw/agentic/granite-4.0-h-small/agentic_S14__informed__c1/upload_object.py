# upload_object.py
# [SAME-SCENARIO] Uploads file or byte stream to Managed Object Storage (Amazon S3 example)

import os
import boto3
from storage_client import create_s3_client
from storage_models import UploadResult


# Configuration - expects AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION env vars
def upload_object(
    bucket: str, key: str, data: bytes, content_type: str = "application/octet-stream"
) -> UploadResult:
    """Uploads raw bytes to the specified bucket/key and returns normalized result.
    Args:
        bucket (str): Target bucket name.
        key (str): Object key/path.
        data (bytes): File contents.
        content_type (str): MIME type for the object.
    Returns:
        UploadResult: ETag and optional version ID.
    """
    s3 = create_s3_client()
    response = s3.put_object(
        Bucket=bucket, Key=key, Body=data, ContentType=content_type
    )
    # Normalize response to our model
    return UploadResult(
        etag=response.get("ETag", "").strip('"'), version_id=response.get("VersionId")
    )


# Example usage (uncomment to test)
# result = upload_object('my-bucket', 'example.txt', b'Hello, world!')
# print(result)
