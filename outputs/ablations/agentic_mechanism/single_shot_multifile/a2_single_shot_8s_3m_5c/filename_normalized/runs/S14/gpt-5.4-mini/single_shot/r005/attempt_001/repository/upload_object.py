import boto3
from storage_client import get_s3_client, resolve_bucket_name
from storage_models import UploadRequest, UploadResponse, coerce_bytes


def upload_object(request: UploadRequest) -> UploadResponse:
    s3 = get_s3_client()
    bucket = resolve_bucket_name(request.bucket)
    body = coerce_bytes(request.body)
    extra_args = {}
    if request.content_type:
        extra_args['ContentType'] = request.content_type
    if request.metadata:
        extra_args['Metadata'] = request.metadata
    if request.server_side_encryption:
        extra_args['ServerSideEncryption'] = request.server_side_encryption
    s3.put_object(Bucket=bucket, Key=request.key, Body=body, **extra_args)
    return UploadResponse(bucket=bucket, key=request.key, content_length=len(body), etag=None)
