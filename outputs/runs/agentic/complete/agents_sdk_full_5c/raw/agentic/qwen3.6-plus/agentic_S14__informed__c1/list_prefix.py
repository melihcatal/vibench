"""
List stored objects under a bucket or container prefix in Amazon S3.

Uses the boto3 SDK to enumerate objects stored under a given prefix
in an Amazon Simple Storage Service (S3) bucket. Supports pagination,
delimiter-based grouping, and continuation tokens.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from storage_client import create_s3_client, validate_bucket_exists
from storage_models import (
    ListPrefixRequest,
    ListPrefixResponse,
    ObjectSummary,
    parse_last_modified,
)

logger = logging.getLogger(__name__)


def list_objects_by_prefix(
    bucket: str,
    prefix: str = "",
    *,
    delimiter: str = "",
    max_keys: int = 1000,
    start_after: str = "",
    continuation_token: Optional[str] = None,
    s3_client: Optional[boto3.client] = None,
) -> ListPrefixResponse:
    """
    List objects in an Amazon S3 bucket under a given prefix.

    Uses the S3 ListObjectsV2 API with optional delimiter for hierarchical
    listing (simulating folder structures) and pagination support.

    Args:
        bucket: S3 bucket name to list from.
        prefix: Prefix to filter objects by (e.g., "documents/2024/").
        delimiter: Delimiter for grouping (e.g., "/" to simulate folders).
        max_keys: Maximum number of keys to return per request (up to 1000).
        start_after: Key to start listing after (exclusive).
        continuation_token: Token from a previous truncated response.
        s3_client: Optional pre-created boto3 S3 client.

    Returns:
        ListPrefixResponse with object summaries and common prefixes.
    """
    client = s3_client or create_s3_client()

    if not validate_bucket_exists(client, bucket):
        raise ValueError(f"Bucket '{bucket}' does not exist or is not accessible.")

    request = ListPrefixRequest(
        bucket=bucket,
        prefix=prefix,
        delimiter=delimiter,
        max_keys=min(max_keys, 1000),
        start_after=start_after,
    )

    list_params: dict[str, str | int] = {
        "Bucket": request.bucket,
        "Prefix": request.prefix,
        "MaxKeys": request.max_keys,
    }
    if request.delimiter:
        list_params["Delimiter"] = request.delimiter
    if request.start_after:
        list_params["StartAfter"] = request.start_after
    if continuation_token:
        list_params["ContinuationToken"] = continuation_token

    try:
        response = client.list_objects_v2(**list_params)  # type: ignore[arg-type]
    except ClientError as exc:
        logger.error("Failed to list objects in s3://%s: %s", bucket, exc)
        raise

    objects: list[ObjectSummary] = []
    for item in response.get("Contents", []):
        last_modified = item.get("LastModified")
        if last_modified and not isinstance(last_modified, datetime):
            last_modified = parse_last_modified(last_modified)
        if last_modified and last_modified.tzinfo is None:
            last_modified = last_modified.replace(tzinfo=timezone.utc)

        objects.append(
            ObjectSummary(
                key=item.get("Key", ""),
                size=item.get("Size", 0),
                etag=item.get("ETag", "").strip('"'),
                last_modified=last_modified,
                storage_class=item.get("StorageClass", "STANDARD"),
            )
        )

    common_prefixes = [
        cp.get("Prefix", "")
        for cp in response.get("CommonPrefixes", [])
    ]

    result = ListPrefixResponse(
        bucket=bucket,
        prefix=prefix,
        objects=objects,
        common_prefixes=common_prefixes,
        is_truncated=response.get("IsTruncated", False),
        next_continuation_token=response.get("NextContinuationToken"),
    )
    logger.info(
        "Listed %d objects under s3://%s/%s (truncated=%s)",
        len(objects),
        bucket,
        prefix,
        result.is_truncated,
    )
    return result


def list_all_objects_by_prefix(
    bucket: str,
    prefix: str = "",
    *,
    delimiter: str = "",
    max_results: Optional[int] = None,
    s3_client: Optional[boto3.client] = None,
) -> list[ObjectSummary]:
    """
    List all objects under a prefix, automatically paginating through results.

    Args:
        bucket: S3 bucket name.
        prefix: Prefix to filter objects.
        delimiter: Delimiter for hierarchical grouping.
        max_results: Optional maximum total objects to return across all pages.
        s3_client: Optional pre-created boto3 S3 client.

    Returns:
        List of all ObjectSummary objects matching the prefix.
    """
    all_objects: list[ObjectSummary] = []
    continuation_token: Optional[str] = None

    while True:
        response = list_objects_by_prefix(
            bucket=bucket,
            prefix=prefix,
            delimiter=delimiter,
            max_keys=1000,
            continuation_token=continuation_token,
            s3_client=s3_client,
        )
        all_objects.extend(response.objects)

        if max_results is not None and len(all_objects) >= max_results:
            all_objects = all_objects[:max_results]
            break

        if not response.is_truncated:
            break

        continuation_token = response.next_continuation_token

    return all_objects


def list_directory_structure(
    bucket: str,
    prefix: str = "",
    *,
    s3_client: Optional[boto3.client] = None,
) -> dict[str, list[ObjectSummary]]:
    """
    List the top-level directory structure under a prefix in Amazon S3.

    Returns a dictionary mapping each immediate sub-prefix to its objects.

    Args:
        bucket: S3 bucket name.
        prefix: Root prefix to inspect.
        s3_client: Optional pre-created boto3 S3 client.

    Returns:
        Dict mapping subdirectory names to their ObjectSummary lists.
    """
    response = list_objects_by_prefix(
        bucket=bucket,
        prefix=prefix,
        delimiter="/",
        s3_client=s3_client,
    )

    structure: dict[str, list[ObjectSummary]] = {}
    for sub_prefix in response.common_prefixes:
        sub_response = list_objects_by_prefix(
            bucket=bucket,
            prefix=sub_prefix,
            s3_client=s3_client,
        )
        structure[sub_prefix] = sub_response.objects

    return structure
