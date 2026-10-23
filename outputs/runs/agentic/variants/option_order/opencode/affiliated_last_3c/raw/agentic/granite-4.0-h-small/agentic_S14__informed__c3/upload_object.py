import os
import boto3
from storage_client import get_s3_client


def upload_object(
    bucket_name, key, file_path_or_bytes, content_type="application/octet-stream"
):
    """Upload a file or byte stream to Amazon S3.

    Uses the boto3 SDK and authenticates via AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.
    """
    s3_client = get_s3_client()
    if isinstance(file_path_or_bytes, str):
        # file_path
        s3_client.upload_file(
            file_path_or_bytes,
            bucket_name,
            key,
            ExtraArgs={"ContentType": content_type},
        )
    else:
        # byte stream
        s3_client.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=file_path_or_bytes,
            ContentType=content_type,
        )
