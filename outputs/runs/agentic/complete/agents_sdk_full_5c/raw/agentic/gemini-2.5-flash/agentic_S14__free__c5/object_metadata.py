import boto3
from typing import Dict, Any
from storage_client import get_s3_client
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse

def get_object_metadata(request: ObjectMetadataRequest) -> ObjectMetadataResponse:
    """
    Reads object metadata or head information from AWS S3 managed object storage.
    """
    s3_client = get_s3_client()
    try:
        response = s3_client.head_object(Bucket=request.bucket_name, Key=request.object_key)
        metadata = {k: v for k, v in response.items() if k not in ['ResponseMetadata', 'ETag', 'LastModified']}
        metadata['ETag'] = response.get('ETag', '').strip(''"')
        metadata['LastModified'] = response.get('LastModified').isoformat() if 'LastModified' in response else None
        
        user_metadata = response.get('Metadata', {})

        return ObjectMetadataResponse(
            success=True,
            object_key=request.object_key,
            bucket_name=request.bucket_name,
            size=response.get('ContentLength'),
            content_type=response.get('ContentType'),
            last_modified=metadata['LastModified'],
            etag=metadata['ETag'],
            user_metadata=user_metadata,
            raw_metadata=metadata
        )
    except s3_client.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            return ObjectMetadataResponse(success=False, message=f"Object {request.object_key} not found in {request.bucket_name}.")
        return ObjectMetadataResponse(success=False, message=f"Error retrieving object metadata: {e}")
    except Exception as e:
        return ObjectMetadataResponse(success=False, message=f"An unexpected error occurred: {e}")

