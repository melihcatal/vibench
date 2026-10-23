import boto3
import os
from botocore.exceptions import ClientError
from typing import List, Dict, Any
from storage_client import get_s3_client
from storage_models import ObjectInfo


def list_objects_with_prefix(
    bucket_name: str, prefix: str = "", max_keys: int = 1000
) -> List[ObjectInfo]:
    """
    List stored objects under a bucket prefix in Amazon S3.

    Args:
        bucket_name: S3 bucket name
        prefix: Prefix to filter objects (default: empty string for all objects)
        max_keys: Maximum number of objects to return (default: 1000)

    Returns:
        List of ObjectInfo objects
    """
    s3_client = get_s3_client()

    objects = []
    continuation_token = None

    try:
        while True:
            list_kwargs = {
                "Bucket": bucket_name,
                "Prefix": prefix,
                "MaxKeys": min(max_keys - len(objects), 1000) if max_keys else 1000,
            }

            if continuation_token:
                list_kwargs["ContinuationToken"] = continuation_token

            response = s3_client.list_objects_v2(**list_kwargs)

            if "Contents" in response:
                for obj in response["Contents"]:
                    object_info = ObjectInfo(
                        key=obj["Key"],
                        size=obj["Size"],
                        last_modified=obj["LastModified"],
                        etag=obj["ETag"].strip('"'),
                        storage_class=obj.get("StorageClass", "STANDARD"),
                    )
                    objects.append(object_info)

            if not response.get("IsTruncated") or (
                max_keys and len(objects) >= max_keys
            ):
                break

            continuation_token = response.get("NextContinuationToken")

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "NoSuchBucket":
            raise FileNotFoundError(f"Bucket {bucket_name} not found")
        elif error_code == "AccessDenied":
            raise PermissionError(f"Access denied to bucket {bucket_name}")
        else:
            raise Exception(f"S3 error: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error: {e}")

    return objects


def list_common_prefixes(
    bucket_name: str, prefix: str = "", delimiter: str = "/"
) -> List[str]:
    """
    List common prefixes (folders) under a bucket prefix.

    Args:
        bucket_name: S3 bucket name
        prefix: Prefix to filter (default: empty string)
        delimiter: Delimiter for common prefixes (default: '/')

    Returns:
        List of common prefix strings
    """
    s3_client = get_s3_client()

    prefixes = []
    continuation_token = None

    try:
        while True:
            list_kwargs = {
                "Bucket": bucket_name,
                "Prefix": prefix,
                "Delimiter": delimiter,
            }

            if continuation_token:
                list_kwargs["ContinuationToken"] = continuation_token

            response = s3_client.list_objects_v2(**list_kwargs)

            if "CommonPrefixes" in response:
                for prefix_obj in response["CommonPrefixes"]:
                    prefixes.append(prefix_obj["Prefix"])

            if not response.get("IsTruncated"):
                break

            continuation_token = response.get("NextContinuationToken")

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "NoSuchBucket":
            raise FileNotFoundError(f"Bucket {bucket_name} not found")
        elif error_code == "AccessDenied":
            raise PermissionError(f"Access denied to bucket {bucket_name}")
        else:
            raise Exception(f"S3 error: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error: {e}")

    return prefixes
