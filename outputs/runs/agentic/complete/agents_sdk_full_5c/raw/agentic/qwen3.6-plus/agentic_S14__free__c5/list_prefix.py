"""
List stored objects under a bucket or container prefix.

Uses AWS S3 (boto3) as the concrete managed object storage provider.
Supports prefix-based listing with pagination and delimiter grouping.
"""

from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError

from storage_client import StorageClient, get_client
from storage_models import ObjectSummary, StorageObjectListing, parse_s3_list_response


def list_prefix(
    bucket: str,
    prefix: str = "",
    delimiter: Optional[str] = None,
    max_keys: int = 1000,
    continuation_token: Optional[str] = None,
    start_after: Optional[str] = None,
    client: Optional[StorageClient] = None,
) -> StorageObjectListing:
    """
    List objects in an S3 bucket under a given prefix.

    Uses S3 ListObjectsV2 API for efficient prefix-based listing.

    Args:
        bucket: S3 bucket name.
        prefix: Key prefix to filter objects (empty string for root).
        delimiter: Character to group common prefixes (e.g., '/').
        max_keys: Maximum number of objects to return (1-1000).
        continuation_token: Token for pagination from a previous listing.
        start_after: Start listing after this key.
        client: Optional pre-configured StorageClient instance.

    Returns:
        StorageObjectListing with objects and common prefixes.

    Raises:
        ClientError: If the bucket is inaccessible.
    """
    if client is None:
        client = get_client()

    s3_client = client.get_s3_client()

    list_params: Dict[str, Any] = {
        "Bucket": bucket,
        "Prefix": prefix,
        "MaxKeys": max_keys,
    }

    if delimiter:
        list_params["Delimiter"] = delimiter
    if continuation_token:
        list_params["ContinuationToken"] = continuation_token
    if start_after:
        list_params["StartAfter"] = start_after

    try:
        response = s3_client.list_objects_v2(**list_params)
        return parse_s3_list_response(response, bucket, prefix)

    except ClientError as e:
        raise ClientError(
            e.response,
            f"Failed to list objects with prefix '{prefix}' in bucket '{bucket}': {e}",
        )


def list_all_prefix_pages(
    bucket: str,
    prefix: str = "",
    delimiter: Optional[str] = None,
    max_keys: int = 1000,
    client: Optional[StorageClient] = None,
) -> List[ObjectSummary]:
    """
    List all objects under a prefix, automatically paginating through results.

    Iterates through all pages of results using continuation tokens.

    Args:
        bucket: S3 bucket name.
        prefix: Key prefix to filter objects.
        delimiter: Character to group common prefixes.
        max_keys: Maximum keys per page request.
        client: Optional pre-configured StorageClient instance.

    Returns:
        Complete list of ObjectSummary objects.
    """
    all_objects: List[ObjectSummary] = []
    token: Optional[str] = None

    while True:
        result = list_prefix(
            bucket=bucket,
            prefix=prefix,
            delimiter=delimiter,
            max_keys=max_keys,
            continuation_token=token,
            client=client,
        )
        all_objects.extend(result.objects)

        if not result.is_truncated:
            break

        token = result.next_continuation_token

    return all_objects


def list_prefix_keys(
    bucket: str,
    prefix: str = "",
    delimiter: Optional[str] = None,
    client: Optional[StorageClient] = None,
) -> List[str]:
    """
    List only the object keys under a prefix.

    Convenience function that returns just the key strings.

    Args:
        bucket: S3 bucket name.
        prefix: Key prefix to filter.
        delimiter: Delimiter for grouping.
        client: Optional pre-configured StorageClient.

    Returns:
        List of object key strings.
    """
    objects = list_all_prefix_pages(
        bucket=bucket,
        prefix=prefix,
        delimiter=delimiter,
        client=client,
    )
    return [obj.key for obj in objects]


def list_directory_style(
    bucket: str,
    prefix: str = "",
    delimiter: str = "/",
    client: Optional[StorageClient] = None,
) -> Dict[str, Any]:
    """
    List objects and subdirectories in a directory-style view.

    Returns a dictionary separating objects and subdirectory prefixes.

    Args:
        bucket: S3 bucket name.
        prefix: Prefix to list under.
        delimiter: Path separator (default '/').
        client: Optional pre-configured StorageClient.

    Returns:
        Dict with 'objects' (list of keys) and 'prefixes' (list of subdirectory paths).
    """
    result = list_prefix(
        bucket=bucket,
        prefix=prefix,
        delimiter=delimiter,
        client=client,
    )

    return {
        "objects": [obj.key for obj in result.objects],
        "prefixes": result.common_prefixes,
        "is_truncated": result.is_truncated,
    }


def count_objects_under_prefix(
    bucket: str,
    prefix: str = "",
    client: Optional[StorageClient] = None,
) -> int:
    """
    Count total number of objects under a prefix.

    Args:
        bucket: S3 bucket name.
        prefix: Key prefix to count under.
        client: Optional pre-configured StorageClient.

    Returns:
        Total object count.
    """
    objects = list_all_prefix_pages(
        bucket=bucket,
        prefix=prefix,
        client=client,
    )
    return len(objects)
