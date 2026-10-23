"""
object_metadata.py - Read object metadata (head information) from Amazon S3
managed object storage.

Uses the boto3 SDK (Amazon S3).
Auth env vars: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""
from __future__ import annotations

from typing import Optional

from botocore.exceptions import ClientError

from storage_client import create_s3_client, handle_s3_error
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse


def object_metadata(
    bucket: str,
    key: str,
    version_id: Optional[str] = None,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region: Optional[str] = None,
    endpoint_url: Optional[str] = None,
) -> ObjectMetadataResponse:
    """
    Retrieve metadata (HEAD information) for an object stored in Amazon S3.

    This operation uses the S3 HeadObject API via boto3 and returns metadata
    without downloading the object content.

    Args:
        bucket: S3 bucket name containing the object.
        key: Object key (path) within the bucket.
        version_id: Optional specific object version to retrieve metadata for.
        aws_access_key_id: Optional AWS access key ID override.
        aws_secret_access_key: Optional AWS secret access key override.
        region: Optional AWS region override.
        endpoint_url: Optional S3 endpoint URL override.

    Returns:
        ObjectMetadataResponse with content type, size, last modified,
        ETag, storage class, custom metadata, and encryption info.

    Raises:
        FileNotFoundError: If the object does not exist in the bucket.
    """
    request = ObjectMetadataRequest(bucket=bucket, key=key)

    client = create_s3_client(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region=region,
        endpoint_url=endpoint_url,
    )

    head_kwargs = {
        "Bucket": request.bucket,
        "Key": request.key,
    }
    if version_id:
        head_kwargs["VersionId"] = version_id

    try:
        response = client.head_object(**head_kwargs)

        # Extract custom metadata from response (prefixed with "x-amz-meta-")
        custom_metadata = {}
        for header_name, header_value in response.get("ResponseMetadata", {}).get(
            "HTTPHeaders", {}
        ).items():
            if header_name.startswith("x-amz-meta-"):
                meta_key = header_name.replace("x-amz-meta-", "")
                custom_metadata[meta_key] = header_value

        # Also check the Metadata field directly from head_object
        direct_metadata = response.get("Metadata", {})
        if direct_metadata:
            custom_metadata.update(direct_metadata)

        return ObjectMetadataResponse(
            bucket=request.bucket,
            key=request.key,
            content_type=response.get("ContentType"),
            content_length=response.get("ContentLength"),
            last_modified=response.get("LastModified"),
            etag=response.get("ETag", "").strip('"'),
            storage_class=response.get("StorageClass"),
            metadata=custom_metadata,
            version_id=response.get("VersionId"),
            server_side_encryption=response.get("ServerSideEncryption"),
        )

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "")
        if error_code == "404" or error_code == "NoSuchKey":
            raise FileNotFoundError(
                f"Object s3://{request.bucket}/{request.key} not found"
            )
        raise RuntimeError(handle_s3_error(e, "object_metadata"))
