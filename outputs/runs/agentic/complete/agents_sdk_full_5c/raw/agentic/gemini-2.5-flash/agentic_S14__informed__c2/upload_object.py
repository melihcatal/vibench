import os
import boto3
from storage_client import get_s3_client, get_s3_bucket_name
from storage_models import ObjectStorageUploadRequest

def upload_object(request: ObjectStorageUploadRequest) -> str:
    s3_client = get_s3_client()
    bucket_name = get_s3_bucket_name()

    if request.file_path:
        if not os.path.exists(request.file_path):
            raise FileNotFoundError(f"File not found at {request.file_path}")
        extra_args = {'ContentType': request.content_type} if request.content_type else {}
        s3_client.upload_file(request.file_path, bucket_name, request.object_key, ExtraArgs=extra_args)
    elif request.data is not None:
        extra_args = {'ContentType': request.content_type} if request.content_type else {}
        s3_client.put_object(Bucket=bucket_name, Key=request.object_key, Body=request.data, **extra_args)
    else:
        raise ValueError("Either file_path or data must be provided for upload.")

    return f"s3://{bucket_name}/{request.object_key}"
