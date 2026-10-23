from storage_client import get_s3_client
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse

def object_metadata(request: ObjectMetadataRequest) -> ObjectMetadataResponse:
    s3_client = get_s3_client()

    response = s3_client.head_object(
        Bucket=request.bucket_name,
        Key=request.object_name
    )

    # The response contains various metadata, including custom metadata prefixed with 'x-amz-meta-'
    # We'll return a filtered dictionary for simplicity, but in a real app, you might parse this more thoroughly.
    metadata = {
        'ContentType': response.get('ContentType'),
        'ContentLength': response.get('ContentLength'),
        'ETag': response.get('ETag', '').strip('"'),
        'LastModified': response.get('LastModified').isoformat() if response.get('LastModified') else None,
        'VersionId': response.get('VersionId'),
        **{k.lower(): v for k, v in response.get('Metadata', {}).items()} # Custom metadata
    }
    # Remove None values for cleaner output
    metadata = {k: v for k, v in metadata.items() if v is not None}

    return ObjectMetadataResponse(metadata=metadata)
