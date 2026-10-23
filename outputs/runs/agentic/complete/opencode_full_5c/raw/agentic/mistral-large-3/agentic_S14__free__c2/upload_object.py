import os
from typing import BinaryIO, Union

from boto3 import client
from botocore.client import Config
from botocore.exceptions import ClientError


def upload_object(
    bucket_name: str,
    object_key: str,
    data: Union[BinaryIO, bytes],
    content_type: str = "application/octet-stream",
    metadata: dict = None,
) -> str:
    """
    Uploads a file or byte stream to AWS S3 managed object storage.

    Args:
        bucket_name: Name of the S3 bucket.
        object_key: Key/path for the object in the bucket.
        data: File-like object or bytes to upload.
        content_type: MIME type of the object.
        metadata: Optional metadata dictionary for the object.

    Returns:
        str: The S3 object key of the uploaded object.

    Raises:
        ClientError: If the upload fails.
    """
    s3_client = client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        config=Config(signature_version="s3v4"),
    )

    extra_args = {"ContentType": content_type}
    if metadata:
        extra_args["Metadata"] = metadata

    s3_client.upload_fileobj(data, bucket_name, object_key, ExtraArgs=extra_args)
    return object_key
