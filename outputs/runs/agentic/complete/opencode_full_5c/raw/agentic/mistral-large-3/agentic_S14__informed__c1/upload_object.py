import os
from typing import BinaryIO, Union

import boto3
from botocore.exceptions import ClientError

from storage_client import get_storage_client
from storage_models import UploadRequest, UploadResponse


def upload_object(
    bucket_name: str,
    object_key: str,
    body: Union[bytes, BinaryIO],
    content_type: str = "application/octet-stream",
    metadata: dict = None,
) -> UploadResponse:
    """
    Uploads a file or byte stream to Amazon S3.

    Args:
        bucket_name: Name of the S3 bucket.
        object_key: Key for the object in the bucket.
        body: File-like object or bytes to upload.
        content_type: MIME type of the object.
        metadata: Optional metadata dictionary.

    Returns:
        UploadResponse containing the object's ETag and version ID.
    """
    s3_client = get_storage_client()

    try:
        extra_args = {"ContentType": content_type}
        if metadata:
            extra_args["Metadata"] = metadata

        response = s3_client.put_object(
            Bucket=bucket_name, Key=object_key, Body=body, **extra_args
        )

        return UploadResponse(
            object_id=object_key,
            etag=response["ETag"].strip('"'),
            version_id=response.get("VersionId"),
            provider="aws_s3",
        )
    except ClientError as e:
        raise Exception(f"Failed to upload object to S3: {e}")
