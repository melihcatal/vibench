"""Read object metadata (HEAD) from AWS S3 managed object storage.

Uses boto3 (AWS SDK for Python) to retrieve object metadata from Amazon S3.
Requires AWS credentials in environment variables:
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
"""

from storage_client import get_s3_client, validate_bucket_name
from storage_models import ObjectMetadataResult


def object_metadata(bucket, key, version_id=None, region=None, endpoint_url=None):
    """Retrieve metadata / HEAD information for an S3 object.

    Args:
        bucket: S3 bucket name.
        key: Object key (path within the bucket).
        version_id: Optional specific object version to query.
        region: Optional AWS region override.
        endpoint_url: Optional custom S3 endpoint.

    Returns:
        ObjectMetadataResult containing size, content_type, etag, etc.

    Raises:
        botocore.exceptions.ClientError: If the object does not exist or access is denied.
    """
    validate_bucket_name(bucket)

    s3_client = get_s3_client(region=region, endpoint_url=endpoint_url)

    params = {
        "Bucket": bucket,
        "Key": key,
    }
    if version_id:
        params["VersionId"] = version_id

    head_response = s3_client.head_object(**params)

    return ObjectMetadataResult.from_s3_head(head_response, bucket, key)


def object_exists(bucket, key, region=None, endpoint_url=None):
    """Check whether an object exists in S3 by attempting a HEAD request.

    Args:
        bucket: S3 bucket name.
        key: Object key (path within the bucket).
        region: Optional AWS region override.
        endpoint_url: Optional custom S3 endpoint.

    Returns:
        True if the object exists, False otherwise.
    """
    validate_bucket_name(bucket)

    s3_client = get_s3_client(region=region, endpoint_url=endpoint_url)

    try:
        s3_client.head_object(Bucket=bucket, Key=key)
        return True
    except s3_client.exceptions.ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "")
        if error_code in ("404", "NoSuchKey"):
            return False
        raise


def get_object_tags(bucket, key, region=None, endpoint_url=None):
    """Retrieve the tag set associated with an S3 object.

    Args:
        bucket: S3 bucket name.
        key: Object key (path within the bucket).
        region: Optional AWS region override.
        endpoint_url: Optional custom S3 endpoint.

    Returns:
        Dict of tag key-value pairs.

    Raises:
        botocore.exceptions.ClientError: If tag retrieval fails.
    """
    validate_bucket_name(bucket)

    s3_client = get_s3_client(region=region, endpoint_url=endpoint_url)

    response = s3_client.get_object_tagging(Bucket=bucket, Key=key)
    tags = {tag["Key"]: tag["Value"] for tag in response.get("TagSet", [])}
    return tags
