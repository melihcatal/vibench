import boto3
import os
from botocore.exceptions import ClientError
from storage_client import get_s3_client


def upload_object(
    bucket_name: str, object_key: str, file_path: str = None, data: bytes = None
) -> dict:
    """
    Upload a file or byte stream to Amazon S3.

    Args:
        bucket_name: S3 bucket name
        object_key: Object key (path) in S3
        file_path: Path to local file (optional if data is provided)
        data: Bytes data to upload (optional if file_path is provided)

    Returns:
        Dictionary with upload result including ETag and version ID
    """
    s3_client = get_s3_client()

    try:
        if file_path:
            with open(file_path, "rb") as file:
                response = s3_client.put_object(
                    Bucket=bucket_name, Key=object_key, Body=file
                )
        elif data:
            response = s3_client.put_object(
                Bucket=bucket_name, Key=object_key, Body=data
            )
        else:
            raise ValueError("Either file_path or data must be provided")

        return {
            "etag": response.get("ETag", "").strip('"'),
            "version_id": response.get("VersionId"),
            "bucket": bucket_name,
            "key": object_key,
        }
    except ClientError as e:
        raise Exception(f"S3 upload failed: {e}")
