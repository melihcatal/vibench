import boto3
import os
from botocore.exceptions import ClientError
from storage_client import get_s3_client


def upload_object(
    bucket_name, object_key, file_path=None, data_bytes=None, content_type=None
):
    """
    Upload a file or byte stream to Amazon S3.

    Args:
        bucket_name: S3 bucket name
        object_key: Object key (path) in S3
        file_path: Path to local file (optional if data_bytes provided)
        data_bytes: Bytes data to upload (optional if file_path provided)
        content_type: MIME type of the content

    Returns:
        dict: Upload result with bucket, key, and etag
    """
    s3_client = get_s3_client()

    extra_args = {}
    if content_type:
        extra_args["ContentType"] = content_type

    try:
        if file_path:
            with open(file_path, "rb") as f:
                response = s3_client.put_object(
                    Bucket=bucket_name, Key=object_key, Body=f, **extra_args
                )
        elif data_bytes:
            response = s3_client.put_object(
                Bucket=bucket_name, Key=object_key, Body=data_bytes, **extra_args
            )
        else:
            raise ValueError("Either file_path or data_bytes must be provided")

        return {
            "bucket": bucket_name,
            "key": object_key,
            "etag": response["ETag"],
            "provider": "Amazon S3",
        }
    except ClientError as e:
        raise Exception(f"Failed to upload object to Amazon S3: {e}")
