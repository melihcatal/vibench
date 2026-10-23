import boto3
import os
from botocore.exceptions import ClientError
from storage_client import get_s3_client


def list_objects_with_prefix(bucket_name, prefix="", max_keys=1000):
    """
    List stored objects under an S3 bucket or container prefix.

    Args:
        bucket_name: S3 bucket name
        prefix: Prefix to filter objects (default empty string)
        max_keys: Maximum number of objects to return (default 1000)

    Returns:
        dict: List of objects and metadata
    """
    s3_client = get_s3_client()

    try:
        paginator = s3_client.get_paginator("list_objects_v2")

        objects = []
        common_prefixes = []

        # Paginate through results
        for page in paginator.paginate(
            Bucket=bucket_name, Prefix=prefix, PaginationConfig={"MaxItems": max_keys}
        ):
            # Add objects
            if "Contents" in page:
                for obj in page["Contents"]:
                    objects.append(
                        {
                            "key": obj["Key"],
                            "size": obj["Size"],
                            "last_modified": obj["LastModified"],
                            "etag": obj["ETag"],
                            "storage_class": obj.get("StorageClass", "STANDARD"),
                        }
                    )

            # Add common prefixes (subdirectories)
            if "CommonPrefixes" in page:
                for prefix_obj in page["CommonPrefixes"]:
                    common_prefixes.append(prefix_obj["Prefix"])

        return {
            "success": True,
            "bucket": bucket_name,
            "prefix": prefix,
            "objects": objects,
            "common_prefixes": common_prefixes,
            "object_count": len(objects),
            "prefix_count": len(common_prefixes),
            "provider": "Amazon S3",
        }

    except ClientError as e:
        return {"success": False, "error": str(e), "provider": "Amazon S3"}
    except Exception as e:
        return {"success": False, "error": str(e), "provider": "Amazon S3"}
