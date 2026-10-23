"""Read object metadata or head information from AWS S3 Managed Object Storage."""

from typing import Optional, Dict, Any

from storage_client import S3ClientFactory
from storage_models import ObjectMetadata


def get_object_metadata(
    key: str,
    bucket: Optional[str] = None,
    version_id: Optional[str] = None,
) -> ObjectMetadata:
    """
    Retrieve metadata for a stored S3 object using the HeadObject API.

    Calls boto3's head_object method against the S3 API endpoint
    (s3.us-east-1.amazonaws.com or S3_ENDPOINT_URL) to fetch object
    metadata without downloading the object body.

    Args:
        key: The object key (path) within the bucket.
        bucket: S3 bucket name (falls back to S3_BUCKET_NAME env var).
        version_id: Specific object version to query (for versioned buckets).

    Returns:
        ObjectMetadata with content type, length, ETag, last modified, etc.

    Raises:
        botocore.exceptions.ClientError: If the object does not exist or
            the caller lacks s3:GetObject permissions.
    """
    factory = S3ClientFactory(bucket=bucket)
    target_bucket = factory.bucket
    s3_client = factory.s3_client

    head_params: Dict[str, Any] = {
        "Bucket": target_bucket,
        "Key": key,
    }
    if version_id:
        head_params["VersionId"] = version_id

    head_response = s3_client.head_object(**head_params)

    metadata = ObjectMetadata.from_head_response(
        key=key,
        bucket=target_bucket,
        head_response=head_response,
    )

    return metadata


def get_object_metadata_batch(
    keys: list,
    bucket: Optional[str] = None,
) -> list:
    """
    Retrieve metadata for multiple S3 objects in a batch.

    Iterates over a list of keys and calls head_object for each one.
    Returns a list of ObjectMetadata, with None for inaccessible keys.

    Args:
        keys: List of object keys to query.
        bucket: S3 bucket name.

    Returns:
        List of ObjectMetadata or None for each key.
    """
    factory = S3ClientFactory(bucket=bucket)
    target_bucket = factory.bucket
    s3_client = factory.s3_client

    results = []
    for key in keys:
        try:
            head_response = s3_client.head_object(Bucket=target_bucket, Key=key)
            meta = ObjectMetadata.from_head_response(
                key=key,
                bucket=target_bucket,
                head_response=head_response,
            )
            results.append(meta)
        except s3_client.exceptions.ClientError:
            results.append(None)

    return results


def object_exists(
    key: str,
    bucket: Optional[str] = None,
) -> bool:
    """
    Check if an object exists in S3 by attempting a head_object call.

    Args:
        key: The object key to check.
        bucket: S3 bucket name.

    Returns:
        True if the object exists and is accessible, False otherwise.
    """
    factory = S3ClientFactory(bucket=bucket)
    target_bucket = factory.bucket
    s3_client = factory.s3_client

    try:
        s3_client.head_object(Bucket=target_bucket, Key=key)
        return True
    except s3_client.exceptions.ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "")
        if error_code in ("404", "NoSuchKey"):
            return False
        raise
