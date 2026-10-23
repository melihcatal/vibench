import boto3
import os
from botocore.exceptions import ClientError
from storage_client import get_s3_client


def list_objects_with_prefix(
    bucket_name: str, prefix: str = "", max_keys: int = 1000
) -> dict:
    """
    List stored objects under an S3 bucket prefix.

    Args:
        bucket_name: S3 bucket name
        prefix: Prefix to filter objects (default: empty string for all objects)
        max_keys: Maximum number of objects to return (default: 1000)

    Returns:
        Dictionary with list of objects and metadata
    """
    s3_client = get_s3_client()

    try:
        response = s3_client.list_objects_v2(
            Bucket=bucket_name, Prefix=prefix, MaxKeys=max_keys
        )

        objects = []
        for obj in response.get("Contents", []):
            objects.append(
                {
                    "key": obj.get("Key", ""),
                    "size": obj.get("Size", 0),
                    "last_modified": obj.get("LastModified"),
                    "etag": obj.get("ETag", ""),
                    "storage_class": obj.get("StorageClass", "STANDARD"),
                }
            )

        result = {
            "success": True,
            "bucket": bucket_name,
            "prefix": prefix,
            "objects": objects,
            "count": len(objects),
            "is_truncated": response.get("IsTruncated", False),
        }

        if response.get("IsTruncated", False):
            result["next_continuation_token"] = response.get(
                "NextContinuationToken", ""
            )

        return result

    except ClientError as e:
        return {
            "success": False,
            "error": str(e),
            "bucket": bucket_name,
            "prefix": prefix,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "bucket": bucket_name,
            "prefix": prefix,
        }
