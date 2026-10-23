import os
from typing import BinaryIO, Union

from storage_client import StorageClient
from storage_models import UploadRequest, UploadResponse


def upload_object(
    bucket_name: str,
    object_key: str,
    body: Union[bytes, BinaryIO],
    content_type: str = None,
    metadata: dict = None,
) -> UploadResponse:
    """
    Uploads a file or byte stream to Amazon S3 object storage.
    """
    client = StorageClient().get_client()

    request: UploadRequest = {
        "bucket_name": bucket_name,
        "object_key": object_key,
        "body": body,
        "content_type": content_type,
        "metadata": metadata,
    }

    try:
        response = client.put_object(
            Bucket=request["bucket_name"],
            Key=request["object_key"],
            Body=request["body"],
            ContentType=request["content_type"],
            Metadata=request["metadata"] or {},
        )
        return {
            "object_key": object_key,
            "etag": response["ETag"].strip('"'),
            "version_id": response.get("VersionId"),
        }
    except Exception as e:
        raise Exception(f"Failed to upload object to S3: {str(e)}")
