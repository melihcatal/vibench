"""
list_prefix.py - Lists stored objects under a bucket or container prefix.

Uses Amazon S3 via boto3 as the concrete managed object storage provider.
Authentication via AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables.
"""

from typing import Optional, List

from botocore.exceptions import ClientError

from storage_client import get_s3_client, validate_bucket_exists
from storage_models import StorageObjectMetadata, StorageObjectListing, normalize_s3_list_response


def list_objects_by_prefix(
    bucket_name: str,
    prefix: str = "",
    delimiter: Optional[str] = None,
    max_keys: int = 1000,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region_name: Optional[str] = None,
) -> StorageObjectListing:
    """
    List objects in an Amazon S3 bucket under a specified prefix.

    Args:
        bucket_name: S3 bucket to list objects from.
        prefix: Object key prefix to filter results (default: empty string for all).
        delimiter: Optional delimiter for grouping common prefixes (e.g., '/' for folder-like grouping).
        max_keys: Maximum number of keys to return (default: 1000).
        aws_access_key_id: Optional AWS access key ID.
        aws_secret_access_key: Optional AWS secret access key.
        region_name: Optional AWS region name.

    Returns:
        StorageObjectListing with normalized object listing results.

    Raises:
        ValueError: If bucket_name is empty.
        RuntimeError: If the listing operation fails.
    """
    if not bucket_name:
        raise ValueError("bucket_name is required.")

    s3_client = get_s3_client(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
    )

    if not validate_bucket_exists(s3_client, bucket_name):
        raise RuntimeError(f"Bucket '{bucket_name}' does not exist or is not accessible.")

    list_params = {
        "Bucket": bucket_name,
        "Prefix": prefix,
        "MaxKeys": max_keys,
    }

    if delimiter:
        list_params["Delimiter"] = delimiter

    try:
        response = s3_client.list_objects_v2(**list_params)
        return normalize_s3_list_response(
            list_response=response,
            bucket_name=bucket_name,
            prefix=prefix,
        )

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "Unknown")
        raise RuntimeError(
            f"Failed to list objects from S3: {error_code} - {e}"
        ) from e


def list_all_objects_by_prefix(
    bucket_name: str,
    prefix: str = "",
    delimiter: Optional[str] = None,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region_name: Optional[str] = None,
) -> List[StorageObjectMetadata]:
    """
    List all objects in an Amazon S3 bucket under a prefix, handling pagination.

    This function automatically handles continuation tokens to retrieve all
    matching objects beyond the single-request limit.

    Args:
        bucket_name: S3 bucket to list objects from.
        prefix: Object key prefix to filter results.
        delimiter: Optional delimiter for grouping common prefixes.
        aws_access_key_id: Optional AWS access key ID.
        aws_secret_access_key: Optional AWS secret access key.
        region_name: Optional AWS region name.

    Returns:
        Complete list of StorageObjectMetadata for all matching objects.
    """
    all_objects: List[StorageObjectMetadata] = []
    continuation_token = None

    s3_client = get_s3_client(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
    )

    while True:
        list_params = {
            "Bucket": bucket_name,
            "Prefix": prefix,
        }

        if delimiter:
            list_params["Delimiter"] = delimiter

        if continuation_token:
            list_params["ContinuationToken"] = continuation_token

        try:
            response = s3_client.list_objects_v2(**list_params)
            listing = normalize_s3_list_response(
                list_response=response,
                bucket_name=bucket_name,
                prefix=prefix,
            )
            all_objects.extend(listing.objects)

            if not listing.is_truncated:
                break

            continuation_token = listing.next_continuation_token

        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "Unknown")
            raise RuntimeError(
                f"Failed to list objects from S3: {error_code} - {e}"
            ) from e

    return all_objects


def get_prefix_summary(
    bucket_name: str,
    prefix: str = "",
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region_name: Optional[str] = None,
) -> dict:
    """
    Get a summary of objects under a prefix in Amazon S3.

    Returns counts, total size, and storage class distribution.

    Args:
        bucket_name: S3 bucket to analyze.
        prefix: Object key prefix to filter.
        aws_access_key_id: Optional AWS access key ID.
        aws_secret_access_key: Optional AWS secret access key.
        region_name: Optional AWS region name.

    Returns:
        Dictionary with summary statistics.
    """
    objects = list_all_objects_by_prefix(
        bucket_name=bucket_name,
        prefix=prefix,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
    )

    total_size = sum(obj.content_length for obj in objects)
    storage_classes = {}

    for obj in objects:
        sc = obj.storage_class or "STANDARD"
        storage_classes[sc] = storage_classes.get(sc, 0) + 1

    return {
        "bucket_name": bucket_name,
        "prefix": prefix,
        "object_count": len(objects),
        "total_size_bytes": total_size,
        "storage_class_distribution": storage_classes,
    }
