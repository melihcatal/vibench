# upload_object.py
# Uploads a file or byte stream to Managed Object Storage (Amazon S3 example)

import os
import boto3
from botocore.exceptions import ClientError
from storage_client import get_s3_client
from storage_models import UploadObjectRequest


def upload_object(request: UploadObjectRequest) -> None:
    """Upload `request.body` to S3 bucket/key using environment credentials."""
    client = get_s3_client()
    try:
        client.upload_fileobj(
            request.body,  # can be a file-like object or BytesIO
            request.bucket,
            request.key,
        )
    except ClientError as exc:
        raise RuntimeError(f"S3 upload failed: {exc}") from exc

    print(f"Uploaded {request.key} to s3://{request.bucket}/")


# Example usage (not executed here):
# upload_object(UploadObjectRequest(bucket="my-bucket", key="path/file.txt",
#                                 body=open('local.txt', 'rb')))
