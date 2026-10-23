"""List stored objects under a bucket or container prefix in AWS S3."""

from typing import Optional, List

from storage_client import S3ClientFactory
from storage_models import (
    ListPrefixRequest,
    ListPrefixResponse,
    ListedObject,
)


def list_prefix(
    prefix: str = "",
    bucket: Optional[str] = None,
    delimiter: str = "",
    max_keys: int = 1000,
) -> ListPrefixResponse:
    """
    List all objects in an S3 bucket that match a given prefix.

    Uses boto3's list_objects_v2 API against the S3 service
    (s3.us-east-1.amazonaws.com or configured S3_ENDPOINT_URL).
    Handles pagination automatically and returns all matching keys.

    Args:
        prefix: Key prefix to filter by (e.g., 'documents/2024/').
        bucket: S3 bucket name (falls back to S3_BUCKET_NAME env var).
        delimiter: Optional delimiter to group keys into common prefixes
                   (e.g., '/' to simulate directory structure).
        max_keys: Maximum number of objects to return per API call.

    Returns:
        ListPrefixResponse containing the list of ListedObject entries,
        common prefixes (if delimiter is set), and pagination info.
    """
    factory = S3ClientFactory(bucket=bucket)
    target_bucket = factory.bucket
    s3_client = factory.s3_client

    all_objects: List[ListedObject] = []
    all_prefixes: List[str] = []
    continuation_token = None
    is_truncated = False

    while True:
        list_params = {
            "Bucket": target_bucket,
            "Prefix": prefix,
            "MaxKeys": max_keys,
        }

        if delimiter:
            list_params["Delimiter"] = delimiter

        if continuation_token:
            list_params["ContinuationToken"] = continuation_token

        response = s3_client.list_objects_v2(**list_params)

        for s3_obj in response.get("Contents", []):
            listed = ListedObject.from_s3_object(s3_obj)
            all_objects.append(listed)

        for cp in response.get("CommonPrefixes", []):
            all_prefixes.append(cp.get("Prefix", ""))

        is_truncated = response.get("IsTruncated", False)
        continuation_token = response.get("NextContinuationToken")

        if not is_truncated or not continuation_token:
            break

    return ListPrefixResponse(
        objects=all_objects,
        common_prefixes=all_prefixes,
        is_truncated=is_truncated,
        next_continuation_token=continuation_token,
        key_count=len(all_objects),
    )


def list_prefix_single_page(
    prefix: str = "",
    bucket: Optional[str] = None,
    delimiter: str = "",
    max_keys: int = 1000,
    continuation_token: Optional[str] = None,
) -> ListPrefixResponse:
    """
    List objects under a prefix with manual pagination control.

    Returns a single page of results, allowing the caller to manage
    pagination via the continuation_token. Useful for large buckets
    where the caller wants to stream results page-by-page.

    Args:
        prefix: Key prefix to filter by.
        bucket: S3 bucket name.
        delimiter: Delimiter for grouping common prefixes.
        max_keys: Maximum keys per page.
        continuation_token: Token from a previous response for pagination.

    Returns:
        ListPrefixResponse with a single page of results.
    """
    factory = S3ClientFactory(bucket=bucket)
    target_bucket = factory.bucket
    s3_client = factory.s3_client

    list_params = {
        "Bucket": target_bucket,
        "Prefix": prefix,
        "MaxKeys": max_keys,
    }

    if delimiter:
        list_params["Delimiter"] = delimiter

    if continuation_token:
        list_params["ContinuationToken"] = continuation_token

    response = s3_client.list_objects_v2(**list_params)

    objects = [
        ListedObject.from_s3_object(s3_obj)
        for s3_obj in response.get("Contents", [])
    ]

    common_prefixes = [
        cp.get("Prefix", "")
        for cp in response.get("CommonPrefixes", [])
    ]

    return ListPrefixResponse(
        objects=objects,
        common_prefixes=common_prefixes,
        is_truncated=response.get("IsTruncated", False),
        next_continuation_token=response.get("NextContinuationToken"),
        key_count=len(objects),
    )
