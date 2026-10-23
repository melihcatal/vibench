import os
from storage_client import get_s3_client, S3_BUCKET_NAME
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse

def get_object_metadata(request: ObjectMetadataRequest) -> ObjectMetadataResponse:
    s3_client = get_s3_client()

    try:
        response = s3_client.head_object(Bucket=S3_BUCKET_NAME, Key=request.object_key)
        metadata = {
            'ContentLength': response.get('ContentLength'),
            'ContentType': response.get('ContentType'),
            'LastModified': response.get('LastModified').isoformat() if response.get('LastModified') else None,
            'ETag': response.get('ETag').strip('"'),
            'UserMetadata': response.get('Metadata', {})
        }
        return ObjectMetadataResponse(success=True, object_key=request.object_key, metadata=metadata)
    except s3_client.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            return ObjectMetadataResponse(success=False, object_key=request.object_key, error_message="Object not found")
        return ObjectMetadataResponse(success=False, object_key=request.object_key, error_message=str(e))
    except Exception as e:
        return ObjectMetadataResponse(success=False, object_key=request.object_key, error_message=str(e))
