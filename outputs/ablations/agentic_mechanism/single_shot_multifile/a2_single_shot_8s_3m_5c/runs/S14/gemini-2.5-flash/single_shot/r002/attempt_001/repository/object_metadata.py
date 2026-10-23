import os
import boto3
from storage_client import get_s3_client
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse

def get_object_metadata(request: ObjectMetadataRequest) -> ObjectMetadataResponse:
    s3_client = get_s3_client()

    # AWS S3 `head_object` retrieves metadata without downloading the object body
    response = s3_client.head_object(
        Bucket=request.bucket,
        Key=request.key
    )

    # Extract relevant metadata
    size = response.get('ContentLength', 0)
    content_type = response.get('ContentType', 'application/octet-stream')
    etag = response.get('ETag', '').strip('"') # ETag includes quotes
    last_modified = response.get('LastModified') # This is a datetime object
    metadata = response.get('Metadata', {})

    return ObjectMetadataResponse(
        bucket=request.bucket,
        key=request.key,
        size=size,
        content_type=content_type,
        etag=etag,
        last_modified=last_modified.isoformat() if last_modified else None,
        metadata=metadata
    )
