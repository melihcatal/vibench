import os
import boto3
from storage_client import get_s3_client
from storage_models import UploadObjectRequest, UploadObjectResponse

def upload_object(request: UploadObjectRequest) -> UploadObjectResponse:
    s3_client = get_s3_client()
    
    # boto3 S3 `upload_fileobj` expects a file-like object
    # For raw bytes, `put_object` is more direct.
    s3_client.put_object(
        Bucket=request.bucket,
        Key=request.key,
        Body=request.data,
        ContentType=request.content_type
    )

    # To get ETag, we can do a head_object after upload, or parse response
    # For simplicity, let's assume successful put_object means object is there
    # and fetch ETag or return a placeholder if not directly available from put_object response
    # The ETag is returned in the response headers of put_object
    # put_object response is not directly typed in boto3, so we cast to dict
    response_data = s3_client.head_object(Bucket=request.bucket, Key=request.key)
    etag = response_data['ETag'].strip('"') if 'ETag' in response_data else ''

    return UploadObjectResponse(bucket=request.bucket, key=request.key, etag=etag)
