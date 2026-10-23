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
        object_key: Object key (path) in the bucket
        file_path: Path to local file (optional if data is provided)
        data: Byte data to upload (optional if file_path is provided)

    Returns:
        Dictionary with upload result including ETag
    """
    s3_client = get_s3_client()

    try:
        if file_path:
            with open(file_path, "rb") as file:
                response = s3_client.upload_fileobj(file, bucket_name, object_key)
                # upload_fileobj doesn't return response, need to head object
                head_response = s3_client.head_object(
                    Bucket=bucket_name, Key=object_key
                )
                return {
                    "success": True,
                    "bucket": bucket_name,
                    "key": object_key,
                    "etag": head_response.get("ETag", ""),
                    "size": head_response.get("ContentLength", 0),
                }
        elif data is not None:
            response = s3_client.put_object(
                Bucket=bucket_name, Key=object_key, Body=data
            )
            return {
                "success": True,
                "bucket": bucket_name,
                "key": object_key,
                "etag": response.get("ETag", ""),
                "size": len(data),
            }
        else:
            raise ValueError("Either file_path or data must be provided")

    except ClientError as e:
        return {
            "success": False,
            "error": str(e),
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
