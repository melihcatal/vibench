import boto3
import os
from botocore.exceptions import ClientError
from storage_client import get_s3_client


def get_object_metadata(bucket_name: str, object_key: str) -> dict:
    """
    Read object metadata or head information from Amazon S3.

    Args:
        bucket_name: S3 bucket name
        object_key: Object key (path) in the bucket

    Returns:
        Dictionary with object metadata
    """
    s3_client = get_s3_client()

    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=object_key)

        metadata = {
            "success": True,
            "bucket": bucket_name,
            "key": object_key,
            "etag": response.get("ETag", ""),
            "size": response.get("ContentLength", 0),
            "content_type": response.get("ContentType", ""),
            "last_modified": response.get("LastModified"),
            "storage_class": response.get("StorageClass", "STANDARD"),
            "metadata": response.get("Metadata", {}),
        }

        # Add user metadata if present
        for key, value in response.get("Metadata", {}).items():
            metadata[f"metadata_{key}"] = value

        return metadata

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "Unknown")
        return {
            "success": False,
            "error": str(e),
            "error_code": error_code,
            "bucket": bucket_name,
            "key": object_key,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "bucket": bucket_name,
            "key": object_key,
        }
