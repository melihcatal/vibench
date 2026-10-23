import os
from typing import BinaryIO, Union

from boto3 import client
from botocore.exceptions import ClientError

from storage_client import get_storage_client
from storage_models import UploadRequest, UploadResponse


def upload_object(
    bucket_name: str,
    object_key: str,
    data: Union[BinaryIO, bytes],
    content_type: str = "application/octet-stream",
    metadata: dict = None,
) -> UploadResponse:
    """
    Uploads a file or byte stream to AWS S3 object storage.

    Args:
        bucket_name: Name of the S3 bucket.
        object_key: Key/path for the object in the bucket.
        data: File-like object or bytes to upload.
        content_type: MIME type of the object.
        metadata: Optional metadata dictionary for the object.

    Returns:
        UploadResponse containing the object key and ETag.

    Raises:
        ClientError: If the upload fails.
    """
    s3_client = get_storage_client()

    try:
        extra_args = {"ContentType": content_type}
        if metadata:
            extra_args["Metadata"] = metadata

        s3_client.upload_fileobj(
            data if isinstance(data, BinaryIO) else BinaryIO(data),
            bucket_name,
            object_key,
            ExtraArgs=extra_args,
        )

        # Fetch ETag after upload
        head = s3_client.head_object(Bucket=bucket_name, Key=object_key)
        etag = head["ETag"]

        return UploadResponse(key=object_key, etag=etag)
    except ClientError as e:
        raise ClientError(
            error_response={
                "Error": {
                    "Code": e.response["Error"]["Code"],
                    "Message": e.response["Error"]["Message"],
                }
            },
            operation_name="upload_object",
        )
