"""
List stored objects under a bucket or container prefix (AWS S3).

Provider: AWS S3 via boto3
- Uses boto3 S3 client list_objects_v2 for AWS S3 object listing
- AWS S3 endpoint: https://s3.{region}.amazonaws.com
"""

import logging
from typing import List

from storage_client import get_s3_client
from storage_models import (
    ListPrefixRequest,
    ListPrefixResponse,
    ListedObject,
    normalize_list_response,
)

logger = logging.getLogger(__name__)


def list_objects_by_prefix(
    bucket: str,
    prefix: str,
    delimiter: str = "",
    max_keys: int = 1000,
    start_after: str = "",
) -> ListPrefixResponse:
    """
    List objects in an AWS S3 bucket under a given prefix.

    Supports pagination via continuation tokens and common prefix
    grouping (directory-like listing).

    Provider signals:
    - boto3 S3 client (AWS S3 managed object storage)
    - list_objects_v2 is the AWS S3 API for object enumeration
    - S3 common prefixes and continuation token pagination
    """
    s3_client = get_s3_client()

    request = ListPrefixRequest(
        bucket=bucket,
        prefix=prefix,
        delimiter=delimiter or None,
        max_keys=max_keys,
        start_after=start_after or None,
    )

    list_kwargs = {
        "Bucket": bucket,
        "Prefix": prefix,
        "MaxKeys": max_keys,
    }

    if delimiter:
        list_kwargs["Delimiter"] = delimiter
    if start_after:
        list_kwargs["StartAfter"] = start_after

    logger.info("Listing objects in s3://%s with prefix '%s'", bucket, prefix)

    raw = s3_client.list_objects_v2(**list_kwargs)

    return normalize_list_response(raw, bucket, prefix)


def list_all_objects_by_prefix(
    bucket: str,
    prefix: str,
    delimiter: str = "",
) -> List[ListedObject]:
    """
    List all objects under a prefix in AWS S3, handling pagination automatically.

    Provider signals:
    - boto3 S3 paginator for AWS S3 list_objects_v2 pagination
    - AWS S3 managed object storage
    """
    s3_client = get_s3_client()

    paginator = s3_client.get_paginator("list_objects_v2")

    page_kwargs = {
        "Bucket": bucket,
        "Prefix": prefix,
    }

    if delimiter:
        page_kwargs["Delimiter"] = delimiter

    logger.info("Listing all objects in s3://%s with prefix '%s'", bucket, prefix)

    all_objects: List[ListedObject] = []

    for page in paginator.paginate(**page_kwargs):
        for obj in page.get("Contents", []):
            listed = ListedObject(
                key=obj.get("Key", ""),
                size=obj.get("Size", 0),
                last_modified=obj.get("LastModified"),
                etag=obj.get("ETag", "").strip('"'),
                storage_class=obj.get("StorageClass", "STANDARD"),
            )
            all_objects.append(listed)

    return all_objects
