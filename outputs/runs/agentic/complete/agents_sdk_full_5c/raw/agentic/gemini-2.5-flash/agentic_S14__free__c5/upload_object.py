import boto3
from typing import BinaryIO, Optional
from storage_client import get_s3_client
from storage_models import ObjectUploadRequest, ObjectUploadResponse

def upload_object(request: ObjectUploadRequest) -> ObjectUploadResponse:
    """
    Uploads a file or byte stream to AWS S3 managed object storage.
    """
    s3_client = get_s3_client()
    try:
        if isinstance(request.data, BinaryIO):
            s3_client.upload_fileobj(request.data, request.bucket_name, request.object_key)
        else:
            s3_client.put_object(Bucket=request.bucket_name, Key=request.object_key, Body=request.data)
        return ObjectUploadResponse(success=True, message=f"Object {request.object_key} uploaded successfully to {request.bucket_name}")
    except Exception as e:
        return ObjectUploadResponse(success=False, message=f"Error uploading object: {e}")

