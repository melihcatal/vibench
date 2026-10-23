import boto3
import os
from botocore.exceptions import ClientError
from storage_client import get_s3_client


def get_object_metadata(bucket_name, object_key):
    """
    Read object metadata or head information from Amazon S3.

    Args:
        bucket_name: S3 bucket name
        object_key: Object key (path) in S3

    Returns:
        dict: Object metadata including size, content type, last modified, etc.
    """
    s3_client = get_s3_client()

    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=object_key)

        metadata = {
            "bucket": bucket_name,
            "key": object_key,
            "size": response["ContentLength"],
            "content_type": response.get("ContentType"),
            "last_modified": response["LastModified"].isoformat(),
            "etag": response["ETag"],
            "metadata": response.get("Metadata", {}),
            "provider": "Amazon S3",
        }

        if "ContentEncoding" in response:
            metadata["content_encoding"] = response["ContentEncoding"]
        if "CacheControl" in response:
            metadata["cache_control"] = response["CacheControl"]

        return metadata
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            raise Exception(
                f"Object not found in Amazon S3: {bucket_name}/{object_key}"
            )
        raise Exception(f"Failed to get object metadata from Amazon S3: {e}")
