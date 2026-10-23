"""
list_prefix.py — List stored objects under a bucket or container prefix.

Concrete provider: Amazon S3 via boto3 SDK.
Provider signals:
  - boto3 S3 list_objects_v2 call
  - S3 client from storage_client
"""

from typing import List, Optional
from botocore.exceptions import ClientError

from storage_client import S3StorageClient
from storage_models import ObjectListing


def list_objects_by_prefix(
    bucket: str,
    prefix: str = "",
    delimiter: Optional[str] = None,
    max_keys: Optional[int] = None,
    start_after: Optional[str] = None,
) -> List[ObjectListing]:
    """
    List objects in an S3 bucket under a given prefix.

    Parameters
    ----------
    bucket : str
        S3 bucket name.
    prefix : str
        Object key prefix to filter results (e.g., "documents/invoices/").
    delimiter : str, optional
        Group keys by delimiter (e.g., "/" for directory-like behavior).
        When set, common prefixes are included as listing entries.
    max_keys : int, optional
        Maximum number of objects to return.
    start_after : str, optional
        Key to start listing after (for pagination).

    Returns
    -------
    list[ObjectListing]
        Normalized listing entries for each object and common prefix.
    """
    client = S3StorageClient(bucket=bucket).get_client()

    list_kwargs = {
        "Bucket": bucket,
        "Prefix": prefix,
    }

    if delimiter:
        list_kwargs["Delimiter"] = delimiter
    if max_keys:
        list_kwargs["MaxKeys"] = max_keys
    if start_after:
        list_kwargs["StartAfter"] = start_after

    results: List[ObjectListing] = []

    response = client.list_objects_v2(**list_kwargs)

    for obj in response.get("Contents", []):
        results.append(ObjectListing.from_s3_object(bucket, obj, is_prefix=False))

    for cp in response.get("CommonPrefixes", []):
        prefix_name = cp.get("Prefix", "")
        results.append(ObjectListing(
            bucket=bucket,
            key=prefix_name,
            is_prefix=True,
        ))

    # Handle truncated results via continuation token
    while response.get("IsTruncated", False):
        list_kwargs["ContinuationToken"] = response["NextContinuationToken"]
        response = client.list_objects_v2(**list_kwargs)

        for obj in response.get("Contents", []):
            results.append(ObjectListing.from_s3_object(bucket, obj, is_prefix=False))

        for cp in response.get("CommonPrefixes", []):
            prefix_name = cp.get("Prefix", "")
            results.append(ObjectListing(
                bucket=bucket,
                key=prefix_name,
                is_prefix=True,
            ))

    return results
