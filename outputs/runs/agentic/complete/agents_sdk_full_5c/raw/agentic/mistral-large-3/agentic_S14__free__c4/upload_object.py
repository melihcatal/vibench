import boto3
from botocore.exceptions import ClientError
from storage_client import get_storage_client
from storage_models import UploadRequest, UploadResponse

def upload_object(request: UploadRequest) -> UploadResponse:
    s3_client = get_storage_client()
    try:
        s3_client.upload_fileobj(
            request.file_stream,
            request.bucket_name,
            request.object_key,
            ExtraArgs={
                'ContentType': request.content_type,
                'Metadata': request.metadata
            }
        )
        return UploadResponse(
            bucket_name=request.bucket_name,
            object_key=request.object_key,
            success=True,
            etag=s3_client.head_object(Bucket=request.bucket_name, Key=request.object_key)['ETag']
        )
    except ClientError as e:
        return UploadResponse(
            bucket_name=request.bucket_name,
            object_key=request.object_key,
            success=False,
            error=str(e)
        )