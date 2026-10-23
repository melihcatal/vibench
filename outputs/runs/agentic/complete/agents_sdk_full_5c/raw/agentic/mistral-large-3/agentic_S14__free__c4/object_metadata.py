import boto3
from botocore.exceptions import ClientError
from storage_client import get_storage_client
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse

def get_object_metadata(request: ObjectMetadataRequest) -> ObjectMetadataResponse:
    s3_client = get_storage_client()
    try:
        response = s3_client.head_object(
            Bucket=request.bucket_name,
            Key=request.object_key
        )
        return ObjectMetadataResponse(
            bucket_name=request.bucket_name,
            object_key=request.object_key,
            metadata=response.get('Metadata', {}),
            content_type=response.get('ContentType'),
            content_length=response.get('ContentLength'),
            last_modified=response.get('LastModified'),
            etag=response.get('ETag'),
            success=True
        )
    except ClientError as e:
        return ObjectMetadataResponse(
            bucket_name=request.bucket_name,
            object_key=request.object_key,
            success=False,
            error=str(e)
        )