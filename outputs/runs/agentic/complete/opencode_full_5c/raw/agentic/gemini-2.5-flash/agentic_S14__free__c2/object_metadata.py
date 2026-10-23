from storage_client import get_s3_client
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse

def get_object_metadata(request: ObjectMetadataRequest) -> ObjectMetadataResponse:
    s3_client = get_s3_client()
    response = s3_client.head_object(
        Bucket=request.bucket_name,
        Key=request.object_key
    )
    return ObjectMetadataResponse(
        content_type=response.get('ContentType'),
        content_length=response.get('ContentLength'),
        last_modified=response.get('LastModified').isoformat() if response.get('LastModified') else None,
        e_tag=response.get('ETag').strip('\"\') if response.get('ETag') else None,
        metadata=response.get('Metadata', {})
    )
