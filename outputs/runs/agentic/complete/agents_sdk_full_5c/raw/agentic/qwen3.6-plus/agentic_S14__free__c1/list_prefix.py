"""List stored objects under a bucket prefix in AWS S3 managed object storage.

Uses boto3 (AWS SDK for Python) to list objects in Amazon S3 buckets.
Requires AWS credentials in environment variables:
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
"""

from storage_client import get_s3_client, validate_bucket_name
from storage_models import ListPrefixResult


def list_prefix(bucket, prefix="", max_keys=None, delimiter=None,
                continuation_token=None, region=None, endpoint_url=None):
    """List objects stored under a given prefix in an S3 bucket.

    Args:
        bucket: S3 bucket name.
        prefix: Object key prefix to filter results (e.g., "documents/2024/").
        max_keys: Maximum number of objects to return (default S3 max is 1000).
        delimiter: Character to group common prefixes (e.g., "/" for directory simulation).
        continuation_token: Token for paginated results from a previous call.
        region: Optional AWS region override.
        endpoint_url: Optional custom S3 endpoint.

    Returns:
        ListPrefixResult containing object listing and pagination info.

    Raises:
        botocore.exceptions.ClientError: If the list operation fails.
    """
    validate_bucket_name(bucket)

    s3_client = get_s3_client(region=region, endpoint_url=endpoint_url)

    params = {
        "Bucket": bucket,
        "Prefix": prefix,
    }
    if max_keys is not None:
        params["MaxKeys"] = max_keys
    if delimiter is not None:
        params["Delimiter"] = delimiter
    if continuation_token is not None:
        params["ContinuationToken"] = continuation_token

    response = s3_client.list_objects_v2(**params)

    return ListPrefixResult.from_s3_list(response, bucket, prefix)


def list_all_prefix(bucket, prefix="", delimiter=None, region=None,
                    endpoint_url=None):
    """List all objects under a prefix, automatically handling pagination.

    Args:
        bucket: S3 bucket name.
        prefix: Object key prefix to filter results.
        delimiter: Character to group common prefixes.
        region: Optional AWS region override.
        endpoint_url: Optional custom S3 endpoint.

    Returns:
        ListPrefixResult with all accumulated objects across all pages.
    """
    validate_bucket_name(bucket)

    s3_client = get_s3_client(region=region, endpoint_url=endpoint_url)

    all_objects = []
    all_prefixes = []
    continuation_token = None
    is_truncated = False

    while True:
        params = {
            "Bucket": bucket,
            "Prefix": prefix,
        }
        if delimiter is not None:
            params["Delimiter"] = delimiter
        if continuation_token:
            params["ContinuationToken"] = continuation_token

        response = s3_client.list_objects_v2(**params)

        contents = response.get("Contents", [])
        for obj in contents:
            all_objects.append({
                "key": obj["Key"],
                "size": obj.get("Size"),
                "last_modified": obj.get("LastModified"),
                "etag": obj.get("ETag", "").strip('"'),
                "storage_class": obj.get("StorageClass"),
            })

        common_prefixes = [
            p.get("Prefix") for p in response.get("CommonPrefixes", [])
        ]
        all_prefixes.extend(common_prefixes)

        is_truncated = response.get("IsTruncated", False)
        if is_truncated:
            continuation_token = response.get("NextContinuationToken")
        else:
            break

    result = ListPrefixResult(
        bucket=bucket,
        prefix=prefix,
        objects=all_objects,
        common_prefixes=list(set(all_prefixes)),
        is_truncated=False,
        next_continuation_token=None,
    )
    return result
