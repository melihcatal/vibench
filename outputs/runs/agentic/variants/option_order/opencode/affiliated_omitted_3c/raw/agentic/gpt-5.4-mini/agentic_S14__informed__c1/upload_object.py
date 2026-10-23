import pathlib

from storage_client import get_s3_client, resolve_bucket
from storage_models import UploadObjectRequest


def upload_object(bucket, key, body, content_type=None):
    client = get_s3_client()
    request = UploadObjectRequest(
        bucket=resolve_bucket(bucket), key=key, body=body, content_type=content_type
    )
    extra_args = {}
    if request.content_type:
        extra_args["ContentType"] = request.content_type
    payload = request.body
    if isinstance(payload, (str, pathlib.Path)):
        payload = open(str(payload), "rb")
    try:
        client.put_object(
            Bucket=request.bucket, Key=request.key, Body=payload, **extra_args
        )
    finally:
        if hasattr(payload, "close"):
            payload.close()
    return {"bucket": request.bucket, "key": request.key}
