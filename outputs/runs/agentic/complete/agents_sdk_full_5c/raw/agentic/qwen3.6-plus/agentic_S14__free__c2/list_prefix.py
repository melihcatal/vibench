"""
List stored objects under a bucket or container prefix (AWS S3).

Uses boto3 S3 list_objects_v2 to enumerate objects matching a prefix pattern.
"""

from typing import Optional, List

from botocore.exceptions import ClientError

from storage_client import get_s3_client, get_bucket_name
from storage_models import ListPrefixRequest, ListPrefixResponse


def list_objects_by_prefix(
    prefix: str = "",
    bucket: Optional[str] = None,
    delimiter: str = "",
    max_keys: int = 1000,
    start_after: Optional[str] = None,
    s3_client=None,
) -> ListPrefixResponse:
    """
    List S3 objects under a given prefix.

    Args:
        prefix: Prefix to filter objects (e.g., "documents/2024/")
        bucket: Target S3 bucket name
        delimiter: Delimiter for grouping common prefixes (e.g., "/")
        max_keys: Maximum number of keys to return (up to 1000)
        start_after: Start listing after this key (pagination)
        s3_client: Pre-configured boto3 S3 client

    Returns:
        ListPrefixResponse with listed objects and metadata
    """
    bucket_name = get_bucket_name(bucket)
    client = s3_client or get_s3_client()

    list_req = ListPrefixRequest(
        bucket=bucket_name,
        prefix=prefix,
        delimiter=delimiter,
        max_keys=max_keys,
        start_after=start_after,
    )

    params = {
        "Bucket": list_req.bucket,
        "Prefix": list_req.prefix,
        "MaxKeys": list_req.max_keys,
    }
    if list_req.delimiter:
        params["Delimiter"] = list_req.delimiter
    if list_req.start_after:
        params["StartAfter"] = list_req.start_after

    try:
        response = client.list_objects_v2(**params)
        return ListPrefixResponse.from_s3_list(
            bucket=list_req.bucket,
            prefix=list_req.prefix,
            list_response=response,
        )
    except ClientError as e:
        raise RuntimeError(
            f"Failed to list objects in s3://{list_req.bucket} with prefix '{list_req.prefix}': {e}"
        ) from e


def list_all_objects_by_prefix(
    prefix: str = "",
    bucket: Optional[str] = None,
    delimiter: str = "",
    s3_client=None,
) -> List[ListPrefixResponse]:
    """
    List all S3 objects under a prefix, handling pagination automatically.

    Args:
        prefix: Prefix to filter objects
        bucket: Target S3 bucket name
        delimiter: Delimiter for grouping common prefixes
        s3_client: Pre-configured boto3 S3 client

    Returns:
        List of ListPrefixResponse pages
    """
    all_responses = []
    continuation_token = None
    client = s3_client or get_s3_client()
    bucket_name = get_bucket_name(bucket)

    while True:
        params = {
            "Bucket": bucket_name,
            "Prefix": prefix,
            "MaxKeys": 1000,
        }
        if delimiter:
            params["Delimiter"] = delimiter
        if continuation_token:
            params["ContinuationToken"] = continuation_token

        response = client.list_objects_v2(**params)
        page_response = ListPrefixResponse.from_s3_list(
            bucket=bucket_name,
            prefix=prefix,
            list_response=response,
        )
        all_responses.append(page_response)

        if not response.get("IsTruncated", False):
            break
        continuation_token = response.get("NextContinuationToken")

    return all_responses


def get_subdirectories(
    prefix: str = "",
    bucket: Optional[str] = None,
    s3_client=None,
) -> List[str]:
    """
    Get immediate subdirectory prefixes under a given prefix.

    Args:
        prefix: Base prefix to scan
        bucket: Target S3 bucket name
        s3_client: Pre-configured boto3 S3 client

    Returns:
        List of subdirectory prefix strings
    """
    response = list_objects_by_prefix(
        prefix=prefix,
        bucket=bucket,
        delimiter="/",
        s3_client=s3_client,
    )
    return response.common_prefixes
