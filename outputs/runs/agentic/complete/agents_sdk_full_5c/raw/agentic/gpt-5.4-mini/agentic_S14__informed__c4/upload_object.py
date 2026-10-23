from __future__ import annotations

import boto3

from storage_client import coerce_bucket, get_s3_client
from storage_models import UploadRequest, normalize_metadata


def upload_object(request: UploadRequest):
    client = get_s3_client()
    bucket = coerce_bucket(request.bucket)
    kwargs = {
        "Bucket": bucket,
        "Key": request.key,
        "Body": request.data,
    }
    if request.content_type:
        kwargs["ContentType"] = request.content_type
    metadata = normalize_metadata(request.metadata)
    if metadata:
        kwargs["Metadata"] = metadata
    return client.put_object(**kwargs)
