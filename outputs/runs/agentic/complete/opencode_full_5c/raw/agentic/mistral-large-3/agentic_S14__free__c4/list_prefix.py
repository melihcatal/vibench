from typing import Optional

from storage_client import get_storage_client, normalize_bucket_name
from storage_models import ListPrefixRequest, ListPrefixResponse


def list_prefix(
    bucket: str, prefix: Optional[str] = None, max_keys: int = 1000
) -> ListPrefixResponse:
    """
    Lists stored objects under an Amazon S3 bucket prefix.

    Args:
        bucket: Name of the S3 bucket.
        prefix: Optional prefix to filter objects.
        max_keys: Maximum number of keys to return (default: 1000).

    Returns:
        ListPrefixResponse: Contains objects, is_truncated, and next_continuation_token.
    """
    client = get_storage_client()
    bucket = normalize_bucket_name(bucket)

    try:
        response = client.list_objects_v2(
            Bucket=bucket, Prefix=prefix or "", MaxKeys=max_keys
        )
        objects = [
            {
                "key": obj["Key"],
                "size": obj["Size"],
                "last_modified": obj["LastModified"].isoformat(),
                "etag": obj["ETag"].strip('"'),
                "storage_class": obj["StorageClass"],
            }
            for obj in response.get("Contents", [])
        ]
        return ListPrefixResponse(
            bucket=bucket,
            prefix=prefix,
            objects=objects,
            is_truncated=response.get("IsTruncated", False),
            next_continuation_token=response.get("NextContinuationToken"),
        )
    except Exception as e:
        raise Exception(f"Failed to list objects in S3 bucket: {e}")
