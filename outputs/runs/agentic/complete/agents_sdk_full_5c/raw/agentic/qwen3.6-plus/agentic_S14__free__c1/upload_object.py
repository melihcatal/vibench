"""Upload a file or byte stream to AWS S3 managed object storage.

Uses boto3 (AWS SDK for Python) to interact with Amazon S3.
Requires AWS credentials in environment variables:
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
"""

import os
from storage_client import get_s3_client, validate_bucket_name
from storage_models import UploadRequest, UploadResponse


def upload_object(bucket, key, body, content_type=None, metadata=None,
                  acl=None, region=None, endpoint_url=None):
    """Upload a file or byte stream to an S3 bucket.

    Args:
        bucket: S3 bucket name.
        key: Object key (path within the bucket).
        body: File-like object or bytes to upload.
        content_type: MIME type of the object.
        metadata: Dict of user-defined metadata keys/values.
        acl: S3 canned ACL (e.g., 'private', 'public-read').
        region: Optional AWS region override.
        endpoint_url: Optional custom S3 endpoint.

    Returns:
        UploadResponse with etag, version_id, and other details.

    Raises:
        botocore.exceptions.ClientError: If the upload fails.
    """
    validate_bucket_name(bucket)

    s3_client = get_s3_client(region=region, endpoint_url=endpoint_url)

    upload_req = UploadRequest(
        bucket=bucket,
        key=key,
        body=body,
        content_type=content_type,
        metadata=metadata,
        acl=acl,
    )

    response = s3_client.put_object(**upload_req.to_s3_kwargs())

    return UploadResponse.from_s3_response(response, bucket, key)


def upload_file(bucket, key, file_path, content_type=None, metadata=None,
                acl=None, region=None, endpoint_url=None):
    """Upload a local file to an S3 bucket using S3 transfer manager.

    Args:
        bucket: S3 bucket name.
        key: Object key (path within the bucket).
        file_path: Local filesystem path to the file.
        content_type: MIME type of the object.
        metadata: Dict of user-defined metadata keys/values.
        acl: S3 canned ACL.
        region: Optional AWS region override.
        endpoint_url: Optional custom S3 endpoint.

    Returns:
        UploadResponse with etag, version_id, and other details.
    """
    validate_bucket_name(bucket)

    s3_client = get_s3_client(region=region, endpoint_url=endpoint_url)

    extra_args = {"ContentType": content_type} if content_type else {}
    if metadata:
        extra_args["Metadata"] = {k: str(v) for k, v in metadata.items()}
    if acl:
        extra_args["ACL"] = acl

    s3_client.upload_file(file_path, bucket, key, ExtraArgs=extra_args)

    # Retrieve the object metadata after upload to build response
    head = s3_client.head_object(Bucket=bucket, Key=key)
    return UploadResponse.from_s3_response(head, bucket, key)
