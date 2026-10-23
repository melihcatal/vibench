import os
from typing import Union

from storage_client import get_storage_client, get_bucket_name
from storage_models import UploadRequest, UploadResponse


def upload_object(request: UploadRequest) -> UploadResponse:
    """
    Upload a file or byte stream to Amazon S3.
    """
    client = get_storage_client()
    bucket = get_bucket_name()

    extra_args = {}
    if request.get("content_type"):
        extra_args["ContentType"] = request["content_type"]
    if request.get("metadata"):
        extra_args["Metadata"] = request["metadata"]

    response = client.put_object(
        Bucket=bucket,
        Key=request["key"],
        Body=request["body"],
        **extra_args
    )

    return {
        "key": request["key"],
        "etag": response["ETag"].strip('"'),
        "version_id": response.get("VersionId"),
    }