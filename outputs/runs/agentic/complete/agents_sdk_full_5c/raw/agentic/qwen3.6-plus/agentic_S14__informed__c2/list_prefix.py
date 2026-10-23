"""
list_prefix.py - List stored objects under a bucket or container prefix in
Amazon S3 managed object storage.

Uses the boto3 SDK (Amazon S3).
Auth env vars: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""
from __future__ import annotations

from typing import Optional

from botocore.exceptions import ClientError

from storage_client import create_s3_client, handle_s3_error, parse_s3_object_listing
from storage_models import ListPrefixRequest, ListPrefixResponse, StorageObjectInfo


def list_prefix(
    bucket: str,
    prefix: str = "",
    delimiter: str = "",
    max_keys: int = 1000,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region: Optional[str] = None,
    endpoint_url: Optional[str] = None,
) -> ListPrefixResponse:
    """
    List objects in an Amazon S3 bucket under a given prefix.

    Uses the S3 list_objects_v2 API via boto3. Supports pagination
    continuation tokens for large result sets.

    Args:
        bucket: S3 bucket name to list objects from.
        prefix: Object key prefix to filter results (e.g., "documents/2024/").
        delimiter: Character used to group keys (e.g., "/" for folder-like grouping).
        max_keys: Maximum number of objects to return per request.
        aws_access_key_id: Optional AWS access key ID override.
        aws_secret_access_key: Optional AWS secret access key override.
        region: Optional AWS region override.
        endpoint_url: Optional S3 endpoint URL override.

    Returns:
        ListPrefixResponse with list of StorageObjectInfo and common prefixes.
    """
    request = ListPrefixRequest(
        bucket=bucket,
        prefix=prefix,
        delimiter=delimiter,
        max_keys=max_keys,
    )

    client = create_s3_client(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region=region,
        endpoint_url=endpoint_url,
    )

    all_objects: list[StorageObjectInfo] = []
    common_prefixes: list[str] = []
    is_truncated = False
    next_token = None

    try:
        list_kwargs = {
            "Bucket": request.bucket,
            "MaxKeys": request.max_keys,
        }
        if request.prefix:
            list_kwargs["Prefix"] = request.prefix
        if request.delimiter:
            list_kwargs["Delimiter"] = request.delimiter

        response = client.list_objects_v2(**list_kwargs)

        # Parse object listings
        parsed_objects = parse_s3_object_listing(response)
        all_objects.extend(parsed_objects)

        # Collect common prefixes (simulated folder structure)
        for cp in response.get("CommonPrefixes", []):
            common_prefixes.append(cp.get("Prefix", ""))

        is_truncated = response.get("IsTruncated", False)
        if is_truncated:
            next_token = response.get("NextContinuationToken")

        return ListPrefixResponse(
            bucket=request.bucket,
            prefix=request.prefix,
            objects=all_objects,
            common_prefixes=common_prefixes,
            is_truncated=is_truncated,
            next_continuation_token=next_token,
        )

    except ClientError as e:
        raise RuntimeError(handle_s3_error(e, "list_prefix"))


def list_prefix_all(
    bucket: str,
    prefix: str = "",
    delimiter: str = "",
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region: Optional[str] = None,
    endpoint_url: Optional[str] = None,
) -> ListPrefixResponse:
    """
    List all objects under a prefix in Amazon S3, auto-paginating through
    all results using continuation tokens.

    Args:
        bucket: S3 bucket name to list objects from.
        prefix: Object key prefix to filter results.
        delimiter: Character used to group keys.
        aws_access_key_id: Optional AWS access key ID override.
        aws_secret_access_key: Optional AWS secret access key override.
        region: Optional AWS region override.
        endpoint_url: Optional S3 endpoint URL override.

    Returns:
        ListPrefixResponse with complete list of all matching objects.
    """
    client = create_s3_client(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region=region,
        endpoint_url=endpoint_url,
    )

    all_objects: list[StorageObjectInfo] = []
    common_prefixes: list[str] = []
    continuation_token = None

    list_kwargs = {
        "Bucket": bucket,
        "MaxKeys": 1000,
    }
    if prefix:
        list_kwargs["Prefix"] = prefix
    if delimiter:
        list_kwargs["Delimiter"] = delimiter

    try:
        while True:
            if continuation_token:
                list_kwargs["ContinuationToken"] = continuation_token

            response = client.list_objects_v2(**list_kwargs)

            parsed = parse_s3_object_listing(response)
            all_objects.extend(parsed)

            for cp in response.get("CommonPrefixes", []):
                common_prefixes.append(cp.get("Prefix", ""))

            if response.get("IsTruncated", False):
                continuation_token = response.get("NextContinuationToken")
            else:
                break

        return ListPrefixResponse(
            bucket=bucket,
            prefix=prefix,
            objects=all_objects,
            common_prefixes=common_prefixes,
            is_truncated=False,
        )

    except ClientError as e:
        raise RuntimeError(handle_s3_error(e, "list_prefix_all"))
