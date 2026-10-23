import os
from typing import BinaryIO, Union
from boto3 import client
from botocore.exceptions import ClientError


def upload_object(
    bucket_name: str,
    object_key: str,
    body: Union[bytes, BinaryIO],
    content_type: str = "application/octet-stream",
    metadata: dict = None,
) -> dict:
    """
    Uploads a file or byte stream to Amazon S3.

    Args:
        bucket_name: Name of the S3 bucket.
        object_key: Key/path for the object in the bucket.
        body: File-like object or bytes to upload.
        content_type: MIME type of the object.
        metadata: Optional metadata dictionary.

    Returns:
        Dictionary containing upload details (e.g., ETag, VersionId).

    Raises:
        ClientError: If the upload fails.
    """
    s3_client = client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    try:
        upload_args = {
            "Bucket": bucket_name,
            "Key": object_key,
            "Body": body,
            "ContentType": content_type,
        }
        if metadata:
            upload_args["Metadata"] = metadata

        response = s3_client.put_object(**upload_args)
        return {
            "ETag": response.get("ETag"),
            "VersionId": response.get("VersionId"),
        }
    except ClientError as e:
        raise Exception(f"Failed to upload object: {e}")
