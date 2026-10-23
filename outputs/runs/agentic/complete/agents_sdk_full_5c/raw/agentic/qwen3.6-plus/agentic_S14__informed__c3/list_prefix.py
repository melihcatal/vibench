"""
List stored objects under a bucket or container prefix in Amazon S3.

Uses boto3 SDK for Amazon S3 (service=Amazon S3).
Environment variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
"""

from typing import List, Optional

from botocore.exceptions import ClientError

from storage_client import get_s3_client, validate_bucket_name
from storage_models import ListPrefixResponse


def list_prefix(
    bucket: str,
    prefix: str = "",
    delimiter: str = "/",
    max_keys: Optional[int] = None,
    continuation_token: Optional[str] = None,
    fetch_all_pages: bool = False,
) -> ListPrefixResponse:
    """
    List objects stored under a given prefix in an S3 bucket.

    Args:
        bucket: The S3 bucket name.
        prefix: The prefix filter (e.g., "documents/2024/").
        delimiter: Delimiter for grouping common prefixes (default "/").
        max_keys: Maximum number of keys to return per page (default 1000).
        continuation_token: Token for paginated results.
        fetch_all_pages: If True, automatically fetch all pages and merge results.

    Returns:
        ListPrefixResponse with object listings and pagination info.

    Raises:
        ValueError: If bucket name is invalid.
        ClientError: On S3 API errors.
    """
    validate_bucket_name(bucket)

    s3_client = get_s3_client()

    if fetch_all_pages:
        return _fetch_all_pages(
            s3_client=s3_client,
            bucket=bucket,
            prefix=prefix,
            delimiter=delimiter,
            max_keys=max_keys,
        )

    list_kwargs = {
        "Bucket": bucket,
        "Prefix": prefix,
        "Delimiter": delimiter,
    }

    if max_keys is not None:
        list_kwargs["MaxKeys"] = max_keys

    if continuation_token:
        list_kwargs["ContinuationToken"] = continuation_token

    response = s3_client.list_objects_v2(**list_kwargs)

    return ListPrefixResponse.from_s3_list(response, bucket, prefix)


def _fetch_all_pages(
    s3_client,
    bucket: str,
    prefix: str,
    delimiter: str,
    max_keys: Optional[int],
) -> ListPrefixResponse:
    """
    Paginate through all results and return a merged ListPrefixResponse.
    """
    all_objects = []
    all_common_prefixes = []
    is_truncated = False

    list_kwargs = {
        "Bucket": bucket,
        "Prefix": prefix,
        "Delimiter": delimiter,
    }

    if max_keys is not None:
        list_kwargs["MaxKeys"] = max_keys

    paginator = s3_client.get_paginator("list_objects_v2")
    page_iterator = paginator.paginate(**list_kwargs)

    for page in page_iterator:
        for item in page.get("Contents", []):
            all_objects.append({
                "key": item["Key"],
                "size": item.get("Size"),
                "last_modified": item.get("LastModified"),
                "etag": item.get("ETag", "").strip('"'),
                "storage_class": item.get("StorageClass"),
            })

        for cp in page.get("CommonPrefixes", []):
            all_common_prefixes.append(cp["Prefix"])

    # Build a response-like dict for normalization
    combined_response = {
        "Contents": [],
        "CommonPrefixes": [{"Prefix": p} for p in all_common_prefixes],
        "IsTruncated": False,
        "MaxKeys": max_keys,
    }

    result = ListPrefixResponse.from_s3_list(combined_response, bucket, prefix)
    result.objects = all_objects
    result.common_prefixes = all_common_prefixes
    return result


def list_all_keys(bucket: str, prefix: str = "") -> List[str]:
    """
    Convenience function to return just the list of all object keys under a prefix.

    Args:
        bucket: The S3 bucket name.
        prefix: The prefix filter.

    Returns:
        List of object key strings.
    """
    response = list_prefix(bucket, prefix, fetch_all_pages=True)
    return [obj["key"] for obj in response.objects]
